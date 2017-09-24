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

import os


class Analyser:

    """
        given the url of the faculty list
        output the data in structured format
    """
    pass


class Downloader:

    """
        handles the downloading of faculty page
    """

    @staticmethod
    def download(university_name, url_list):
        if not os.path.exists(r'../temp'):
            os.makedirs(r'../temp')

        request.urlretrieve(url_list, filename="../temp/{}.html".format(university_name))


class Verifier:

    """
        handles the determination of attribute type
    """
    pass


class Loader:

    """
        handles the storing of verified data
    """




