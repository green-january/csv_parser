#!/usr/bin/env python3
import argparse
import logging

from parser.parser import normalize_input_file_to_stdout


def main(input_file_path):
    """
    Initiate csv parsing and data normalization

    :param input_file_path: path to a csv file
    """
    # initialize system logging
    logging.basicConfig(
        filename='logging.log',
        level=logging.DEBUG,
        format='%(levelname)s %(asctime)s.%(msecs)03d %(name)s %(filename)s: %(message)s',
        datefmt='%m-%d-%Y %H:%M:%S'
    )

    logging.debug(f'Initiating normalization of input file: [{input_file_path}]')
    normalize_input_file_to_stdout(input_file_path)

    logging.debug(f'Completed normalization of input file: [{input_file_path}]')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Normalize input csv data and output the results to stout. Input "
                    "data is expected in csv comma delimited format with a header row."
    )
    parser.add_argument("input_file", help='path to the input csv file')
    args = parser.parse_args()

    main(args.input_file)
