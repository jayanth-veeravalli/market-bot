from pydantic import BaseModel
from datetime import date
from typing import Optional


class PutOption(BaseModel):
    symbol: str
    strike: float
    expiry: date
    bid: float
    ask: float
    midpoint: float
    delta: Optional[float] = None
    iv: Optional[float] = None


class OptionsResult(BaseModel):
    ticker: str
    current_price: float
    current_week: list[PutOption]
    next_week: list[PutOption]
    error: Optional[str] = None
