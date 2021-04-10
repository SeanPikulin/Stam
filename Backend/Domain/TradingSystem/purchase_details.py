import datetime
from dataclasses import dataclass

from typing import List


@dataclass
class PurchaseDetails:
    user_name: str
    store_name: str
    product_names: List[str]
    date: datetime
    total_price: float
