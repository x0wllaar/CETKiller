import logging

import consts
from custom_types import BadInstruction

_logger = logging.getLogger(__name__)

def nop_patch(buf: bytearray, base_file_offset: int, inst: BadInstruction):
    base_file_start = base_file_offset + inst.start_offset
    base_file_end = base_file_offset + inst.end_offset
    _logger.debug(f"Patching {inst.length}-byte instruction {inst.short_mnemonic} at {base_file_start:#x} in file")

    assert (base_file_end - base_file_start) == inst.length
    assert bytes(buf[base_file_start:base_file_end]) == inst.exact_bytes

    nop_replacement = bytes([consts.NOP_OPCODE] * inst.length)
    buf[base_file_start:base_file_end] = nop_replacement