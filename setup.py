import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='hex2file',
    version='1.1.1',
    packages=['hex2file'],
    install_requires=['deprecation==2.0.5'],
    test_suite='nose.collector',
    tests_require=['nose'],
    entry_points={
        'console_scripts': ['hex2file=hex2file:_cmd_line']
    },
    url='https://github.com/mattixtech/hex2file',
    license='MIT',
    author='Matthew Brooks',
    author_email='matt@mattbrooks.ca',
    description='A Python module for writing hex string content to a file.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='hex'
)
