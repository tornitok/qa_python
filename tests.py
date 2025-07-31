import pytest

from main import BooksCollector

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

    @pytest.mark.parametrize("book_name, genre", [
        ("1984", "Фантастика"),
        ("It", "Ужасы"),
        ("Шерлок Холмс", "Детективы"),
    ])
    def test_set_book_genre_valid_book_and_genre(self, book_name, genre):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.books_genre[book_name] == genre

    @pytest.mark.parametrize("book_name, invalid_genre", [
        ("Dracula", "Романтика"),
        ("Tom & Jerry", "Приключения"),
    ])
    def test_set_book_genre_invalid_genre(self, book_name, invalid_genre):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, invalid_genre)
        assert collector.books_genre[book_name] == ""

    def test_get_book_genre_valid_book_and_genre(self):
        collector = BooksCollector()
        book_name = collector.add_new_book('Горе от ума')
        genre = collector.set_book_genre(book_name, 'Комедия')
        assert collector.get_book_genre(genre) == book_name



