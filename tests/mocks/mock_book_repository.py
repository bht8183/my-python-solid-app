from src.domain.book import Book

class MockBookRepo:

    def __init__(self) -> None:
        self._books: list[Book] = [
            Book(book_id="1", title="test", author="author"),
            Book(book_id="2", title="other", author="someone"),
        ]
    
    def get_all_books(self) -> list[Book]:
        return list(self._books)
    
    def add_book(self, book: Book) -> str:
        self._books.append(book)
        return book.book_id
    
    def find_book_by_name(self, query: str) -> list[Book]:
        return [b for b in self._books if b.title == query]

    def delete_book_by_name(self, query: str) -> bool:
        before = len(self._books) # how many books
        self._books = [b for b in self._books if b.title != query] # all books except the one for delete
        return len(self._books) != before # if num of books not change then delete fail
    
    def update_book(self, old_id: str, updated: Book) -> bool:
        for i, b in enumerate(self._books): # all books
            if b.book_id == old_id: # if you find book
                self._books[i] = updated # replace book
                return True 
        return False # book never found