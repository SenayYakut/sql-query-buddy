from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

class SchemaRetriever:
    def __init__(self, persist_directory="vectorstore"):
        self.embeddings = OpenAIEmbeddings()
        self.db = Chroma(persist_directory=persist_directory, embedding_function=self.embeddings)

    def retrieve(self, query: str, k: int = 5):
        return self.db.similarity_search(query, k=k)
