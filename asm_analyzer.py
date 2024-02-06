import logging
from typing import Generator

import iced_x86

import consts
import custom_types

_logger = logging.getLogger(__name__)


def analyze_section_code(sect_code: bytes, base_addr: int, bitness: int = 32) -> Generator[custom_types.BadInstruction, None, None]:
    _logger.info(f"Decoding {bitness}-bit section at {base_addr:#x}, size {len(sect_code)}")
    decoder = iced_x86.Decoder(bitness, sect_code, ip = base_addr)
    formatter = iced_x86.Formatter(iced_x86.FormatterSyntax.NASM)
    
    n_instr = 0
    n_patches = 0

    for instr in decoder:
        n_instr += 1
        mnemonic_check_str = formatter.format_mnemonic(instr, iced_x86.FormatMnemonicOptions.NO_PREFIXES).upper()
        if mnemonic_check_str not in consts.BAD_INSTRUCTIONS:
            continue
        
        full_mnemonic = formatter.format(instr)
        instr_start_offset = instr.ip - base_addr
        instr_end_offset = instr_start_offset + instr.len
        instr_bytes = sect_code[instr_start_offset:instr_end_offset]
        instr_bytes_str = instr_bytes.hex().upper()

        _logger.debug(f"Found bad instruction {mnemonic_check_str} (full: {full_mnemonic}) at offset {instr_start_offset:#x}, bytes {instr_bytes_str} ({instr.len} bytes long)")

        yield custom_types.BadInstruction(mnemonic_check_str, instr_bytes, instr_start_offset, instr_end_offset, instr.len)
        n_patches += 1
    
    _logger.info(f"Decoded {n_instr} instructrions, {n_patches} bad instructions found")