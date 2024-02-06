from collections import namedtuple

BadInstruction = namedtuple("BadInstruction", ("short_mnemonic", "exact_bytes", "start_offset", "end_offset", "length"))