"""
hexwriter_test.py
Matthew Brooks, 2018

Unit test for 'hex2file'.
"""
import os
import tempfile
import unittest

import hex2file


def _check_output_file(func):
    """
    A decorator which verifies the output file is correct.

    :param func: the function to wrap via decorator
    :return: the wrapped function
    """

    def _wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        # TODO: Temporary hack for verifying the file
        self.assertEqual(self.expected_file_size,
                         os.stat(self.output_file.name).st_size)
        os.unlink(self.output_file.name)

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

        cls.hex_str = """0x00FF00FF
            0xFF00FF00"""
        cls.expected_file_size = (cls.hex_str.count("\n") + 1) * 4

    @_check_output_file
    def test_write_str(self):
        """
        Tests hex2file.write_str.

        :return: None
        """

        # TODO: test append...

        self.output_file = tempfile.NamedTemporaryFile("w", delete=False)
        hex2file.write_str(self.hex_str, self.output_file.name)
        self.output_file.close()

    @_check_output_file
    def test_write_from_file(self):
        """
        Tests hex2file.write_from_file

        :return: None
        """

        # TODO: test append...

        with tempfile.NamedTemporaryFile("w", delete=False) as input_file:
            input_file.write(self.hex_str)

        with tempfile.NamedTemporaryFile("w",
                                         delete=False) as self.output_file:
            hex2file.write_from_file(input_file.name, self.output_file.name)

        os.unlink(input_file.name)


if __name__ == '__main__':
    unittest.main()
