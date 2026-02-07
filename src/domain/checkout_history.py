from dataclasses import dataclass, field
import uuid
from datetime import datetime, timezone
from typing import Optional

@dataclass
class CheckoutHistory:
    checkout_id: str
    book_id: str
    checkout_date: datetime
    return_date: Optional[str] 
    due_date: datetime
    returned: bool
    email: str

    @classmethod
    def from_dict(cls, data: dict) -> "CheckoutHistory":
        return cls(
            checkout_id=data["checkout_id"],
            book_id=data["book_id"],
            checkout_date=datetime.fromisoformat(data["checkout_date"]),
            return_date=datetime.fromisoformat(data["return_date"]) if data.get("return_date") else None,
            due_date=datetime.fromisoformat(data["due_date"]),
            returned=bool(data["returned"]),
            email=data["email"],
        )

    def to_dict(self) -> dict:
        return {
            "checkout_id": self.checkout_id,
            "book_id": self.book_id,
            "checkout_date": self.checkout_date.isoformat(),
            "return_date": self.return_date.isoformat() if self.return_date else None,
            "due_date": self.due_date.isoformat(),
            "returned": self.returned,
            "email": self.email,
        }
    