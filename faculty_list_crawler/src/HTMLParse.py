from html.parser import HTMLParser
from functools import reduce
from urllib.parse import urlparse
from heapq import nlargest


# import name database
# with open('datamodified.dat','r') as f:
#     names = set(i.split(',')[0] for i in list(f))
#




class HTMLNode():
    def __init__(self, tag, url, route, parent = None, attrs = None, data = None, children = None):
        self.tag = tag
        self.url = url
        self.route = route
        self.parent = parent
        self.children = children if children else []
        self.attrs = attrs if attrs else {}
        self.data = data if data else []
        self.cmp = None
        
        # Implementation Specific Class Instance Variables
        self.mc = None
        self.names = set()
        
    def addChild(self, tag, url, parent, attrs):
        self.children.append(HTMLNode(tag, url, self.route + [len(self.children)], parent, attrs))
        return len(self.children)-1
    
    def getChild(self, idx):
        return self.children[idx]
    
    def getChildRecursive(self, route):
        return reduce(lambda n, i: n[i], route, self)
    
    def addData(self, data):
        self.data.append(data)
        
    def depthLevel(self, d):
        for c in self.children:
            if not d:
                yield c
            yield from c.depthLevel(d-1)
            
    def depthFirstTraversal(self):
        yield self
        for c in self.children:
            yield from c.depthFirstTraversal()
    
    def getData(self):
        return reduce(lambda x, y: x + y, (i.data for i in self.depthFirstTraversal()), [])
    
    def getCleanData(self):
        return [i.strip() for i in self.getData() if i.strip()]
    
    def getCleanDataString(self):
        return ' '.join(self.getCleanData())

    def expandLinks(self):
        currUrl = urlparse(self.url)
        urlList = []
        for c in self.depthFirstTraversal():
            if c.tag=='a' and 'href' in c.attrs:
                if c.attrs['href'][0] == '/':
                    urlList.append([c, currUrl.scheme + '://' + currUrl.netloc + c.attrs['href']])
                elif 'http' in urlparse(c.attrs['href']).scheme:# and urlparse(c.attrs['href']).netloc == currUrl.netloc:
                    urlList.append([c, c.attrs['href']])
        for c, u in urlList:
            print(u)
            c.children.append(GPHTMLParser(u,self.route + [len(self.children)],c).HTMLGraph)

    def getRouteWithClasses(self):
        c = self
        r = self.route[::-1]
        for i in range(len(r)):
            r[i] = [r[i],c.tag,c.attrs.get('class','').split(' ')]
            c = c.parent
        return r[::-1]
    
    def findMostChildrenRecursive(self):
        return max(self.depthFirstTraversal(), key=lambda x: len(x.children))
    
    def findNMostChildrenRecursive(self, n):
        return nlargest(n, self.depthFirstTraversal(), key=lambda x: len(x.children))
        
    def __repr__(self):
        return 'TAG: {} ATTRIBUTES: {} DATA: {} CHILDREN: \n{}'.format(self.tag, self.attrs, self.data, '\n'.join(i.tag + str(i.attrs) for i in self.children))
        
    def __getitem__(self,idx):
        return self.children[idx]
    
    def findChildWithMostInstancesOfStringRecursive(self, string):
        return max(self.depthFirstTraversal(), key=lambda x: sum(string.lower() in s.lower() for s in x.getCleanData()))
    
    # Implementation Specific Method
    # This method returns a number between 0 and 1 specifying how much of the string was part of a name
    def containsName(self, data):
        d = data
        r = 0
        for n in names:
            if n in d:
                r+=len(n)/len(data)
                d = d.replace(n,'')
        return r

#     def containsPhd(self, data):

    # Implementation Specific Method
    def findNames(self):
        return {d:self.containsName(d) for d in self.data}
    
    # Implementation Specific Method
    def findMainFacultyList(self):
        # This deals with faculty pages with multiple lists of faculty members
        # Ideally we want to get the core faculty members, so this algorithm gets 3 of the nodes with the most children
        # And then maximizes for the number of children in that child node containing 'prof' in it
        
        self.mc = max(self.findNMostChildrenRecursive(3), key=lambda x: sum(any('prof' in s.lower() for s in c.getCleanData()) for c in x.children))
        return self.mc
    
    # Implementation Specific Method
    def findChildrenWithNamesRecursive(self):
        mc = self.mc if self.mc else self.findMainFacultyList()
        r = [k for k in ([{k:v for k,v in i.findNames().items() if v},i.route[len(mc.route):]] for i in mc.depthFirstTraversal()) if k[0]]
        sr = {tuple(i[1][1:]):0 for i in r}
        sr = {k:sum(j for i in r for j in i[0].values() if tuple(i[1][1:])==k) for k in sr}
        res = [i for i in r if tuple(i[1][1:])==max(sr, key=lambda k: sr[k])]

        # This is a stupid monkeypatch for sites that have the names split up into multiple HTML Nodes for whatever reason
        # Typically with these sites the above algorithm is able to find the correct location of the names, but only gets
        # Last names or First names because they are split into different child nodes
        # The idea is to ascend the HTML Tree until it finds that _all_ the names have a space in them

        if not all(' ' in j for i in res for j in i[0]):
            subRoute = res[0][1][1:]
            while not all(' ' in mc.getChildRecursive([i[1][0]] + subRoute).getCleanDataString() for i in res) and subRoute:
                subRoute = subRoute[:-1]
            for i in range(len(res)):
                nameString = mc.getChildRecursive([res[i][1][0]] + subRoute).getCleanDataString()
                proportion = 0
                nameStringMod = nameString
                for n in names:
                    if n in nameStringMod:
                        proportion += len(n)/len(nameString)
                        nameStringMod = nameStringMod.replace(n, '')
                res[i][0]={nameString:proportion}
                res[i][1]=[res[i][1][0]] + subRoute
        res = {max(i[0],key=lambda x:i[0][x]): i[1] for i in res}
        self.names = res
        return res

    def findDetails(self):
        if not self.names:
            self.findChildrenWithNamesRecursive()
        self.mc.expandLinks()
        nameIdx = {v[0]:k for k,v in self.names.items()}
        subRoute = None
        mc = self.mc
        for c in mc[next(iter(nameIdx))].depthFirstTraversal():
            if c.tag == '' and c.parent.tag == 'a' and any(c.route[len(mc.route)]==k for k in nameIdx):
