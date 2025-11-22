from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

class LLMWrapper:
    def __init__(self, model_name="gpt-4", temperature=0):
        self.model = ChatOpenAI(model_name=model_name, temperature=temperature)

    def run(self, prompt: str):
        chat_prompt = ChatPromptTemplate.from_template(prompt)
        return self.model(chat_prompt.format())
