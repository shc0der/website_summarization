from typing import Tuple

from bs4 import BeautifulSoup

from app.data.services.summarize_pipeline import SummarizePipeline
from app.infrastructure.scrape_client import ScrapeClient


class SummarizeUseCase:
    def __init__(self, client: ScrapeClient):
        self._client = client

    def execute(self, models:list, websites:list) -> Tuple[str, str]:
        client = ScrapeClient()
        for model_config in models:
            model_name = model_config["model"]
            query = f"**{model_name}**"
            yield (query, query)

            text = f"The text is being summarized with the model {model_name} for the website: "
            yield (query, text)

            summarizer =  SummarizePipeline(model_name, model_config["tokens"])
            for website in websites:
                yield (query, f"**{website}**\n")

                text = self._extract_text(client.get(website))
                for chunk in summarizer.summarize(text):
                    yield (query, f"{chunk}\n")


    @staticmethod
    def _extract_text(html_content: str):
        soup = BeautifulSoup(html_content, "html.parser")

        for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
            element.decompose()

        text = soup.get_text(separator=" ")
        clean_text = ' '.join(text.split())

        return clean_text