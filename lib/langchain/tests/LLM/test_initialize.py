from ally_ai_langchain import LLM


def test_default_llm_is_not_none():
    llm = LLM()
    assert llm is not None