#                 print(c.route[len(mc.route)])
                for d in mc[c.route[len(mc.route)]].depthFirstTraversal():
                    print(d.route[len(mc.route)+1:])
                    if any(i in nameIdx[c.route[len(mc.route)]] for i in d.data):
                        try:
                            for i in nameIdx:
                                mc.getChildRecursive([i] + d.route[len(mc.route)+1:])
                        except:
                            continue
                        else:
                            if all(mc.getChildRecursive([i] + d.route[len(mc.route)+1]).data in nameIdx[i] for i in nameIdx):
                                subRoute = d.route[len(mc.route)+1:]
                                break
        print(subRoute)


class GPHTMLParser(HTMLParser):
    non_closing_tags = set(['area','base','br','col','command','embed','hr','img','input','keygen','link','meta','param','source','track','wbr'])
    drv = PhantomJSDriver('http://115.66.242.122:8910')
    def __init__(self, url, route = None, parent = None):
        HTMLParser.__init__(self)
        self.HTMLGraph = HTMLNode('', url, route if route else [], parent)
        self.route = []
        self.url = url
        self.feed(self.drv.getPage(url))
        
    def currNode(self):
        return self.HTMLGraph.getChildRecursive(self.route)
    
    def handle_starttag(self, tag, attrs):
        if tag in self.non_closing_tags:
            return
        self.route.append(self.currNode().addChild(tag, self.url, self.currNode(), dict(attrs)))

    def handle_endtag(self, tag):
        self.route.pop()

    def handle_data(self, data):
        self.currNode().addData(data)


# In[4]:

import tabulate
from IPython.display import HTML, display
hg = GPHTMLParser('http://www.seed.manchester.ac.uk/geography/about/people/').HTMLGraph
display(HTML(tabulate.tabulate(hg.findChildrenWithNamesRecursive().items(),tablefmt='html',headers=['name & probability','route'])))


# In[5]:

hg2 = GPHTMLParser('http://www.colorado.edu/geography/ppl4/faculty').HTMLGraph
display(HTML(tabulate.tabulate(hg2.findChildrenWithNamesRecursive().items(),tablefmt='html',headers=['name & probability','route'])))


# In[6]:

hg3 = GPHTMLParser('http://geography.utoronto.ca/people/faculty/full-time-faculty/').HTMLGraph
display(HTML(tabulate.tabulate(hg3.findChildrenWithNamesRecursive().items(),tablefmt='html',headers=['name & probability','route'])))


# In[7]:

hg4 = GPHTMLParser('http://www.geog.ucl.ac.uk/people/academic-staff').HTMLGraph
display(HTML(tabulate.tabulate(hg4.findChildrenWithNamesRecursive().items(),tablefmt='html',headers=['name & probability','route'])))


# In[8]:

hg5 = GPHTMLParser('http://www.geog.qmul.ac.uk/staff/academicstaff/').HTMLGraph
display(HTML(tabulate.tabulate(hg5.findChildrenWithNamesRecursive().items(),tablefmt='html',headers=['name & probability','route'])))


# In[9]:

hg6 = GPHTMLParser('https://www.geog.cam.ac.uk/people/').HTMLGraph
display(HTML(tabulate.tabulate(hg6.findChildrenWithNamesRecursive().items(),tablefmt='html',headers=['name & probability','route'])))


# In[10]:

hg7 = GPHTMLParser('http://www.geog.ox.ac.uk/staff/').HTMLGraph
display(HTML(tabulate.tabulate(hg7.findChildrenWithNamesRecursive().items(),tablefmt='html',headers=['name & probability','route'])))


# In[11]:

hg8 = GPHTMLParser('http://www.geog.ubc.ca/people/').HTMLGraph
display(HTML(tabulate.tabulate(hg8.findChildrenWithNamesRecursive().items(),tablefmt='html',headers=['name & probability','route'])))


# In[12]:

hg9 = GPHTMLParser('http://www.comp.nus.edu.sg/about/depts/cs/faculty/').HTMLGraph
display(HTML(tabulate.tabulate(hg9.findChildrenWithNamesRecursive().items(),tablefmt='html',headers=['name & probability','route'])))


# In[13]:

hg10 = GPHTMLParser('https://www.sph.nus.edu.sg/about/faculty-directory').HTMLGraph
display(HTML(tabulate.tabulate(hg10.findChildrenWithNamesRecursive().items(),tablefmt='html',headers=['name & probability','route'])))


# In[14]:

hg11 = GPHTMLParser('https://accounting.wharton.upenn.edu/faculty/faculty-list/').HTMLGraph
display(HTML(tabulate.tabulate(hg11.findChildrenWithNamesRecursive().items(),tablefmt='html',headers=['name & probability','route'])))


# In[ ]:



