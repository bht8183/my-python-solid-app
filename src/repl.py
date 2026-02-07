from src.services.book_generator_service_V2 import generate_books_json
from src.services.book_generator_bad_data_service import generate_books_dirty as get_bad_books

from src.services.checkout_history_generator_service import generate_checkout_history_json
from src.domain.book import Book
from src.services.book_service import BookService
from src.services.checkout_history_service import CheckoutHistoryService
from src.repositories.book_repository import BookRepository
from src.repositories.checkout_history_repo import CheckoutHistoryRepository
from src.services.book_analytics_sevices import BookAnalyticsService
import requests

class BookREPL:
    def __init__(self, book_svc, book_analytics_svc,checkout_svc):
        self.running = True
        self.book_svc = book_svc
        self.book_analytics_svc = book_analytics_svc
        self.checkout_svc = checkout_svc


    def start(self):
        print('Welcome to the book app! Type \'Help\' for a list of commands!')
        while self.running:
            cmd = input('>>>').strip()
            self.handle_command(cmd)

    def handle_command(self, cmd):
        if cmd == 'exit':
            self.running = False
            print('Goodbye!')
        elif cmd == 'getAllRecords':
            self.get_all_records()
        elif cmd == 'addBook':
            self.add_book()
        elif cmd == 'findByName':
            self.find_book_by_name()
        elif cmd == 'getJoke':
            self.get_joke()
        elif cmd == 'deleteBook':
            self.delete_book()
        elif cmd == 'updateBook':
            self.update_book()

        elif cmd == 'getAveragePrice':
            self.get_average_price()
        elif cmd == 'getTopBooks':
            self.get_top_books()
        elif cmd == 'getValueScores':
            self.get_value_scores()

        elif cmd == "checkoutBook":
            self.check_out_book()
        elif cmd == "checkinBook":
            self.check_in_book()
        elif cmd == "getCheckoutHistory":
            self.get_checkout_history_for_book()
        elif cmd == "getCheckoutHistoryall":
            self.get_checkout_history_all()
        
        elif cmd == 'help':
            print('Available commands: addBook, getAllRecords, findByName, getJoke, deleteBook, updateBook, checkOutBook, checkInBook, getCheckoutHistory, getCheckoutHistoryAll, getAveragePrice, getTopBooks, getValueScores, help, exit')
        else:
            print('Please use a valid command!')

    def get_average_price(self):
        books = self.book_svc.get_all_books()
        avg_price = self.book_analytics_svc.average_price(books)
        print(avg_price)

    def get_top_books(self):
        books = self.book_svc.get_all_books()
        top_rated_books = self.book_analytics_svc.top_rated_with_pandas(books)
        print(top_rated_books)

    def get_value_scores(self):
        books = self.book_svc.get_all_books()
        value_scores = self.book_analytics_svc.value_scores_with_pandas(books)
        print(value_scores)

    def get_joke(self):
        try:
            url = 'https://api.chucknorris.io/jokes/random'
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            print(response.json()['value'])
        except requests.exceptions.Timeout:
            print('Request timed out.')
        except requests.exceptions.HTTPError as e:
            print(f'HTTP Error: {e}')
        except requests.exceptions.RequestException as e:
            print(f'Something else went wrong: {e}')

    def find_book_by_name(self):
        query = input('Please enter book name: ')
        books = self.book_svc.find_book_by_name(query)
        print(books)

    def get_all_records(self):
        books = self.book_svc.get_all_books()
        print(books)

    def add_book(self):
        try:
            print('Enter Book Details:')
            title = input('Title: ')
            author = input('Author: ')
            book = Book(title= title, author=author)
            new_book_id = self.book_svc.add_book(book)
            print(new_book_id)
        except Exception as e:
            print(f'An unexpected error has occurred: {e}')
        
    def delete_book(self):
        try:
            print('Enter Book name:')
            name = input('Book name: ')

            matches = self.book_svc.find_book_by_name(name)
            if not matches:
                print("book not found lol")
                return

            book = matches[0] 
            result = self.book_svc.delete_book_by_name(book.book_id) 
            if result:
                print(f'book {book.book_id} has been deleted')
            else:
                print("uhhhhhhhhhh")
        except Exception as e:
            print(f'An unexpected error has occurred: {e}')
    
    def update_book(self):
        try:
            book_id = input("Book ID to update: ").strip()

            title = input("New title: ").strip()
            author = input("New author: ").strip()

            new_book = Book(book_id=book_id, title=title, author=author)

            updated = self.book_svc.update_book(book_id,new_book)

            if updated:
                print("book updated")
        
        except Exception as e:
            print(f'An unexpected error has occurred: {e}')


    
    def check_out_book(self):
        try:
            book_id = input("Book ID to check out: ").strip()
            email = input("Leave an email for the checkout: ").strip()
            checkout_id = self.checkout_svc.check_out_book(book_id,email)
            print(f"Checked out! checkout_id={checkout_id}")
        except Exception as e:
            print(f"Checkout failed: {e}")

    def check_in_book(self):
        try:
            book_id = input("Book ID to check in: ").strip()
            checkout_id = self.checkout_svc.check_in_book(book_id)
            print(f"Checked in! closed checkout_id={checkout_id}")
        except Exception as e:
            print(f"Check-in failed: {e}")

    def get_checkout_history_for_book(self):
        try:
            book_id = input("Book ID to view history: ").strip()
            history = self.checkout_svc.get_checkout_history(book_id)
            if not history:
                print("No history for this book.")
                return
            for h in history:
                print(h)
        except Exception as e:
            print(f"Could not fetch history: {e}")

    def get_checkout_history_all(self):
        try:
            history = self.checkout_svc.get_checkout_history_all()
            print(f"Total history records: {len(history)}")
            for h in history[:25]:
                print(h)
            if len(history) > 25:
                print("... (showing first 25)")
        except Exception as e:
            print(f"Could not fetch history: {e}")





if __name__ == '__main__':
    generate_books_json()
    get_bad_books()
    generate_checkout_history_json(seed=14)
    repo = BookRepository('books.json')
    check_repo = CheckoutHistoryRepository('checkout_history.json')
    book_service = BookService(repo)
    book_analytics_service = BookAnalyticsService()
    checkout_service = CheckoutHistoryService(repo,check_repo)
    repl = BookREPL(book_service, book_analytics_service, checkout_service)
    repl.start()
