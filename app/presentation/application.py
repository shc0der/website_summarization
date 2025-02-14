import time
from typing import List

import pandas as pd
from gradio import ChatMessage
from injector import inject
import gradio as gr

from app.data.data_provider import DataProvider
from app.use_cases.summarize_use_case import SummarizeUseCase


class Application:
    @inject
    def __init__(self, data_provider: DataProvider, summarize_use_case: SummarizeUseCase):
        self._data_provide = data_provider
        self._summarize_use_case = summarize_use_case


    def _on_summarize(self, models: pd.DataFrame, websites: pd.DataFrame, history:List[ChatMessage]):
        models = models[["tokens", "model"]].replace("", None).dropna()

        selected_models = models.to_dict("records")
        selected_websites = websites[websites['website'].str.len() > 0]["website"].to_list()

        if selected_models and selected_websites:# and False:
            last_query = ""
            for query, text in self._summarize_use_case.execute(selected_models, selected_websites):
                if last_query != query:
                    last_query = query
                    history.append(gr.ChatMessage(role="user", content=text))

                    yield history
                else:
                    if history[-1].role == "user":
                        history.append(gr.ChatMessage(content=""))

                    for char in text:
                        history[-1].content += char

                        yield history
                        time.sleep(0.06)
        else:
            for c in selected_models or []:
                history.append(gr.ChatMessage(content=f"{c['model']} : {c['tokens']}"))
                yield history

            history.append(gr.ChatMessage(content="Incorrect data. Models and Websites must be specified."))
            yield history


    def launch(self):
        with gr.Blocks(title="Streaming Chat API") as demo:
            gr.Markdown("## Testing of summarization")

            with gr.Row():
                with gr.Column(scale=1):
                    summarize_btn = gr.Button("Summarize")

                    models_data = self._data_provide.of("models").extract()
                    websites_data = self._data_provide.of("websites").extract()

                    models = gr.Dataframe(
                        value=models_data.values,
                        headers=models_data.headers,
                        datatype=models_data.datatype,
                        interactive=True,
                        col_count=(len(models_data.headers), "fixed"),
                        column_widths=[2, 1],
                        max_chars=24,
                        max_height=224,
                        line_breaks=False,
                    )

                    websites = gr.Dataframe(
                        value=websites_data.values,
                        headers=websites_data.headers,
                        datatype=websites_data.datatype,
                        interactive=True,
                        col_count=(len(websites_data.headers), "fixed"),
                        max_chars=24,
                        line_breaks=False,
                        max_height=300
                    )
                with gr.Column(scale=4):
                    chatbot = gr.Chatbot(
                        label="Summarization results",
                        type="messages",
                        min_height="85vh",
                        height="800",
                        show_copy_button=True,
                        resizeable=True)

            summarize_btn.click(
                self._on_summarize,
                inputs=[models, websites, chatbot],
                outputs=[chatbot],
            )

            demo.launch(server_name='0.0.0.0',server_port=7860)