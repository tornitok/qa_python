import pytest

from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # # пример теста:
    # # обязательно указывать префикс test_
    # # дальше идет название метода, который тестируем add_new_book_
    # # затем, что тестируем add_two_books - добавление двух книг
    # def test_add_new_book_add_two_books(self):
    #     # создаем экземпляр (объект) класса BooksCollector
    #     collector = BooksCollector()
    #
    #     # добавляем две книги
    #     collector.add_new_book('Гордость и предубеждение и зомби')
    #     collector.add_new_book('Что делать, если ваш кот хочет вас убить')
    #
    #     # проверяем, что добавилось именно две
    #     # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
    #     assert len(collector.get_books_rating()) == 2
    #
    # # напиши свои тесты ниже
    # # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

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

    def test_get_book_genre_valid_book_and_genre(self, collector):
        collector.add_new_book('Горе от ума')
        collector.set_book_genre('Горе от ума', 'Комедии')
        assert collector.get_book_genre('Горе от ума') == 'Комедии'


    def test_get_books_with_specific_genre(self, collector):
        collector.add_new_book('Горе от ума')
        collector.set_book_genre('Горе от ума', 'Комедии')
        result = collector.get_books_with_specific_genre('Комедии')
        assert 'Горе от ума' in result
        assert isinstance(result, list) and len(result) == 1

    @pytest.mark.parametrize("book_name, genre", [
        ("1984", "Фантастика"),
        ("It", "Ужасы"),
        ("Шерлок Холмс", "Детективы"),
        ("Убийство на улице Морг", "Детективы")
    ])
    def test_get_books_genre_valid_book_and_genre(self, collector, book_name, genre):
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        books_genre = collector.get_books_genre()
        assert book_name in books_genre
        assert books_genre[book_name] == genre

    @pytest.mark.parametrize("book_name, genre, should_be_included", [
        ("Маша и медведь", "Мультфильмы", True),
        ("Смех сквозь слёзы", "Комедии", True),
        ("Оно", "Ужасы", False),
        ("Шерлок Холмс", "Детективы", False),
    ])
    def test_get_books_for_children_filters_correctly(self, collector, book_name, genre, should_be_included):
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        result = collector.get_books_for_children()
        if should_be_included:
            assert book_name in result
        else:
            assert book_name not in result


    @pytest.mark.parametrize("book_name, genre", [
        ("1984", "Фантастика"),
        ("Шрек", "Мультфильмы"),
    ])
    def test_add_book_in_favorites_adds_only_once(self, collector, book_name, genre):
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        collector.add_book_in_favorites(book_name)
        collector.add_book_in_favorites(book_name)  # повторно
        favorites = collector.get_list_of_favorites_books()
        assert favorites.count(book_name) == 1


    @pytest.mark.parametrize("invalid_name", [
        "Неизвестная книга",
        "Призрак",
        "Тень прошлого"
    ])
    def test_add_book_in_favorites_does_not_add_if_not_exists(self, collector, invalid_name):
        collector.add_book_in_favorites(invalid_name)
        assert invalid_name not in collector.get_list_of_favorites_books()


    @pytest.mark.parametrize("book_name, genre", [
        ("Гарри Поттер", "Фантастика"),
        ("Три кота", "Мультфильмы"),
    ])
    def test_delete_book_from_favorites_removes_correctly(self, collector, book_name, genre):
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        collector.add_book_in_favorites(book_name)
        collector.delete_book_from_favorites(book_name)
        assert book_name not in collector.get_list_of_favorites_books()


    @pytest.mark.parametrize("book_name", [
        "Песнь льда и пламени",
        "Преступление и наказание",
    ])
    def test_delete_book_from_favorites_does_nothing_if_not_in_list(self, collector, book_name):
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, "Фантастика")
        collector.delete_book_from_favorites(book_name)  # не добавляли в избранное
        assert collector.get_list_of_favorites_books() == []


    def test_get_list_of_favorites_books_returns_current_list(self, collector):
        books = [
            ("Книга 1", "Фантастика"),
            ("Книга 2", "Комедии"),
        ]
        for name, genre in books:
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)
            collector.add_book_in_favorites(name)
        favorites = collector.get_list_of_favorites_books()
        assert set(favorites) == {"Книга 1", "Книга 2"}




