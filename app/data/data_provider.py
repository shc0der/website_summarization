from app.data.data_source import TableDataSource


class DataProvider:
    def __init__(self, models_datasource: TableDataSource, websites_datasource: TableDataSource):
        self._data_sources = {
            "models": models_datasource,
            "websites": websites_datasource
        }

    def of(self, data_type: str):
        datasource = self._data_sources.get(data_type)
        if datasource:
            return datasource#.extract()
        else:
            raise ValueError(f"Invalid data type ({data_type})")
