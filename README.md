# hex2file
A Python module for writing hex string content to a file.

## What it does
Writes ascii hex strings to a file directly as in binary hex format. The string
can be multi-line or single-line and 0x-prefixed or not. Excess whitespace in
the input is ignored.  

The following input (multi-line string):  
0xFF00FF00  
0xAABBCCDD  
0x12345678  
98765432 3456789A  
  
Would result in the following file content:  
FF00FF00AABBCCDD12345678987654323456789A

## Compatibility
Python 2/3 compatible.

# Install
Get the module via pip: `pip install hex2file`. Once installed 'hex2file' will
be added to your path and the module will be available for importing in your
Python projects.

# Usage
## Command Line
When pip installed, hex2file is added to your path. It can accept input directly
from stdin or from a file with the '-f' flag. See `hex2file --help`.

Example: `echo "0xFF00FF00" | hex2file /tmp/test`

## Library
The module can also be imported into a Python project. After installing it
simply `import hex2file` and use `hex2file.write()`.

# Testing
Run the tests using `python setup.py test` from the root directory of this
repository.
