#ch6_burp_wordlist.py
from burp import IBurpExtender
from burp import IContextMenuFactory
from javax.swing import JMenuItem
from java.util import ArrayList, List
from HTMLParser import HTMLParser
from datetime import datetime
import re

#This class attempts to strip all tags from and HTML page recieved in the http response
#The remaining text will appened to an array and then joined with " " for regex parsing
class TagStripper(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.page_text = []

    def handle_data(self, data):
        self.page_text.append(data)

    def handle_comment(self, data):
        self.page_text.append(data)

    def strip(self, html_page):
        self.feed(html_page)
        return " ".join(self.page_text)

#BurpExtender Class as per Reference API
class BurpExtender(IBurpExtender, IContextMenuFactory):
    #The extension is registered and we initialize the hosts and word list sets
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self.context = None
        self.hosts = set()
        self.word_list = set(["password"])
        callbacks.setExtensionName("BHP WordList")
        callbacks.registerContextMenuFactory(self)
        return

    #Invoke the "Create WordList" Menu
    def createMenuItems(self, context):
        self.context = context
        menu_list = ArrayList()
        menu_list.add(JMenuItem("Create WordList", actionPerformed=self.menu_action))
        return menu_list

    #Menu Action: Obtain the http_host and http_response. The http_host is appened to the hosts set
    #HTTP Response, if available, is analyzed to create a word list
    def menu_action(self, event):
        http_traffic = self.context.getSelectedMessages()
        for traffic in http_traffic:
            http_service = traffic.getHttpService()
            http_host = http_service.getHost()
            self.hosts.add(http_host)
            http_response = traffic.getResponse()
            if http_response:
                self.get_words(http_response)
        self.display_words()
        return

    #We check the header for a text document in the body. If the content type is text, username
    #the TagStripper class to parse out the text and run a regex to create our wordlist based on
    #the regex criteria and word length. The resulting words are added to the word_list set
    def get_words(self, http_response):
        headers, body = http_response.tostring().split("\r\n\r\n", 1)
        if headers.lower().find("content-type: text") == -1:
            return
        tag_stripper = TagStripper()
        page_text = tag_stripper.strip(body)
        word_candidates = re.findall("[a-zA-Z]\w{2,}", page_text)
        for word in sorted(word_candidates):
            if len(word) <= 12:
                self.word_list.add(word.lower())
        return

    #This method will display our word list after adding some optional suffices
    def display_words(self):
        print "Word List for: %s" % " ".join(self.hosts)
        for word in self.word_list:
            self.mangle(word)
        return

    #This method add the suffices below each word in the word_list set.
    def mangle(self, word):
        year = datetime.now().year
        suffices = ["", "!", "1", year]

        for suffix in suffices:
            print "%s%s" % (word, suffix)
            print "%s%s" % (word.capitalize(), suffix)
        return
