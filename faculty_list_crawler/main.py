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
from bs4.element import Tag
from pymongo import MongoClient
from common import UnknownStatusException
from nameparser import HumanName
import logging
import os
from html.parser import HTMLParser
import string


class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.data_list = []

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        if data != " ":
            self.data_list.append(data)

    def get_list(self):
        return self.data_list


class Downloader:

    """
        handles the downloading of faculty page
    """
    PATH_TO_TEMP_WEB = r'temp'
    FORMAT_TEMP_WEB = "temp/{}-{}.html"

    def __init__(self):
        self.db_handler = DatabaseHandler()

    def _download(self, university_id, faculty_id, url_list):
        if not os.path.exists(self.PATH_TO_TEMP_WEB):
            os.makedirs(self.PATH_TO_TEMP_WEB)
        request.urlretrieve(url_list, filename=self.FORMAT_TEMP_WEB.format(university_id, faculty_id))

    def process_requests(self):
        logging.info("retrieving crawl requests from database ...")
        user_requests = self.db_handler.get_crawl_requests()
        logging.info("{} requests found.".format(user_requests.count()))

        for user_request in user_requests.find():
            self._download(user_request['universityId'], user_request['facultyId'], user_request['facultyUrl'])
            self.db_handler.update_status("success", user_request['_id'], user_request['status'])


class Analyser:

    """
        given the url of the faculty list
        output the data in structured format
    """

    PATH_TO_TEMP_WEB = r'temp'

    def __init__(self):
        self.soup_memory = []
        self.name_dictionary = self.load_name_dictionary()

    def load_name_dictionary(self):
        name_list = open("name_dictionary.txt").read().split("\n")
        name_list = list(map(lambda x: x.split(',')[0], name_list))
        return name_list

    def _build_soup(self, file_name):
        try:
            file = open(os.path.join(self.PATH_TO_TEMP_WEB, file_name), encoding='utf-8').read()
        except UnicodeDecodeError:
            file = open(os.path.join(self.PATH_TO_TEMP_WEB, file_name), encoding='latin-1').read()
        return BeautifulSoup(file, 'lxml')

    def find_most_children(self, element):
        for child in element.contents:
            if isinstance(child, Tag):
                count = self._find_number_of_direct_tags(child)
                self.soup_memory.append((count, child))
                self.find_most_children(child)

    @staticmethod
    def _find_number_of_direct_tags(element):
        counter = 0
        for child in element.contents:
            if isinstance(child, Tag):
                counter += 1
        return counter

    def get_highest_element(self):
        self.soup_memory.sort(key=lambda x: x[0], reverse=True)
        return self.soup_memory[0][1]

    # TODO: the core of the project: how to parse??????
    def _parse_element(self, element):
        for item in element.contents:
            if isinstance(item, Tag):
                parser = MyHTMLParser()
                feed_content = str(item).replace("\n", "").strip().replace(u'\xa0', u' ')
                parser.feed(feed_content)
                data_list = parser.get_list()

                if not data_list:
                    continue

                token_list = parser.get_list()

                if self.is_valid_data_row(token_list):

                    clean_token_list = []
                    for token in token_list:
                        if not self.is_punctuation_token(token):
                            clean_token_list.append(token)

                    name_token = clean_token_list[0]  # or 0:1, will add a function to determine that
                    name_parser = HumanName(name_token)
                    title = name_parser.title
                    name = name_token.replace(title, "").strip()
                    logging.info(name)

    def is_valid_data_row(self, token_list):
        # test first few token are names? if not not relevant, allow friendly kills
        if len(token_list) < 2 and len(token_list[0]) < 20:
            return True

        first_token = " ".join(token_list[:2]).split(" ")
        for item in first_token:
            if item in self.name_dictionary:
                return True
        return False

    def is_punctuation_token(self, token):
        if len(token) <= 2:
            return not token.isalpha()
        return False

    def clear_memory(self):
        self.soup_memory = []

    def analyse_web(self):
        files = os.listdir(self.PATH_TO_TEMP_WEB)
        for temp_file in files:
            soup = self._build_soup(temp_file)
            body_tag = soup.body
            self.find_most_children(body_tag)
            element = self.get_highest_element()
            self.clear_memory()
            self._parse_element(element)


class DatabaseHandler:

    """
        handles operation to database
        the DB used during developmment is an instance of MongoDB hosted on Theodore's personal server
        the production DB would require further discussion
    """

    DB_IP = '115.66.242.122'
    DB_PORT = 9212
    PROJECT_DATABASE = 'bt3101'
    CRAWL_REQUEST_COLLECTION = 'crawlrequests'

    def __init__(self):
        self.client = MongoClient(self.DB_IP, self.DB_PORT)
        self.db = self.client[self.PROJECT_DATABASE]

    def get_crawl_requests(self):
        return self.db[self.CRAWL_REQUEST_COLLECTION]

    def update_status(self, status, request_id, original_status):
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


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # Downloader().process_requests()
    Analyser().analyse_web()
