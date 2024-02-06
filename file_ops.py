import contextlib
import sys
from typing import Generator, BinaryIO

@contextlib.contextmanager
def binary_open_file(path: str, mode: str = "rb") -> Generator[BinaryIO, None, None]:
    assert mode[-1] == "b"
    if path == "-":
        yield from _prepare_stdio(mode)
    else:
        yield from _prepare_file(path, mode)
        
def _prepare_file(path: str, mode: str) -> Generator[BinaryIO, None, None]:
    try:
        fl = open(path, mode)
        yield fl
    finally:
        fl.close()

def _prepare_stdio(mode: str) -> Generator[BinaryIO, None, None]:
    try:
        if mode.startswith("a") or mode.startswith("x") or mode.startswith("w"):
            yield sys.stdout.buffer
        else:
            yield sys.stdin.buffer
    finally:
        pass

