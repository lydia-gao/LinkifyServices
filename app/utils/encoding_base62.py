import string

ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase
BASE = 62

def to_base62(num: int) -> str:
    if num == 0:
        return ALPHABET[0]
    s = []
    while num:
        num, r = divmod(num, BASE)
        s.append(ALPHABET[r])
    return ''.join(reversed(s))

def from_base62(code: str) -> int:
    n = 0
    for ch in code:
        n = n * BASE + ALPHABET.index(ch)
    return n