from src.domain.checkout_history import CheckoutHistory
from src.repositories.checkout_history_protocol import CheckoutHistoryRepositoryProtocol
import json

class CheckoutHistoryRepository(CheckoutHistoryRepositoryProtocol):
    def __init__(self, filepath: str="checkout_history.json"):
        self.filepath = filepath
    
    def get_checkout_history_all(self) -> list[CheckoutHistory]:
        with open(self.filepath, 'r', encoding = 'utf-8') as f:
            data = json.load(f)
        return [CheckoutHistory.from_dict(item) for item in data]
    
    def add_record(self, record: CheckoutHistory) -> str:
        checkout_histories = self.get_checkout_history_all()
        checkout_histories.append(record)
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([c.to_dict() for c in checkout_histories], f, indent = 2)
        return record.checkout_id
    
    def get_history_for_book(self, book_id: str) -> list[CheckoutHistory]:
        histories = self.get_checkout_history_all()

        filtered = [h for h in histories if h.book_id == book_id]

        filtered.sort(key=lambda h: h.checkout_date)
        return filtered
    
    def add_seed_records(self, records: list[CheckoutHistory]) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in records], f, indent=2)