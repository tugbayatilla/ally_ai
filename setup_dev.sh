python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip

which python3

pip install -r ./requirements.txt

PYTHONPATH=./lib/core:./lib/langchain:./lib/llamaindex:./lib/ally::./lib/chroma
export PYTHONPATH