from openai import OpenAI
import traceback


class GPTModel:
    def __init__(self, model_name="gpt-3.5-turbo"):
        self.client = OpenAI()
        self.model = model_name

    def infer(self, text, history=None, system=None):
        try:
            if system is None:
                system = "You are a helpful assistant"
            if history is None:
                history = []
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    *history,
                    {"role": "user", "content": text},
                ]
            )
            assert len(response.choices) > 0, "GPTModel Bad result"
            content = response.choices[0].message.content
            history = [
                *history,
                {"role": "user", "content": text},
                {"role": "assistance", "content": content},
            ]
            return {"text": content, "history": history}
        except Exception:
            raise GPTModelError(traceback.format_exc())


class SummarizeModel(GPTModel):
    def __init__(self, model_name="gpt-3.5-turbo", prompt=None):
        super().__init__(model_name)
        self.prompt = prompt
        if self.prompt is None:
            self.prompt = "Please summarize the following paragraph:"

    def infer(self, paragraph, history=None, system=None):
        if system is None:
            system = "You're a helpful assistant to summarize long paragraphs."
        text = "{} {}".format(self.prompt, paragraph)
        return super().infer(text, history, system)

class GPTModelError(Exception):
    pass