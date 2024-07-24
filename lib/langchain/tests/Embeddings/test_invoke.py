import pytest
from ally_ai_langchain import Embeddings
from openai import APIConnectionError


def test_embed_query_simple_raises_APIConnectionError():
    embeddings = Embeddings()
    with pytest.raises(APIConnectionError):
        embeddings.embed_query('test')