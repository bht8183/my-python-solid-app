import pytest
import src.services.book_service as book_service
from tests.mocks.mock_book_repository import MockBookRepo
from src.domain.book import Book

def test_get_all_books_positive():
    # AAA - arrange, act, assert
    repo = MockBookRepo()
    svc = book_service.BookService(repo)

    books = svc.get_all_books()

    assert len(books) == 2 # Assert

def test_find_book_name_negative():
    name = 2 # not a string
    repo = MockBookRepo()
    svc = book_service.BookService(repo)

    with pytest.raises(TypeError) as e:
        book = svc.find_book_by_name(name)

    assert str(e.value) == 'Expected str, got something else.' # Assert

def test_delete_book_by_name_positive():
    repo = MockBookRepo()
    svc = book_service.BookService(repo)

    deleted = svc.delete_book_by_name("test")
    
    assert deleted is True # Assert

def test_delete_book_by_name_negative_not_found():
    repo = MockBookRepo()
    svc = book_service.BookService(repo)

    deleted = svc.delete_book_by_name("not_exist")

    assert deleted is False # Assert

def test_update_book_positive():
    repo = MockBookRepo()
    svc = book_service.BookService(repo)

    updated = Book(book_id= "1", title="updated-title", author="updated-author")

    ok = svc.update_book("1", updated)

    assert ok is True # Assert
    books = svc.get_all_books()
    match = next(b for b in books if b.book_id == "1")
    assert match.title == "updated-title"  # check val was 
    
def test_update_book_negative_not_found():
    repo = MockBookRepo()
    svc = book_service.BookService(repo)

    updated = Book( title="x", author="y")

    ok = svc.update_book("999", updated)

    assert ok is False # Assert