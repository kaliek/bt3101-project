from html.parser import HTMLParser


class UnknownStatusException(Exception):
    pass


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
