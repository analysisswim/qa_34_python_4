import pytest


from main import BooksCollector


@pytest.fixture
def collector():
    collector = BooksCollector()
    return collector
