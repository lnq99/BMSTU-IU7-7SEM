def int_to_bin_str(n: int, size: int = 0) -> str:
    res = bin(n)[2:]
    if size:
        res = f'{res:0>{size}}'
    return res


def int_to_hex_str(n: int, size: int = 0) -> str:
    res = hex(n)[2:]
    if size:
        res = f'{res:0>{size}}'
    return res


def int_to_ascii(n: int):
    return bytearray.fromhex(hex(n)[2:]).decode()


def rotate_left(n: int, rotation: int, size: int) -> int:
    head = n >> (size - rotation)
    return (n << rotation) - (head << size) + head


def permute(n: int, sequence: list, size: int) -> int:
    shift = [size - i for i in sequence]
    res = 0
    for i in shift:
        res <<= 1
        res += n >> i & 1
    return res
