import os
import abc
from dataclasses import dataclass
from typing import Optional, Any, Dict, List

import pandas as pd

@dataclass
class TableData:
    values: pd.DataFrame
    headers: list
    datatype: list

class DataSource(abc.ABC):

    @abc.abstractmethod
    def extract(self):
        raise NotImplementedError("Please Implement this method")


class TableDataSource(DataSource):
    def __init__(self, source_type: str, headers: list, datatype: list, file_path: Optional[str] = None):
        if source_type == "file":
            if file_path is None:
                raise FileNotFoundError(f"File is empty.")
            if not os.path.exists(file_path):
                raise FileExistsError(f"File {file_path} not found.")

            from app.data.data_loader import FileLoader
            self._file_loader = FileLoader(file_path)

        self._source_type = source_type
        self._headers = headers
        self._datatype = datatype

    def extract(self):
        if self._source_type == "file":
            return self._make_result(self._file_loader.load())
        elif self._source_type == "empty":
            return self._make_result()
        else:
            ValueError(f"Invalid source type ({self._source_type})")

    def _make_result(self, data: Optional[List[Dict[str, Any]]] = None):
        return TableData(
            values=self._apply_transformations(data, self._headers),
            headers=self._headers,
            datatype=self._datatype)

    @staticmethod
    def _apply_transformations(data: Optional[List[Dict[str, Any]]], headers: list):
        return pd.DataFrame(data) if data else pd.DataFrame(columns=headers)
