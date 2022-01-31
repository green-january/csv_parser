# csv_parser
Technical Assessment

# Objective
Please write a tool that reads a CSV formatted file on stdin and emits a normalized CSV formatted file on stdout.

# Solution
The solution is a python command line utility that parses an input csv file, 
normalizes the raw data, and outputs the cleansed data to stdout in csv format. 
The command line utility accepts a file path as an input argument and manages 
reading the file within the application. 

A few elements are partially implemented for demonstration purposes:
1. Unit testing
1. Logging
1. Exception handling

## Improvements
In addition to the partially implemented items above, some of the opportunities for improvement include:
1. Accept input records on stdin instead of working with the file internally
1. Input validation
1. Forgiveness in parsing logic
1. Tracking and logging errors on specific records

# Usage
The python solution relies on a few external dependencies. Users may want to create a 
new python3 virtual environment to manage dependencies.

## Setup
```bash
# Create virtual environment
$ python3 -m venv venv

# Activate virtual environment
$ source ./venv/bin/activate

# Install dependencies
(venv)$ pip install -r requirements.txt
```
## Execute
```bash
# Help documentation
(venv)$ ./normalizer.py --help

# Execute
(venv)$ ./normalizer.py path/to/file.csv > output.csv

# Deactivate virtual environment
(venv)$ deactivate
```

## Logs
Logging output is written to an output file in the current directory `logging.log`.
Sample logging output:
```text
DEBUG 01-30-2022 21:13:18.056 root normalizer.py: Initiating normalization of input file: [./sample.csv]
DEBUG 01-30-2022 21:13:18.058 root parser.py: Opened input file: [./sample.csv]
DEBUG 01-30-2022 21:13:18.058 root parser.py: Writing output to stdout
DEBUG 01-30-2022 21:13:18.115 root normalizer.py: Completed normalization of input file: [./sample.csv]
```

# Unit Testing
The solution includes a small sample of unit tests for demonstrative purposes.
Tests may be executed with an active python3 virtual environment:
```bash
# Execute unit tests
(venv)$ python -m unittest
....
----------------------------------------------------------------------
Ran 4 tests in 0.049s

OK
```