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

    # --- public API ---

    def run(self):
        logging.info("retrieving crawl requests from database ...")
        user_requests = self.db_handler.get_crawl_requests()
        logging.info("{} requests found.".format(user_requests.count()))

        for user_request in user_requests:
            try:
                self._download_page(user_request['universityId'], user_request['facultyId'], user_request['facultyUrl'])
                self.db_handler.update_status("success", user_request['_id'], user_request['status'])
            except ValueError:  # invalid url
                self.db_handler.update_status("failure", user_request['_id'], user_request['status'])

    # --- private ---

    def _download_page(self, university_id, faculty_id, url_list):
        if not os.path.exists(self.PATH_TO_TEMP_WEB):
            os.makedirs(self.PATH_TO_TEMP_WEB)
        request.urlretrieve(url_list, filename=self.FORMAT_TEMP_WEB.format(university_id, faculty_id))


class Analyser:

    """
        handling the parsing of html
    """

    PATH_TO_TEMP_WEB = r'temp'
    STOP_WORDS = ['academic']

    def __init__(self):
        self.soup_memory = []
        self.name_dictionary = self._load_name_dictionary()

    # --- public API ---

    def run(self):
        files = os.listdir(self.PATH_TO_TEMP_WEB)
        for temp_file in files:
            soup = self._build_soup(temp_file)
            body_tag = soup.body
            self._count_direct_children_recursive(body_tag)
            element = self._get_most_children_element()
            self.parse_html_and_store(element)

    def parse_html_and_store(self, element):
        for item in element.contents:
            if isinstance(item, Tag):
                parser = MyHTMLParser()
                feed_content = str(item).replace("\n", "").strip().replace(u'\xa0', u' ')
                parser.feed(feed_content)
                data_list = parser.get_list()

                if not data_list:
                    continue

                token_list = parser.get_list()

                logging.info(token_list)

                if self._is_valid_data_row(token_list):
                    clean_token_list = self._clean_punctuation(token_list)

                    name = self._parse_name(clean_token_list)
                    position = self._parse_position(clean_token_list)
                    logging.info(name + " " + position)

    # --- private ---

    @staticmethod
    def _load_name_dictionary():
        """
        load the name dictionary from text and
        store as list
        :return: list
        """
        name_list = open("resource/name_dictionary.txt").read().split("\n")
        name_list = list(map(lambda x: x.split(',')[0], name_list))
        return name_list

    def _build_soup(self, file_name):
        """
        build BeautifulSoup object from file name
        :param file_name: string
        :return: BeautifulSoup
        """
        try:
            file = open(os.path.join(self.PATH_TO_TEMP_WEB, file_name), encoding='utf-8').read()
        except UnicodeDecodeError:
            file = open(os.path.join(self.PATH_TO_TEMP_WEB, file_name), encoding='latin-1').read()
        return BeautifulSoup(file, 'lxml')

    def _clear_memory(self):
        self.soup_memory = []

    # algorithm

    def _count_direct_children_recursive(self, element):
        """
        a recursive method to add Tag object into
        memory list, with a count of direct children
        :param element: Tag
        :return: None
        """
        for child in element.contents:
            if isinstance(child, Tag):
                count = self._get_number_of_direct_tags(child)
                self.soup_memory.append((count, child))
                self._count_direct_children_recursive(child)

    @staticmethod
    def _get_number_of_direct_tags(element):
        """
        get the number of direct children that are of
        type Tag
        :param element: Tag
        :return: int
        """
        counter = 0
        for child in element.contents:
            if isinstance(child, Tag):
                counter += 1
        return counter

    def _get_most_children_element(self):
        """
        sort the memory list, get the highest instance,
        clear the memory for another page
        :return: list
        """
        self.soup_memory.sort(key=lambda x: x[0], reverse=True)
        desired_element = self.soup_memory[0][1]
        self._clear_memory()  # clear memory for every call
        return desired_element

    # parsing

    @staticmethod
    def _parse_name(clean_token_list):
        """
        given cleaned token list, parse name from
        at most first 2 tokens in the list
        :param clean_token_list: list
        :return: string
        """
        name_token = clean_token_list[0].strip()

        if " " not in name_token:  # after strip, if single word, append second token
            name_token += " " + clean_token_list[1]

        name_token = name_token.strip()
        name_parser = HumanName(name_token)
        title = name_parser.title
        name = name_token.replace(title, "").strip()

        # post clean
        if "-" in name:
            name = name.split("-")[0].strip()

        return name

    @staticmethod
    def _parse_position(clean_token_list):
        """
        given cleaned token list, parse position
        from the entire list except the first token
        we ignore the possbility of the second token being the name
        because it will not likely to consist keywords such as prof

        only allow, professor, assoc prof, assist prof and reader (total 4)

        :param clean_token_list: list
        :return: string
        """
        position = ""
        for token_lower in clean_token_list[1:]:
            if "Professor" in token_lower or "Prof" in token_lower:  # maintain Cap to avoid word like `profile`
                if "Associate" in token_lower or "Assoc" in token_lower:
                    position = "Associate Professor"
                elif "Assistant" in token_lower:
                    position = "Assistant Professor"
                else:
                    position = "Professor"
                break
            else:
                if "Reader" in token_lower:
                    position = "Reader"
                    break

        return position

    def _clean_punctuation(self, token_list):
        """
        remove punctuation in the token list
        :param token_list: list
        :return: list
        """
        clean_token_list = []
        for token in token_list:
            if not self.is_punctuation_token(token):
                clean_token_list.append(token)
        return clean_token_list

    # validation

    def _is_valid_data_row(self, token_list):
        """
        validate whether a row is data row
        it is ok to kill an friendly target, but it is bad to allow false data go through

        1. if the first token of the row consists more than 5 words then probably it is not
        2. if there are stopping words in first token, common words in the header element
        3. joined the first 2 token, do name match with name dictionary
        :param token_list: list
        :return: boolean
        """
        first_token = token_list[0]
        first_token_list = first_token.split(" ")
        if len(first_token_list) > 5:
            return False

        if self._is_in_stop_words(first_token):
            return False

        joined_token = " ".join(token_list[:2]).split(" ")
        for item in joined_token:
            if item in self.name_dictionary:
                return True

        return False

    def _is_in_stop_words(self, token):
        """
        whether the token contains any of the stop words
        :param token: string
        :return: boolean
        """
        for stopwords in self.STOP_WORDS:
            if stopwords in token.lower():
                return True
        return False

    @staticmethod
    def is_punctuation_token(token):
        """
        whether a token is only a punctuation
        :param token: string
        :return: boolean
        """
        token = token.strip()
        if len(token) <= 2:
            return not token.isalpha()
        return False


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
        return self.db[self.CRAWL_REQUEST_COLLECTION].find(
            {"status": [0, 0, 0]}
        )

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
    # Downloader().run()
    Analyser().run()
