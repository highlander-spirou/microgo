from typing import TypeAlias, Tuple, TypedDict

class status_text(TypedDict):
    message: str
    
api_response: TypeAlias = Tuple[status_text, int]