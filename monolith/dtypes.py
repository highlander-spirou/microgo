from typing import TypeAlias, Tuple, TypedDict

class status_text(TypedDict):
    message: str


class Error:
    pass

# API return that can directly return by flask
api_response: TypeAlias = Tuple[status_text, int]

# Internal returns thats always return a 200 status code
internal_response: TypeAlias = Tuple[any, int]
