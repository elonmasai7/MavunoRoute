from collections import defaultdict, deque
from datetime import UTC, datetime, timedelta

from fastapi import Request
from fastapi.responses import JSONResponse
from redis import Redis
from redis.exceptions import RedisError
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import get_settings
from app.utils.response import error_response

settings = get_settings()


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'"
        )
        return response


class DistributedRateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.redis = Redis.from_url(
            settings.redis_url,
            decode_responses=True,
            socket_connect_timeout=0.2,
            socket_timeout=0.2,
        )
        self.redis_backoff_until: datetime | None = None
        self.hits: dict[str, deque[datetime]] = defaultdict(deque)

    @staticmethod
    def _request_ip(request: Request) -> str:
        return request.headers.get("x-forwarded-for", request.client.host if request.client else "unknown").split(",")[0].strip()

    @staticmethod
    def _path_bucket(path: str) -> str:
        return "/".join(path.split("/")[:4])

    @staticmethod
    def _minute_bucket(now: datetime) -> str:
        return now.strftime("%Y%m%d%H%M")

    def _get_limit(self, path: str) -> int | None:
        if path.startswith(f"{settings.api_prefix}/auth"):
            return settings.rate_limit_auth_per_minute
        if path.startswith(f"{settings.api_prefix}/weather") or path.startswith(f"{settings.api_prefix}/health"):
            return settings.rate_limit_public_per_minute
        return None

    def _allow_with_redis(self, ip: str, path_bucket: str, limit: int, now: datetime) -> bool | None:
        if self.redis_backoff_until and now < self.redis_backoff_until:
            return None

        key = f"rate_limit:{path_bucket}:{ip}:{self._minute_bucket(now)}"
        try:
            pipeline = self.redis.pipeline()
            pipeline.incr(key)
            pipeline.expire(key, 70)
            count, _ = pipeline.execute()
            return int(count) <= limit
        except RedisError:
            self.redis_backoff_until = now + timedelta(seconds=30)
            return None

    def _allow_with_memory(self, ip: str, path_bucket: str, limit: int, now: datetime) -> bool:
        key = f"{ip}:{path_bucket}"
        window = timedelta(minutes=1)
        queue = self.hits[key]
        while queue and now - queue[0] > window:
            queue.popleft()
        if len(queue) >= limit:
            return False
        queue.append(now)
        return True

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if path.startswith("/docs") or path.startswith("/redoc"):
            return await call_next(request)

        limit = self._get_limit(path)

        if limit:
            now = datetime.now(UTC)
            ip = self._request_ip(request)
            path_bucket = self._path_bucket(path)

            allowed = self._allow_with_redis(ip, path_bucket, limit, now)
            if allowed is None:
                allowed = self._allow_with_memory(ip, path_bucket, limit, now)

            if not allowed:
                return JSONResponse(
                    status_code=429,
                    content=error_response("Rate limit exceeded", "RATE_LIMIT_EXCEEDED", {}),
                )

        return await call_next(request)
