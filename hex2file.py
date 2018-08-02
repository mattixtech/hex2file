#!/usr/bin/env python
"""
hex2file.py
Matthew Brooks, 2018

Utility for writing hex to a file.
"""
import argparse
import binascii
import sys


def _sanitize(hex_str):
    """
    Sanitize string input before attempting to write to file.

    :param hex_str: the string input to sanitize
    :return: the sanitized string
    """

    return "".join(hex_str.replace("0x", "").split())


def _str2hexbin(hex_str):
    """
    Converts a hex string to hex binary.

    :param hex_str: the string to convert
    :return: the string converted to hex or None if we were passed an empty
    string
    """

    hex_str = hex_str.strip()

    if not hex_str:
        return None

    sanitized_line = _sanitize(hex_str)

    try:
        int(sanitized_line, 16)
    except (TypeError, ValueError):
        raise ValueError("Invalid hex input '{}'".format(sanitized_line))

    return binascii.unhexlify(sanitized_line)


def write_str(hex_str, file_path, append=False):
    """
    Write a hex string to a file as hex.

    :param hex_str: the string containing the hex
    :param file_path: the path to the file to write
    :param append:  whether to append or overwrite
    :return: None
    """

    if hex_str is not None:
        if append:
            mode = "a"
        else:
            mode = "w"

        mode += "b"

        with open(file_path, mode) as f:
            for line in iter(hex_str.splitlines()):
                hexbin_line = _str2hexbin(line)
                if hexbin_line:
                    f.write(hexbin_line)


def write_from_file(text_file_path, file_path, append=False):
    """
    Writes the hex (in ascii format) contained in the given file to the given
    output file path.

    :param text_file_path: the path to the input file
    :param file_path: the path to the file to write
    :param append: whether to append or overwrite
    :return: None
    """

    with open(text_file_path, 'r') as input_file:
        write_str(input_file.read(), file_path, append)


def parse_arguments():
    """
    Parse the command line arguments.

    :return: the parsed arguments
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--append",
                        help="Append to the file rather than overwrite.",
                        action="store_true")
    parser.add_argument("output_path",
                        help="The path to the output file to write hex to.")

    return parser.parse_args()


def main():
    """
    When ran directly, accepts input via stdin and converts that to hex in a
    file provided as arg1.

    :return: None
    """

    # Check if stdin has anything for us
    if not sys.stdin.isatty():
        stdin_input = sys.stdin.read()
        parsed_args = parse_arguments()
        append = False

        if parsed_args.append:
            append = True

        write_str(stdin_input, parsed_args.output_path, append)
        sys.exit(0)
    else:
        sys.stderr.write("ERROR: Invalid input.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
