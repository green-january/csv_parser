import csv
import logging
import pytz
import sys

from datetime import datetime

from parser.exceptions import ParsingException

# field names
FULL_NAME = 'FullName'
ZIP = 'ZIP'
TOTAL_DURATION = 'TotalDuration'
BAR_DURATION = 'BarDuration'
FOO_DURATION = 'FooDuration'
TIMESTAMP = 'Timestamp'
NOTES = 'Notes'
ADDRESS = 'Address'

# expected format of timestamps in file
TIMESTAMP_FORMAT = '%m/%d/%y %I:%M:%S %p'


def normalize_input_file_to_stdout(input_file_path):
    """
    Parse an input csv file and normalize each row. Normalized data will be written
    to standard out. The input file is expected to contain a header row with the
    following fields:

    Timestamp,Address,ZIP,FullName,FooDuration,BarDuration,TotalDuration,Notes

    :param input_file_path: path to a csv file
    """
    # field order matches order of header fields
    fields = [
        TIMESTAMP, ADDRESS, ZIP, FULL_NAME, FOO_DURATION,
        BAR_DURATION, TOTAL_DURATION, NOTES
    ]
    writer = csv.DictWriter(sys.stdout, fieldnames=fields)
    with open(input_file_path, encoding='utf-8') as input_file:
        reader = csv.DictReader(input_file, fieldnames=fields)
        next(reader, None)

        logging.debug(f'Opened input file: [{input_file_path}]')
        logging.debug('Writing output to stdout')

        writer.writeheader()
        for row in reader:
            normalize_row_to_writer(row, writer)


def normalize_row_to_writer(raw_data, writer):
    """
    Normalize raw data values from the input file into well-formatted values for output.
    Output cleaned data to the writer.

    :param raw_data: dictionary of raw data with keys from the original file header
    :param writer:
    """
    clean_data = raw_data.copy()
    try:
        # scrub the foo and bar durations first, so the results may be used to calculate their total
        clean_data[FOO_DURATION] = convert_duration_string_to_seconds(raw_data[FOO_DURATION])
        clean_data[BAR_DURATION] = convert_duration_string_to_seconds(raw_data[BAR_DURATION])
        clean_data[TOTAL_DURATION] = calculate_total_duration(
            clean_data[FOO_DURATION],
            clean_data[BAR_DURATION]
        )
        clean_data[TIMESTAMP] = convert_timestamp_to_eastern_rfc9333(raw_data[TIMESTAMP])
        clean_data[ZIP] = format_zip(raw_data[ZIP])
        clean_data[FULL_NAME] = format_full_name(raw_data[FULL_NAME])
    except ParsingException as ex:
        print('WARNING could not parse record. See log for details', file=sys.stderr)
        logging.exception(ex)
        return
    writer.writerow(clean_data)


def convert_timestamp_to_eastern_rfc9333(timestamp_string):
    """
    Convert a timestamp string into eastern time and format to RFC 9333 for output.
    Input timestamps are expected in the format:

    m/d/yy hh:MM:SS AM/PM
    1/1/20 11:10:59 PM

    Input values do not contain timezone designations, but are expected to be
    US/Pacific time.

    :param timestamp_string: timestamp string to convert
    :return: string in RFC9333 format representing input time in US/Eastern
    """
    try:
        date_time = datetime.strptime(timestamp_string, TIMESTAMP_FORMAT)
    except ValueError as ve:
        raise ParsingException(
            f'{TIMESTAMP} field must be a valid date in the format {TIMESTAMP_FORMAT}'
        ) from ve

    pacific = pytz.timezone('US/Pacific')
    pacific_aware = pacific.localize(date_time)
    eastern_aware = pacific_aware.astimezone(pytz.timezone('US/Eastern'))
    return eastern_aware.isoformat()


def convert_duration_string_to_seconds(duration_string):
    """
    Convert a string representation of time duration into decimal seconds. Input
    durations are expected in the format:

    HH:MM:SS.sss
    50:24:10.221

    :param duration_string: string representation of a time duration
    :return: duration as a string of elapsed seconds
    """
    hours, minutes, seconds = duration_string.split(':')
    duration = (float(hours) * 60 * 60) + (float(minutes) * 60) + float(seconds)
    return f'{duration:.3f}'


def calculate_total_duration(foo_duration_seconds, bar_duration_seconds):
    """
    Calculate the total duration in seconds

    :param foo_duration_seconds: foo duration in seconds
    :param bar_duration_seconds: bar duration in seconds
    :return: sum of input durations as a string
    """
    total = float(foo_duration_seconds) + float(bar_duration_seconds)
    return f'{total:.3f}'


def format_zip(zip_string):
    return zip_string.rjust(5, '0')


def format_full_name(name):
    return name.upper()
