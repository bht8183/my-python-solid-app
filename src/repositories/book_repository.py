import json
from src.domain.book import Book
from src.repositories.book_repository_protocol import BookRepositoryProtocol

class BookRepository(BookRepositoryProtocol):
    def __init__(self, filepath: str="books.json"):
        self.filepath = filepath

    def get_all_books(self) -> list[Book]:
        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [Book.from_dict(item) for item in data]

    def add_book(self, book:Book) -> str:
        books = self.get_all_books()
        books.append(book)
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([b.to_dict() for b in books], f, indent=2)
        return book.book_id

    def find_book_by_name(self, query) -> Book:
        return [b for b in self.get_all_books() if b.title == query]
    

    def delete_book_by_name(self, book_id: str) -> bool:

        books = self.get_all_books()

        new_books = [b for b in books if b.book_id != book_id]

        if len(new_books) == len(books):
            return False
    
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([b.to_dict() for b in new_books], f, indent=2)

        return True

    def update_book(self, old_id: str, updated: Book) -> bool:
        
        books = self.get_all_books()
        counter = 0
        for book in books:
            if book.book_id == old_id:
                books[counter] = updated
                with open(self.filepath, 'w', encoding='utf-8') as f:
                    json.dump([b.to_dict() for b in books], f, indent=2)
                return True
            
            counter += 1
        return False
    
    def check_out_book(self, book_id: str) -> bool:
        books = self.get_all_books()

        for i, book in enumerate(books):
            if book.book_id == book_id:
                book.check_out()

                # Persist changes
                books[i] = book
                with open(self.filepath, "w", encoding="utf-8") as f:
                    json.dump([b.to_dict() for b in books], f, indent=2)

                return True

        # book not found lol
        return False
    
    def check_in_book(self, book_id: str) -> bool:
        books = self.get_all_books()

        for i, book in enumerate(books):
            if book.book_id == book_id:
      
                book.check_in()

                # Persist changes
                books[i] = book
                with open(self.filepath, "w", encoding="utf-8") as f:
                    json.dump([b.to_dict() for b in books], f, indent=2)

                return True

        return False