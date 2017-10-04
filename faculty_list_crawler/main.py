"""
    University College London: http://www.geog.ucl.ac.uk/people/academic-staff

    University of Colorado – Boulder: http://www.colorado.edu/geography/ppl4/faculty

    University of Manchester: http://www.seed.manchester.ac.uk/geography/about/people/

    University of Toronto (St George): http://geography.utoronto.ca/people/faculty/full-time-faculty/

    Queen Mary London: http://www.geog.qmul.ac.uk/staff/academicstaff/

    University of Cambridge: https://www.geog.cam.ac.uk/people/

    University of British Columbia: http://www.geog.ubc.ca/people/

    University of Oxford: http://www.geog.ox.ac.uk/staff/
"""
from urllib import request
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
from pymongo import MongoClient
from common import UnknownStatusException

import os


class Downloader:

    """
        handles the downloading of faculty page
    """

    DB_IP = '115.66.242.122'
    DB_PORT = 9212
    PROJECT_DATABASE = 'bt3101'
    CRAWL_REQUEST_COLLECTION = 'crawlrequests'

    def __init__(self):
        self.client = MongoClient(self.DB_IP, self.DB_PORT)
        self.db = self.client[self.PROJECT_DATABASE]

    @staticmethod
    def _download(university_id, faculty_id, url_list):
        if not os.path.exists(r'../temp'):
            os.makedirs(r'../temp')
        request.urlretrieve(url_list, filename="../temp/{}-{}.html".format(university_id, faculty_id))

    def _get_crawl_requests(self):
        return self.db[self.CRAWL_REQUEST_COLLECTION]

    def process_requests(self):
        requests = self._get_crawl_requests()
        for user_request in requests.find():
            self._download(user_request['universityId'], user_request['facultyId'], user_request['facultyUrl'])

            self._update_status("success", user_request['_id'], user_request['status'])

    def _update_status(self, status, request_id, original_status):
        if status == 'success':
            original_status[0] = 1
            self.db[self.CRAWL_REQUEST_COLLECTION].update(
                {"_id": request_id},
                {
                    '$set': {"status": original_status}
                }
            )
        elif status == 'failure':
            original_status[0] = 2
            self.db[self.CRAWL_REQUEST_COLLECTION].update(
                {"_id": request_id},
                {
                    '$set': {"status": original_status}
                }
            )
        else:
            raise UnknownStatusException


class Analyser:

    """
        given the url of the faculty list
        output the data in structured format
    """
    def __init__(self):
        self.soup = None
        self.soup_memory = []

    def build_soup(self):
        self.soup = BeautifulSoup(open('../temp/University of Colorado – Boulder.html', 'r', encoding='utf-8').read(), 'lxml')
        # self.soup = BeautifulSoup(open('../temp/University College London.html', 'r', encoding='utf-8').read(), 'lxml')

    def get_body(self):
        return self.soup.body

    def find_most_children(self, element):
        for child in element.contents:
            if isinstance(child, Tag):
                count = self.find_number_of_direct_tags(child)
                self.soup_memory.append((count, child))
                self.find_most_children(child)

    def find_number_of_direct_tags(self, element):
        counter = 0
        for child in element.contents:
            if isinstance(child, Tag):
                counter += 1
        return counter

    def get_highest_elemment(self):
        self.soup_memory.sort(key=lambda x:x[0], reverse=True)
        print(self.soup_memory[0])





class Verifier:

    """
        handles the determination of attribute type
    """
    pass


class Loader:

    """
        handles the storing of verified data
    """


if __name__ == '__main__':
    Downloader().process_requests()
