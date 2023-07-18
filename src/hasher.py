def encode(string: str):
    return f"{string}.hashed"


def decode(string: str):
    return f"{string.split('.')[0]}"
