from pathlib import Path

from app.providers.storage.base import StorageProviderInterface


class LocalStorageProvider(StorageProviderInterface):
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    async def save(self, content: bytes, destination: str) -> str:
        target = self.base_path / destination
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        return str(target)

    async def delete(self, destination: str) -> None:
        target = self.base_path / destination
        if target.exists():
            target.unlink()
