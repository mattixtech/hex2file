"""
hex2file_test.py
Matthew Brooks, 2018

Unit test for 'hex2file'.
"""
from functools import wraps

import binascii
import os
import tempfile
import unittest

import hex2file


def _check_output_file(func):
    """
    A decorator which verifies the output file(s) contains the correct content.

    :param func: the function to wrap via decorator
    :return: the wrapped function
    """

    @wraps(func)
    def _wrapper(self, *args, **kwargs):
        # Setup some temp files
        self.output_file = tempfile.NamedTemporaryFile(mode="w", delete=False)
        self.append_file = tempfile.NamedTemporaryFile(mode="w", delete=False)
        # Call the actual test function
        func(self, *args, **kwargs)
        self.output_file.close()
        self.append_file.close()

        # Verify the regular write
        with open(self.output_file.name, "rb") as f:
            hex_data = f.read()

        self.assertEqual(binascii.unhexlify(self.valid_hex_data_str), hex_data)

        # Verify the append
        with open(self.append_file.name, "rb") as f:
            hex_data = f.read()

        self.assertEqual(
            binascii.unhexlify(self.valid_hex_data_str * self.append_repeat),
            hex_data)

        # Remove the temp files
        os.unlink(self.output_file.name)
        os.unlink(self.append_file.name)

    return _wrapper


class TestHex2File(unittest.TestCase):
    """
    Tests the hex2file module.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up before any tests are executed.

        :return: None
        """

        cls.append_repeat = 5
        cls.invalid_hex_str = "0x00FF00FZ"
        cls.hex_str_to_filter = """
            # Begin
            0x00FF00FF,
            0xFF00FF00,
            // Middle
            0xAABBCCDD,
            0x00000000,
            0x12345678,
            #0xAABBCCDD,
            /* End */
            """
        cls.valid_hex_str = """
            0x00FF00FF
            0xFF00FF00
            0xAABBCCDD
            0x00000000
            0x12345678
            """
        cls.valid_hex_data_str = ""

        for line in cls.valid_hex_str.splitlines():
            hex_line = hex2file._sanitize(line)

            if hex_line:
                cls.valid_hex_data_str += hex_line

    @_check_output_file
    def test_write_str(self):
        """
        Tests hex2file.write_str.

        The implementation tested here is deprecated.

        :return: None
        """

        # Regular write
        hex2file.write_str(self.valid_hex_str, self.output_file.name)

        # Append
        for _ in range(self.append_repeat):
            hex2file.write_str(self.valid_hex_str, self.append_file.name,
                               append=True)

    @_check_output_file
    def test_write_from_file(self):
        """
        Tests hex2file.write_from_file.

        The implementation tested here is deprecated.

        :return: None
        """

        # Regular write
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as input_file:
            input_file.write(self.valid_hex_str)

        hex2file.write_from_file(input_file.name, self.output_file.name)

        # Append
        for _ in range(self.append_repeat):
            hex2file.write_from_file(input_file.name, self.append_file.name,
                                     append=True)

        os.unlink(input_file.name)

    def test_invalid_input(self):
        """
        Test the case where we try to write invalid hex.

        :return: None
        """

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            with self.assertRaises(ValueError):
                hex2file.write(self.invalid_hex_str, f.name)

        self.assertEqual(0, os.stat(f.name).st_size)
        f.close()
        os.unlink(f.name)

    @_check_output_file
    def test_filtering(self):
        """
        Tests write() with comment_strings and ignore_strings set.

        :return: None
        """

        # Regular write
        hex2file.write(self.hex_str_to_filter, self.output_file.name,
                       comment_strings=("#", "/*", "//"), ignore_strings=(",",))
        # Append
        for _ in range(self.append_repeat):
            hex2file.write(self.hex_str_to_filter, self.append_file.name,
                           append=True, comment_strings=("#", "/*", "//"),
                           ignore_strings=(",",))


if __name__ == '__main__':
    unittest.main()
