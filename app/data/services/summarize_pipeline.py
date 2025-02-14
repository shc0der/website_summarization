from chonkie import SentenceChunker
from transformers import pipeline


class SummarizePipeline:
    def __init__(self, model_name: str, max_tokens: int=512):
        self._summarizer = pipeline("summarization", model=model_name)

        self._chunker = SentenceChunker(
            tokenizer=model_name,
            chunk_size=max_tokens,
            chunk_overlap=128,
            min_sentences_per_chunk=1
        )

    def summarize(self, text:str):
        text_chunks = self._chunker.chunk(text)
        for chunk in text_chunks:
            print(f"Chunk text: {chunk.text}")
            print(f"Token count: {chunk.token_count}")
            print(f"Number of sentences: {len(chunk.sentences)}\n")

            try:
                summary = self._summarizer(chunk.text, max_length=130, min_length=30, do_sample=False)
                print(f"Summary: {summary[0]['summary_text']}")

                yield summary[0]['summary_text']
            except Exception as e:
                yield f"\n\n**Error:**{e}\n\n"
        print(f"#" * 80)
