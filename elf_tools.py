from dataclasses import dataclass
from enum import Enum

@dataclass
class ELFFlags:
    SHF_WRITE: bool
    SHF_ALLOC: bool
    SHF_EXECINSTR: bool
    SHF_MASKPROG: bool

def decode_flags(flags: int) -> ELFFlags:
    return ELFFlags(
        SHF_WRITE = (flags & 0x01) > 0,
        SHF_ALLOC =  (flags & 0x02) > 0,
        SHF_EXECINSTR = (flags & 0x04) > 0,
        SHF_MASKPROG = (flags & 0xf0000000) > 0 
    )
