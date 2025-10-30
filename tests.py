import pytest
from main import BooksCollector


@pytest.fixture
def collector():
    return BooksCollector()


# ---------- add_new_book ----------
def test_add_new_book_add_two_books(collector):
    collector.add_new_book('Гордость и предубеждение и зомби')
    collector.add_new_book('Что делать, если ваш кот хочет вас убить')
    assert len(collector.get_books_genre()) == 2


def test_add_new_book_does_not_add_duplicate(collector):
    collector.add_new_book('Дубликат')
    collector.add_new_book('Дубликат')
    assert len(collector.get_books_genre()) == 1


# проверяем добавление книг: 1, 39, 40 символов
@pytest.mark.parametrize('values', ['a' * 1, 'a' * 39, 'a' * 40])
def test_add_new_book_check_positive_boundary_values(collector, values):
    collector.add_new_book(values)
    assert values in collector.get_books_genre()


# негативные границы: пустая строка и 41 символ не добавляются
@pytest.mark.parametrize('bad_name', ['', 'a' * 41])
def test_add_new_book_does_not_add_out_of_bounds_names(collector, bad_name):
    collector.add_new_book(bad_name)
    assert bad_name not in collector.get_books_genre()


# ---------- set_book_genre / get_book_genre ----------
def test_set_book_genre_success_when_valid(collector):
    collector.add_new_book('Книга жанра')
    collector.set_book_genre('Книга жанра', 'Фантастика')
    assert collector.get_book_genre('Книга жанра') == 'Фантастика'


@pytest.mark.parametrize('bad_genre', ['Роман', 'horror', '', None])
def test_set_book_genre_ignores_invalid_genre(collector, bad_genre):
    collector.add_new_book('Книга без жанра')
    # жанр не из списка допустимых — не должен установиться
    collector.set_book_genre('Книга без жанра', bad_genre)
    assert collector.get_book_genre('Книга без жанра') == ''


def test_set_book_genre_ignored_for_unknown_book(collector):
    # книги нет в словаре — ничего не происходит
    collector.set_book_genre('Несуществующая', 'Фантастика')
    assert collector.get_books_genre() == {}


def test_get_book_genre_returns_none_for_unknown(collector):
    assert collector.get_book_genre('Неизвестная книга') is None


# ---------- get_books_with_specific_genre / get_books_genre ----------
def test_get_books_with_specific_genre_returns_only_that_genre(collector):
    collector.add_new_book('Детская 1')
    collector.add_new_book('Детская 2')
    collector.add_new_book('Ужас 1')
    collector.set_book_genre('Детская 1', 'Мультфильмы')
    collector.set_book_genre('Детская 2', 'Комедии')
    collector.set_book_genre('Ужас 1', 'Ужасы')

    res = collector.get_books_with_specific_genre('Мультфильмы')
    assert set(res) == {'Детская 1'}


def test_get_books_genre_returns_full_mapping(collector):
    collector.add_new_book('А')
    collector.add_new_book('Б')
    collector.set_book_genre('А', 'Комедии')
    data = collector.get_books_genre()
    assert isinstance(data, dict) and data['А'] == 'Комедии' and data['Б'] == ''


# ---------- get_books_for_children ----------
def test_get_books_for_children_excludes_age_rated(collector):
    # возрастной рейтинг есть у жанров: 'Ужасы', 'Детективы'
    collector.add_new_book('Детям ОК 1')
    collector.add_new_book('Детям ОК 2')
    collector.add_new_book('Не детям 1')
    collector.add_new_book('Не детям 2')

    collector.set_book_genre('Детям ОК 1', 'Мультфильмы')
    collector.set_book_genre('Детям ОК 2', 'Комедии')
    collector.set_book_genre('Не детям 1', 'Ужасы')
    collector.set_book_genre('Не детям 2', 'Детективы')

    children = collector.get_books_for_children()
    assert set(children) == {'Детям ОК 1', 'Детям ОК 2'}


# ---------- favorites ----------
def test_add_book_in_favorites_adds_only_if_present_and_no_duplicates(collector):
    collector.add_new_book('Любимая')
    collector.add_book_in_favorites('Любимая')
    collector.add_book_in_favorites('Любимая')          # повторно не добавится
    collector.add_book_in_favorites('Нет в словаре')    # не существует в books_genre
    assert collector.get_list_of_favorites_books() == ['Любимая']

