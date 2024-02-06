import logging
import sys
import io


import elftools.elf.elffile
import elftools.elf.sections

import args
import asm_analyzer
import file_ops
import elf_tools
import exceptions
import nop_patcher

_logger = logging.getLogger(__name__)

def main():
    with file_ops.binary_open_file(args.INPUT_FILE, "rb") as input_f:
        input_file_bytes = input_f.read()

    mutable_file_bytes = bytearray(input_file_bytes)
    
    elf = elftools.elf.elffile.ELFFile(io.BytesIO(input_file_bytes))
    
    arch = elf.header["e_machine"]
    if (arch != "EM_386") and (arch != "EM_X86_64"):
        _logger.error("Only x86 32-bit and 64-bit ELFs supported")
        raise exceptions.UnsupportedELFFile("Only x86 32-bit and 64-bit ELFs supported")
    if arch == "EM_X86_64":
        _logger.warn("x86-64 is experimental and not fully supported")

    n_patched = 0
    for sect in elf.iter_sections():
        s_n_patched = 0
        flags = elf_tools.decode_flags(sect.header.sh_flags)
        if not flags.SHF_EXECINSTR:
            _logger.debug(f"Skipping non-executable section {sect.name}")
            continue
        sect_addr = sect.header["sh_addr"]
        sect_offset = sect.header["sh_offset"]
        _logger.info(f"Processing executable section {sect.name}, address {sect_addr:#x}")
        if sect.compressed:
            _logger.error("Compressed sections are not supported")
            raise exceptions.UnsupportedELFFile("Compressed sections are not supported")

        assert sect.data_size == sect.header["sh_size"]
        sect_bytes = sect.data()
        assert len(sect_bytes) == sect.header["sh_size"]

        for bi in asm_analyzer.analyze_section_code(sect_bytes, sect_addr, 32 if arch == "EM_386" else 64):
            nop_patcher.nop_patch(mutable_file_bytes, sect_offset, bi)
            s_n_patched += 1
        _logger.info(f"{s_n_patched} instructions patched in section {sect.name}")
        n_patched += s_n_patched

    with file_ops.binary_open_file(args.OUTPUT_FILE, "wb") as output_f:
        output_f.write(bytes(mutable_file_bytes)) 

    _logger.info(f"{n_patched} instructions patched in file")

if __name__ == "__main__":
    main()