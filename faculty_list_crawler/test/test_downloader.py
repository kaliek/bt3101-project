import unittest

from faculty_list_crawler.main import Downloader


class TestDownloader(unittest.TestCase):

    TEST_LIST = [
        ("University College London", "http://www.geog.ucl.ac.uk/people/academic-staff"),
        ("University of Colorado – Boulder", "http://www.colorado.edu/geography/ppl4/faculty")
    ]

    def test_download(self):
        downloader = Downloader()

        for item in self.TEST_LIST:
            downloader._download_page(*item)


if __name__ == '__main__':
    unittest.main()
