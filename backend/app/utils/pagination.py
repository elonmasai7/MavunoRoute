from math import ceil


def build_pagination_meta(page: int, per_page: int, total: int) -> dict:
    total_pages = ceil(total / per_page) if per_page else 1
    return {
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
    }
