import json
import abc
from pathlib import Path


class DataLoader(abc.ABC):

    @abc.abstractmethod
    def load(self):
        raise NotImplementedError("Please Implement this method")

class FileLoader(DataLoader):
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def load(self):
        if not self.file_path.exists():
            raise FileNotFoundError(f"File {self.file_path} not found.")

        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data


