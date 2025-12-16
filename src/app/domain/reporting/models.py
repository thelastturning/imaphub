import msgspec

class SearchTermRow(msgspec.Struct):
    search_term: str
    status: str
    keyword: str
    clicks: int
    impressions: int
    cost_micros: int
    conversions: float
