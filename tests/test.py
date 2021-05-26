import unittest
from rss_reader.rss_reader import rss_reader
import io
import logging
import logging.handlers
import sys
from unittest import mock
from unittest.mock import patch

class TestReader(unittest.TestCase):
    def test_checking_the_installation(self):
        """Creates object and outputs it to stdout"""
        self.output = io.StringIO()
        sys.stdout = self.output

    def test_set_limit_for_print(self):
        """Good limit"""
        parser = rss_reader.command_arguments_parser(["--limit 3"])
        self.assertTrue(parser)

    def test_0_limit(self):
        """Test limit zero"""
        parser = rss_reader.command_arguments_parser(["--limit 0"])
        self.assertTrue(parser)

    def test_0_limit_message(self):
        """Test limit zero message"""
        parser = rss_reader.command_arguments_parser(["--limit 0"])
        self.assertLogs(parser, "Invalid limit. Enter the limit (greater than 0), please")

    def test_limit_negative_number(self):
        """Test limit negative number"""
        parser = rss_reader.command_arguments_parser(["--limit -5"])
        self.assertTrue(parser)


    def test_checking_verbose(self, mock_print):
        """Test verbose status message"""
        parser = rss_reader.command_arguments_parser(["https://news.yahoo.com/rss/", "--verbose"])
        self.assertTrue(parser.verbose)

    def test_checking_verbose_plus(self):
        """Test verbose status message"""
        parser = rss_reader.command_arguments_parser(["https://news.yahoo.com/rss/", "--verbose"])
        self.assertLogs(parser, "Getting access to the RSS")

    def test_checking_verbose_plus1(self):
        """Test verbose status message"""
        parser = rss_reader.command_arguments_parser(["https://news.yahoo.com/rss/", "--verbose"])
        data = rss_reader.parses_data(parser, "--limit 1")
        self.assertLogs(parser, "Reads amount of news - 1")


    def test_checking_verbose_plus_limit(self):
        """Test verbose status message and limit"""
        parser = rss_reader.command_arguments_parser(["--limit 7", "--verbose"])
        self.assertTrue(parser.verbose)


    def test_checking_json_format(self):
        """Test json format"""
        parser = rss_reader.command_arguments_parser(["https://news.yahoo.com/rss/", "--json"])
        self.assertTrue(parser.json)

    def test_checking_empty(self):
        """Test without link"""
        parser = rss_reader.command_arguments_parser([""])
        self.assertTrue(parser)


    def test_logging_INFO(self):
        """Test verbose"""
        parser = rss_reader.command_arguments_parser(["https://news.yahoo.com/rss/", "--verbose"])
        self.assertLogs(parser, logging.INFO)

    def test_logging_ERROR(self):
        """Test without verbose"""
        parser = rss_reader.command_arguments_parser(["https://news.yahoo.com/rss/"])
        self.assertLogs(parser, logging.ERROR)

    def test_wrong_source(self):
        """Test wrong url"""
        parser = rss_reader.parses_data(["https://news.sahoo.com/rss/"], "--limit 1")
        self.assertEqual(parser, {})


    def test_good_source(self):
        """Test good url"""
        parser = rss_reader.parses_data(["https://news.yahoo.com/rss/"], "--limit 1")
        self.assertEqual(parser, {})

    def test_printException(self):
        """Test not rss format"""
        parser = rss_reader.command_arguments_parser(["https://news.yahoo.com", "--limit 1"])
        with self.assertRaises(SystemExit):
            self.assertLogs(rss_reader.main(), logging.ERROR)


    def test_printing_news(self):
        """Test print of news"""
        dictionary = rss_reader.parses_data("https://news.yahoo.com/rss/", "--limit 1")
        self.assertEqual(dictionary, {'Feed': 'Yahoo News - Latest News & Headlines'})

    def test_printing_(self):
        """Test print of news"""
        dictionary = rss_reader.parses_data("https://news.yahoo.com/rss/", "--limit 1")
        list_of_keys = []
        for keys in dictionary:
            for part in dictionary["News"]:
                list_of_keys.append(part.keys)
                list_of_keys += keys
        self.assertEqual(list_of_keys, ['Title', 'Date', 'Link', 'Images'])


    def test_bad_link(self):
        # Test Exception is raising and user-friendly message is printing to stdout, if we give a bad link
        parser = rss_reader.parses_data("https://news.sahoo.com/rss/", "--limit 1")
        with self.assertRaises(Exception):
            self.assertEqual(parser, "Xml was failed")

    def test_0_link_(self):
        # Test Exception is raising and user-friendly message is printing to stdout, if we give a bad link
        parser = rss_reader.parses_data("https://news.sahoo.com/rss/", "--limit 1")
        with self.assertRaises(Exception):
            self.assertEqual(parser, "Xml was failed")


if __name__ == "__main__":
    unittest.main()
