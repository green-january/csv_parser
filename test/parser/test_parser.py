from unittest import TestCase

from parser.exceptions import ParsingException
from parser.parser import (
    convert_timestamp_to_eastern_rfc9333,
    convert_duration_string_to_seconds,
    TIMESTAMP
)


class TestConvertTimestampToEasternRfc9333(TestCase):

    def test_convert_timestamp_to_eastern_rfc9333(self):
        # given: a well formed US/Pacific timestamp string that is not timezone aware
        timestamp_string = '4/1/11 11:00:00 AM'

        # when: the string is converted to US/Eastern
        result = convert_timestamp_to_eastern_rfc9333(timestamp_string)

        # then: the resulting timestamp string is converted to US/Eastern and formatted in RFC3339
        self.assertEqual(result, '2011-04-01T14:00:00-04:00')

    def test_convert_timestamp_to_eastern_rfc9333_malformed_input(self):
        # given: a timestamp string that is not well formed
        timestamp_string = '4/1/2011 11:00:00 AM'

        # when: converting the string to US/Eastern
        # then: a parsing exception is raised
        with self.assertRaises(ParsingException) as ex:
            result = convert_timestamp_to_eastern_rfc9333(timestamp_string)

        # and: the exception indicates the timestamp could not be parsed
        self.assertIn(TIMESTAMP, ex.exception.args[0])

    def test_convert_timestamp_to_eastern_rfc9333_invalid_date(self):
        # given: a timestamp string that is not a valid date
        timestamp_string = '4/31/11 11:00:00 AM'

        # when: converting the string to US/Eastern
        # then: a parsing exception is raised
        with self.assertRaises(ParsingException) as ex:
            result = convert_timestamp_to_eastern_rfc9333(timestamp_string)

        # and: the exception indicates the timestamp could not be parsed
        self.assertIn(TIMESTAMP, ex.exception.args[0])


class TestNormalizeDuration(TestCase):

    def test_normalize_duration_to_seconds(self):
        # given: a duration of time represented as a string
        duration_str = '1:10:10.100'

        # when: the string is normalized
        result = convert_duration_string_to_seconds(duration_str)

        # then: the result is the correct number of seconds
        self.assertAlmostEqual(float(result), 4210.1)
