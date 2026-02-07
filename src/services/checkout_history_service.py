from src.repositories.checkout_history_protocol import CheckoutHistoryRepositoryProtocol
from src.repositories.book_repository_protocol import BookRepositoryProtocol
from src.domain.checkout_history import CheckoutHistory
import uuid

from datetime import datetime, timezone, timedelta

class CheckoutHistoryService:
    def __init__(self,
                 book_repo: BookRepositoryProtocol,
                 checkout_history_repo: CheckoutHistoryRepositoryProtocol):
        self.book_repo = book_repo
        self.checkout_history_repo = checkout_history_repo

    def add_seed_records(self, records: list[CheckoutHistory]) -> None:
        self.checkout_history_repo.add_seed_records(records)
    
    def get_checkout_history_all(self) -> list[CheckoutHistory]:
        return self.checkout_history_repo.get_checkout_history_all()
    
    def get_checkout_history(self, book_id: str) -> list[CheckoutHistory]:
        if not isinstance(book_id, str):
            raise TypeError('Expected str, got something else!')
        return self.checkout_history_repo.get_history_for_book(book_id)
    
    def check_out_book(self, book_id: str, user_email:str) -> str:
        if not isinstance(book_id, str):
            raise TypeError("Expected str, got something else!")

        # Mark book unavailable
        ok = self.book_repo.check_out_book(book_id)
        if ok is False:
            raise ValueError("Book not found or already checked out.")

        # Create a checkout record
        now = datetime.now(timezone.utc)
        record = CheckoutHistory(
            checkout_id=str(uuid.uuid4()),
            book_id=book_id,
            checkout_date=now,
            return_date=None,
            due_date= now+timedelta(days=14), # return in 14 dats
            returned=False,
            email= user_email
        )

        self.checkout_history_repo.add_record(record)
        return record.checkout_id
    
    def check_in_book(self, book_id: str) -> str:
        if not isinstance(book_id, str):
            raise TypeError("Expected str, got something else!")

        # mark book available
        ok = self.book_repo.check_in_book(book_id)
        if ok is False:
            raise ValueError("Book not found or already checked in.")

        # find recent checkout record
        all_history = self.checkout_history_repo.get_checkout_history_all()

        # if book not returned
        open_records = [h for h in all_history if h.book_id == book_id and h.returned is False]
        if not open_records:
            # book checked-in but history of checkout exists
            raise ValueError("No active checkout record found to close")

        # latest checkout_date
        open_records.sort(key=lambda h: h.checkout_date, reverse=True)
        active = open_records[0]

        # close checkout
        active.returned = True
        active.return_date = datetime.now(timezone.utc)

        # Persist changes
        self.checkout_history_repo.add_seed_records(all_history)

        return active.checkout_id