from typing import Protocol
from src.domain.book import Book

class BookRepositoryProtocol(Protocol):
    def get_all_books(self) -> list[Book]:
        ...

    def add_book(self, book:Book) -> str:
        ...

    def find_book_by_name(self, query:str) -> list[Book]:
        ...

    def delete_book_by_name(self, book_id: str) -> bool:
        ...

    def update_book(self, old_id: str, updated: Book) -> bool:
        ...

    def check_out_book(self, book_id: str) -> Book:
        ...
    
    def check_in_book(self, book_id: str) -> Book:
        ...

    def add_seed_records(self, books: list[Book]) -> None:
        ...
