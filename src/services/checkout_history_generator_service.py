import json
import uuid
import random
from datetime import datetime, timedelta, timezone

def generate_checkout_history_json(
    books_filename: str = "books.json",
    history_filename: str = "checkout_history.json",
    # setting up some vals for the list
    max_records_per_book: int = 5,
    checkout_period_days: int = 180,
    checkout_length_days_range: tuple[int, int] = (1, 28),
    due_days: int = 14,
                ) -> None:
    
    rng = random.Random()
    now = datetime.now(timezone.utc)
    start_window = now - timedelta(days=checkout_period_days)

    # Load books
    with open(books_filename, "r", encoding="utf-8") as f:
        books = json.load(f)

    history: list[dict] = []
    email_counter = 1 

    for book in books:
        book_id = book["book_id"]
        available = bool(book.get("available", True))

        record_count = rng.randint(0, max_records_per_book)
        if record_count == 0:
            continue

        # Create  checkout dates
        # Start random points, then add gaps
        checkout_date = start_window + timedelta(
            days=rng.randint(0, checkout_period_days - 1),
            seconds=rng.randint(0, 86399),
        )

        records_for_book: list[dict] = []

        for _ in range(record_count):
            # Ensure checkouts in chronological order
            gap_days = rng.randint(3, 30)
            checkout_date = checkout_date + timedelta(days=gap_days, seconds=rng.randint(0, 20000))
            if checkout_date > now:
                checkout_date = now - timedelta(days=rng.randint(0, 7))

            due_date = checkout_date + timedelta(days=due_days)

            # mostly returned records
            returned = rng.choice([True, True, True, False]) 
            return_date = None
            if returned:
                length_days = rng.randint(*checkout_length_days_range)
                return_date = min(checkout_date + timedelta(days=length_days), now)
            
            email = f"email_{email_counter}@gmail.com"
            email_counter += 1


            records_for_book.append(
                {
                    "checkout_id": str(uuid.uuid4()),
                    "book_id": book_id,
                    "checkout_date": checkout_date.isoformat(),
                    "return_date": return_date.isoformat() if return_date else None,
                    "due_date": due_date.isoformat(),
                    "returned": returned,
                    "email": email, # added email for the strech goal but never implemented the return funciton sorry
                }
            )

        # check book list
        # If book is available then last record returned
        # If book is unavailable then last record NOT returned
        if records_for_book:
            last = records_for_book[-1]
            if available:
                # force returned
                if last["returned"] is False:
                    last["returned"] = True
                    # set a return_date
                    last_checkout_dt = datetime.fromisoformat(last["checkout_date"])
                    last["return_date"] = min(last_checkout_dt + timedelta(days=rng.randint(1, 21)), now).isoformat()
            else:
                # force active checkout
                last["returned"] = False
                last["return_date"] = None

        history.extend(records_for_book)

    # Sort by checkout_date
    history.sort(key=lambda r: r["checkout_date"])

    with open(history_filename, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)
