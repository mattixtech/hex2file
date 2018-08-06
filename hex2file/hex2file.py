"""
hex2file.py
Matthew Brooks, 2018

Utility for writing hex to a file.
"""
import argparse
import binascii
import deprecation
import sys


def _sanitize(hex_str, comment_strings=None, ignore_strings=None):
    """
    Sanitize string input before attempting to write to file.

    :param hex_str: the string input to sanitize
    :param comment_strings:  a tuple of strings identifying comment characters
    :param ignore_strings:  a tuple of strings to ignore in the input
    :return: the sanitized string or None
    """

    # Remove whitespace
    hex_str = hex_str.strip()

    if not hex_str:
        return None

    # Ignore lines beginning with a comment string and any content after a
    # comment string
    if comment_strings:
        for comment_string in comment_strings:
            if hex_str.startswith(comment_string):
                return None
            else:
                hex_str = hex_str.split(comment_string)[0]

    hex_id = "0x"

    # Ignore strings
    if ignore_strings:
        ignore_strings += (hex_id,)
    else:
        ignore_strings = (hex_id,)

    for string_to_remove in ignore_strings:
        hex_str = hex_str.replace(string_to_remove, "")

    return "".join(hex_str.split())


def _str2hexbin(hex_str):
    """
    Converts a hex string to hex binary.

    :param hex_str: the string to convert
    :return: the string converted to hex or None if we were passed an empty
    string
    """

    if hex_str:
        try:
            int(hex_str, 16)
        except (TypeError, ValueError):
            raise ValueError("Invalid hex input '{}'".format(hex_str))

        return binascii.unhexlify(hex_str)


def write(hex_input, file_path, append=False, comment_strings=None,
          ignore_strings=None, from_file=False):
    """
    Write a hex string to a file as hex.

    :param hex_input: the string containing the hex or the file containing the
    hex if 'from_file' is set
    :param file_path: the path to the file to write
    :param append:  whether to append or overwrite
    :param comment_strings:  a tuple of strings identifying comment characters
    :param ignore_strings:  a tuple of strings to ignore in the input
    :param from_file:  specifies to read from the given file rather than a
    string
    :return: None
    """

    if hex_input is not None:
        if append:
            mode = "a"
        else:
            mode = "w"

        mode += "b"

        if from_file:
            # TODO: Should we check for exceptions here?
            with open(hex_input, 'r') as input_file:
                hex_input = input_file.read()

        with open(file_path, mode) as f:
            for line in iter(hex_input.splitlines()):
                hexbin_line = _str2hexbin(
                    _sanitize(line, comment_strings=comment_strings,
                              ignore_strings=ignore_strings))
                if hexbin_line:
                    f.write(hexbin_line)


@deprecation.deprecated(deprecated_in="1.1.0",
                        details="Use the write() function instead")
def write_str(hex_input, file_path, append=False):
    """
    Write a hex string to a file as hex.

    :param hex_input: the string containing the hex or the file containing the
    hex if 'from_file' is set
    :param file_path: the path to the file to write
    :param append:  whether to append or overwrite
    :return: None
    """

    write(hex_input, file_path, append)


@deprecation.deprecated(deprecated_in="1.1.0",
                        details="Use the write() function instead and set"
                                " 'from_file'")
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
        write(input_file.read(), file_path, append=append)


def _parse_arguments():
    """
    Parse the command line arguments.

    :return: the parsed arguments
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--append",
                        help="Append to the file rather than overwrite it.",
                        action="store_true")
    parser.add_argument("-c", "--comments",
                        help="Ignore lines starting with any of the supplied"
                             " comment strings (space separated) and any"
                             " content preceded by any of those strings")
    parser.add_argument("-f", "--file",
                        help="Get the hex contents from the specified file")
    parser.add_argument("-i", "--ignore",
                        help="Ignore any of the given strings (space separated)"
                             " in the input")
    parser.add_argument("output_path",
                        help="The path to the output file to write hex to.")

    return parser.parse_args()


def _cmd_line():
    """
    Writes hex from a file or from stdin.

    :return: None
    """

    append = False
    from_file = False
    parsed_args = _parse_arguments()

    # Check if we are copying from a file
    if parsed_args.file:
        hex_input = parsed_args.file
        from_file = True
    # Check if stdin has anything for us
    elif not sys.stdin.isatty():
        hex_input = sys.stdin.read()
    else:
        sys.stderr.write("ERROR: No input provided via stdin\n")
        sys.exit(1)

    if parsed_args.append:
        append = True

    # Convert the comments strings into a tuple
    if parsed_args.comments:
        parsed_args.comments = tuple(parsed_args.comments.split())

    # Convert the ignore strings into a tuple
    if parsed_args.ignore:
        parsed_args.ignore = tuple(parsed_args.ignore.split())

    try:
        write(hex_input, parsed_args.output_path, append=append,
              comment_strings=parsed_args.comments,
              ignore_strings=parsed_args.ignore, from_file=from_file)
    except ValueError as e:
        sys.stderr.write("ERROR: {}\n".format(e))
        sys.exit(1)
    except IOError as e:
        sys.stderr.write(
            "ERROR: {} '{}'\n".format("".join(e.args[1:]), e.filename))
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    _cmd_line()
