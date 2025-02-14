from injector import Module, singleton, provider

from app.core.settings import Settings
from app.data.data_provider import DataProvider
from app.data.data_source import TableDataSource
from app.infrastructure.scrape_client import ScrapeClient
from app.use_cases.summarize_use_case import SummarizeUseCase


class AppModule(Module):
    @singleton
    @provider
    def provide_settings(self) -> Settings:
        return Settings()

    @singleton
    @provider
    def provide_scrape_client(self) -> ScrapeClient:
        return ScrapeClient()

    @singleton
    @provider
    def provide_summarize_use_case(self, client: ScrapeClient) -> SummarizeUseCase:
        return SummarizeUseCase(client)

    @singleton
    @provider
    def provide_data_provider(self, settings: Settings) -> DataProvider:
        return DataProvider(
            self._create_models_datasource(settings.MODELS_FILE_PATH),
            self._create_websites_datasource(settings.WEBSITES_FILE_PATH))

    @staticmethod
    def _create_models_datasource(models_file_path: str):
        return TableDataSource(
            source_type="file",
            headers=["model", "tokens"],
            datatype=["str", "number"],
            file_path=models_file_path)

    @staticmethod
    def _create_websites_datasource(website_file_path: str):
        return TableDataSource(
            source_type="file",
            headers=["website"],
            datatype=["str"],
            file_path=website_file_path)
