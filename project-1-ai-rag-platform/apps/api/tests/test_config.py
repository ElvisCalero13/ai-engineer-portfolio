from src.config import settings


def test_default_environment():
    assert settings.environment in ["dev", "test", "prod"]


def test_default_embedding_provider():
    assert settings.embedding_provider in ["local", "openai"]


def test_default_llm_provider():
    assert settings.llm_provider in ["local", "openai"]