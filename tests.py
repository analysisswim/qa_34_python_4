import pytest
from main import BooksCollector


@pytest.fixture
def collector():
    return BooksCollector()


# ---------- add_new_book ----------
def test_add_new_book_add_two_books(collector):
    collector.add_new_book('Гордость и предубеждение и зомби')
    collector.add_new_book('Что делать, если ваш кот хочет вас убить')
    assert len(collector.books_genre) == 2

def test_add_new_book_does_not_add_duplicate(collector):
    collector.add_new_book('Дубликат')
    collector.add_new_book('Дубликат')
    assert len(collector.books_genre) == 1

@pytest.mark.parametrize('values', ['a' * 1, 'a' * 39, 'a' * 40])
def test_add_new_book_check_positive_boundary_values(collector, values):
    collector.add_new_book(values)
    assert values in collector.books_genre

@pytest.mark.parametrize('bad_name', ['', 'a' * 41])
def test_add_new_book_does_not_add_out_of_bounds_names(collector, bad_name):
    collector.add_new_book(bad_name)
    assert bad_name not in collector.books_genre



# ---------- set_book_genre / get_book_genre (РАЗДЕЛЕНЫ) ----------
@pytest.mark.parametrize('genre', BooksCollector().genre)
def test_set_book_genre_sets_value_in_mapping_for_all_allowed(collector, genre):
    collector.books_genre = {'Книга жанра': ''}
    collector.set_book_genre('Книга жанра', genre)
    assert collector.books_genre['Книга жанра'] == genre

@pytest.mark.parametrize('bad_genre', ['Роман', 'horror', '', None])
def test_set_book_genre_ignores_invalid_genre(collector, bad_genre):
    collector.books_genre = {'Книга без жанра': ''}
    collector.set_book_genre('Книга без жанра', bad_genre)
    assert collector.books_genre['Книга без жанра'] == ''

def test_set_book_genre_ignored_for_unknown_book(collector):
    collector.set_book_genre('Несуществующая', 'Фантастика')
    assert collector.books_genre == {}

@pytest.mark.parametrize('genre', BooksCollector().genre)
def test_get_book_genre_returns_value_from_mapping_for_all_allowed(collector, genre):
    collector.books_genre = {'Книга жанра 2': genre}
    assert collector.get_book_genre('Книга жанра 2') == genre

# get: неизвестная книга — None
def test_get_book_genre_returns_none_for_unknown(collector):
    assert collector.get_book_genre('Неизвестная книга') is None


# ---------- get_books_with_specific_genre / get_books_genre ----------
def test_get_books_with_specific_genre_returns_only_that_genre(collector):
    collector.books_genre = {
        'Детская 1': 'Мультфильмы',
        'Детская 2': 'Комедии',
        'Ужас 1': 'Ужасы',
    }
    result = collector.get_books_with_specific_genre('Мультфильмы')
    assert set(result) == {'Детская 1'}


def test_get_books_genre_returns_current_mapping(collector):
    expected = {'А': 'Комедии', 'Б': ''}
    collector.books_genre = dict(expected)
    assert collector.get_books_genre() == expected


# ---------- get_books_for_children ----------
def test_get_books_for_children_excludes_age_rated(collector):
    # возрастной рейтинг: 'Ужасы', 'Детективы'
    collector.books_genre = {
        'Детям ОК 1': 'Мультфильмы',
        'Детям ОК 2': 'Комедии',
        'Не детям 1': 'Ужасы',
        'Не детям 2': 'Детективы',
    }
    children = collector.get_books_for_children()
    assert set(children) == {'Детям ОК 1', 'Детям ОК 2'}



# ---------- избранное: add / get / delete (РАЗДЕЛЬНО) ----------
def test_add_book_in_favorites_only_existing_no_duplicates(collector):
    # книга должна быть в books_genre; дубликаты не добавляются; неизвестная игнорируется
    collector.books_genre = {'Любимая': '', 'Вторая': ''}
    collector.add_book_in_favorites('Любимая')
    collector.add_book_in_favorites('Любимая')        # дубль не добавится
    collector.add_book_in_favorites('Нет в словаре')  # игнор
    assert collector.favorites == ['Любимая']


def test_get_list_of_favorites_books_returns_current_list(collector):
    collector.favorites = ['А', 'Б']
    assert collector.get_list_of_favorites_books() == ['А', 'Б']


def test_delete_book_from_favorites_removes_and_is_idempotent(collector):
    collector.favorites = ['А', 'Б']
    collector.delete_book_from_favorites('А')
    assert collector.favorites == ['Б']
    # повторное удаление того же элемента — без эффекта
    collector.delete_book_from_favorites('А')
    assert collector.favorites == ['Б']
