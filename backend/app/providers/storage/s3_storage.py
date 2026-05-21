from app.providers.storage.base import StorageProviderInterface


class S3StorageProvider(StorageProviderInterface):
    async def save(self, content: bytes, destination: str) -> str:
        raise NotImplementedError("S3 provider implementation requires cloud credentials and SDK wiring")

    async def delete(self, destination: str) -> None:
        raise NotImplementedError("S3 provider implementation requires cloud credentials and SDK wiring")
