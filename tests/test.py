import unittest
from rss_reader.rss_reader import rss_reader
import sys
import io

class TestReader(unittest.TestCase):
    def checking_the_installation(self):
        """Creates object and outputs it to stdout"""
        self.output = io.StringIO()
        sys.stdout = self.output

    def set_limit_for_print(self):
        """Good limit"""
        parser = rss_reader.command_arguments_parser(["--limit 3"])
        self.assertTrue(parser)

    def test_0_limit(self):
        """Test limit zero"""
        parser = rss_reader.command_arguments_parser(["--limit 0"])
        self.assertTrue(parser)

    def checking_test_verbose(self):
        """Test verbose status message"""
        parser = rss_reader.command_arguments_parser(["https://news.yahoo.com/rss/", "--verbose"])
        self.assertTrue(parser.verbose)

    def checking_empty(self):
        """Test without link"""
        parser = rss_reader.command_arguments_parser([""])
        self.assertTrue(parser)


if __name__ == "__main__":
    unittest.main()

