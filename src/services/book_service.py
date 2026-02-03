from src.repositories.book_repository_protocol import BookRepositoryProtocol
from src.domain.book import Book

class BookService:
    def __init__(self, repo: BookRepositoryProtocol):
        self.repo = repo

    def get_all_books(self) -> list[Book]:
        return self.repo.get_all_books()

    def add_book(self, book:Book) -> str:
        return self.repo.add_book(book)

    def find_book_by_name(self, query:str) -> list[Book]:
        if not isinstance(query, str):
            raise TypeError('Expected str, got something else.')
        return self.repo.find_book_by_name(query)

    def delete_book_by_name(self, book_id: str) -> bool:
        return self.repo.delete_book_by_name(book_id)

    def update_book(self, old_id: str, updated: Book) -> bool:
        return self.repo.update_book(old_id, updated)