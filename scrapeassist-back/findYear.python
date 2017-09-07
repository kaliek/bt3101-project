from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import ssl



def text_contain_number(text):
    # return re.search('(?!\d)19[6-9]\d|2[0-1]\d{2}(?<!\d)',text)
    m = re.search('(?<![0-9])(19[6-9]\d|20[0-1]\d)(?!\d)',text)
    if m is None:
        return None
    return m.group(0)

url = "https://bioengineering.stanford.edu/people/michael-lin"
# url = "https://engineering.stanford.edu/people/zev-bryant"
# url = "http://bme.columbia.edu/christoph-juchem"
context = ssl._create_unverified_context()
html = urlopen(url, context=context).read()
soup = BeautifulSoup(html, "html.parser")

for script in soup(["script", "style"]):
    script.extract() 

text = soup.get_text()

lines = (line.strip() for line in text.splitlines())
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
text = '\n'.join(chunk for chunk in chunks if chunk)

result = text_contain_number(text)
if result is None:
    print ("No Number")
else:
    print (result)


