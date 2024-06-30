import os
os.environ["OPENAI_API_KEY"] = "<put_your_token_here>"
assert os.environ["OPENAI_API_KEY"].startswith("sk-"), "Fix your OpenAI API Key in `meeting_note/lib/__init__.py`"
