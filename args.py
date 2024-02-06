assert __name__ != "__main__"

import argparse
import logging

INPUT_FILE: str = None
OUTPUT_FILE: str = None

def _arg_parse():
    global INPUT_FILE
    global OUTPUT_FILE

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, required=False, default="-", help="Path to the input ELF file (- means stdin)")
    parser.add_argument("--output", "-o", type=str, required=False, default="-", help="Path to the output file (- means stdout)")
    parser.add_argument("--loglevel", type=str, required=False, default="INFO", help="Logging level")
    
    args = parser.parse_args()
    INPUT_FILE = str(args.input)
    OUTPUT_FILE = str(args.output)

    loglevel = getattr(logging, args.loglevel.upper())
    logging.basicConfig(level=loglevel)

_arg_parse()