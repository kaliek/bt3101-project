from faculty_list_crawler.src.main import Downloader

import unittest


class TestDownloader(unittest.TestCase):

    TEST_LIST = [
        ("University College London", "http://www.geog.ucl.ac.uk/people/academic-staff"),
        ("University of Colorado – Boulder", "http://www.colorado.edu/geography/ppl4/faculty")
    ]

    def test_download(self):
        downloader = Downloader()

        for item in self.TEST_LIST:
            downloader.download(*item)


if __name__ == '__main__':
    unittest.main()
