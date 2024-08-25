import os
assert os.environ.get("OPENAI_API_KEY", '').startswith("sk-"), 'Fix your OpenAI API Key by prepending: os.environ["OPENAI_API_KEY"] = "<put_your_token_here>"'
os.environ["OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"].strip()
