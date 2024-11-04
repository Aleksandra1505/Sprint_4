from main import BooksCollector
import pytest

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.get_books_rating()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

    @pytest.mark.parametrize("book_title, expected_result", [
    ("1984", True),                # добавление корректного названия
    ("", False),                   # пустое название
    ("Valid Title", True),         # валидное название
    ("A" * 41, False),            # слишком длинное название
    ("Do not let me down", True)
    ])
    def test_add_new_book(self, book_title, expected_result):
        collector = BooksCollector()
        collector.add_new_book(book_title)

        if expected_result:
            assert book_title in collector.books_genre
        else:
            assert book_title not in collector.books_genre

    @pytest.mark.parametrize("book_title, genre, expected_genre", [
        ("Mizzery", "Ужасы", "Ужасы"),
        ("IT", "Комедии", "Комедии"),
    ])

    def test_set_book_genre_updates_genre_for_existing_book(self, book_title, genre, expected_genre):
        collector = BooksCollector()
        collector.add_new_book(book_title)
        collector.set_book_genre(book_title, genre)
        assert collector.books_genre[book_title] == expected_genre

    def  test_set_book_genre_does_not_change_genre_for_non_existing_book(self):
        collector = BooksCollector()
        collector.add_new_book('Mizzery')
        collector.set_book_genre('Non Existing Book', 'Ужасы')
        assert collector.books_genre['Mizzery'] == ''

    @pytest.mark.parametrize("book_title, initial_genre, new_genre, expected_genre", [
        ("IT", "Ужасы", "Комедии", "Комедии"),
        ("Carrie", "Ужасы", "Андерграунд", "Ужасы"),  # Не валидный жанр
    ])
    def test_set_book_genre_updates_genre_for_existing_book(self, book_title, initial_genre, new_genre, expected_genre):
        collector = BooksCollector()
        collector.add_new_book(book_title)
        collector.set_book_genre(book_title,  initial_genre)
        collector.set_book_genre(book_title, new_genre)
        assert collector.books_genre[book_title] == expected_genre

    def test_get_book_genre_for_existing_book_with_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Carrie')
        collector.set_book_genre('Carrie', 'Ужасы')

        assert collector.get_book_genre('Carrie') == 'Ужасы'

    def test_get_book_genre_for_existing_book_without_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Carrie')

        assert collector.get_book_genre('Carrie') == ''

    def test_get_books_with_specific_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Carrie')
        collector.set_book_genre('Carrie', 'Ужасы')

        collector.add_new_book('1408')
        collector.set_book_genre('1408', 'Ужасы')

        collector.add_new_book('my family and other animals')
        collector.set_book_genre('my family and other animals', 'Комедии')

        assert collector.get_books_with_specific_genre('Ужасы') == ['Carrie', '1408']

    def test_test_get_books_with_specific_genre_with_no_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Twilight')

        assert collector.get_books_with_specific_genre('Ужасы') == []

    def test_get_books_genre_returns_empty_dict_when_no_books(self):
        collector = BooksCollector()
        assert collector.get_books_genre() == {}

    def test_get_books_genre_returns_dict_with_one_book_without_genre(self):
        collector = BooksCollector()
        collector.add_new_book('1984')
        assert collector.get_books_genre() == {'1984': ''}

    def test_get_books_for_children_with_childrens_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Treasure Island')
        collector.set_book_genre('Treasure Island', 'Мультфильмы')
        assert collector.get_books_for_children() == ['Treasure Island']

    def test_add_book_in_favorites_if_book_exists_in_books_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Treasure Island')
        collector.set_book_genre('Treasure Island', 'Мультфильмы')
        collector.add_book_in_favorites('Treasure Island')
        assert 'Treasure Island' in collector.favorites

    def test_delete_book_from_favorites_removes_book_if_it_exists_in_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Treasure Island')
        collector.set_book_genre('Treasure Island', 'Мультфильмы')

        collector.add_book_in_favorites('Treasure Island')
        assert 'Treasure Island' in collector.favorites

        collector.delete_book_from_favorites('Treasure Island')
        assert 'Treasure Island' not in collector.favorites

    def test_get_list_of_favorites_books_if_you_have_books_in_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Treasure Island')
        collector.set_book_genre('Treasure Island', 'Мультфильмы')

        collector.add_book_in_favorites('Treasure Island')

        favorites_list = collector.get_list_of_favorites_books()
        assert 'Treasure Island' in favorites_list
        assert len(favorites_list) == 1
