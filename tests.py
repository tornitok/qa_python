import pytest

from conftest import collector
from main import BooksCollector


class TestBooksCollector:

    def test_add_new_book_one_book_added(self, collector):
        collector.add_new_book('Алиса в Стране Чудес')
        genre = collector.get_book_genre('Алиса в Стране Чудес')
        assert genre == ''

    @pytest.mark.parametrize("book_name, genre", [
        ("1984", "Фантастика"),
        ("It", "Ужасы"),
        ("Шерлок Холмс", "Детективы"),
    ])
    def test_set_book_genre_valid_book_and_genre(self, collector, book_name, genre):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.books_genre[book_name] == genre

    @pytest.mark.parametrize("book_name, invalid_genre", [
        ("Dracula", "Романтика"),
        ("Tom & Jerry", "Приключения"),
    ])
    def test_set_book_genre_invalid_genre(self, collector, book_name, invalid_genre):
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, invalid_genre)
        assert collector.books_genre[book_name] == ""

    def test_get_book_genre_valid_book_and_genre(self, collector):
        collector.add_new_book('Горе от ума')
        collector.set_book_genre('Горе от ума', 'Комедии')
        assert collector.get_book_genre('Горе от ума') == 'Комедии'

    def test_get_books_with_specific_genre_filters_correctly(self, collector):
        collector.add_new_book('Горе от ума')
        collector.set_book_genre('Горе от ума', 'Комедии')

        collector.add_new_book('Война и мир')
        collector.set_book_genre('Война и мир', 'Романы')

        collector.add_new_book('1984')
        collector.set_book_genre('1984', 'Фантастика')

        result = collector.get_books_with_specific_genre('Комедии')
        assert result == ['Горе от ума']
        assert 'Война и мир' not in result
        assert '1984' not in result

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

    def test_get_books_for_children_includes_cartoon(self, collector):
        collector.add_new_book("Маша и медведь")
        collector.set_book_genre("Маша и медведь", "Мультфильмы")
        result = collector.get_books_for_children()
        assert "Маша и медведь" in result

    def test_get_books_for_children_includes_comedy(self, collector):
        collector.add_new_book("Смех сквозь слёзы")
        collector.set_book_genre("Смех сквозь слёзы", "Комедии")
        result = collector.get_books_for_children()
        assert "Смех сквозь слёзы" in result

    def test_get_books_for_children_excludes_horror(self, collector):
        collector.add_new_book("Оно")
        collector.set_book_genre("Оно", "Ужасы")
        result = collector.get_books_for_children()
        assert "Оно" not in result

    def test_get_books_for_children_excludes_detective(self, collector):
        collector.add_new_book("Шерлок Холмс")
        collector.set_book_genre("Шерлок Холмс", "Детективы")
        result = collector.get_books_for_children()
        assert "Шерлок Холмс" not in result

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
        collector.add_new_book("Книга 1")
        collector.set_book_genre("Книга 1", "Фантастика")
        collector.add_book_in_favorites("Книга 1")

        collector.add_new_book("Книга 2")
        collector.set_book_genre("Книга 2", "Комедии")
        collector.add_book_in_favorites("Книга 2")

        favorites = collector.get_list_of_favorites_books()
        assert favorites == ["Книга 1", "Книга 2"]
