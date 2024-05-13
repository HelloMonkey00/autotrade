from typing import List
from dataclasses import dataclass

@dataclass
class GetSnapshotsRequest:
    code_list: List[str]

@dataclass
class Snapshot:
    code: str
    last_price: float
    implied_volatility: float

@dataclass
class GetSnapshotsResponse:
    snapshots: List[Snapshot]