from burp import IBurpExtender
from burp import IContextMenuFactory

from javax.swing import JMenuItem
from java.util import List, ArrayList
from java.net import URL

import socket
import urllib
import json
import re
import base64

bing_api_key = "YOURKEY"

calss BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self.context = None
        
        # we set up out extension
        callbacks.setExtensionName("BHP Bing")
        callbacks.registerContextMenuFactory(self)
        return
    
    def createMenuItems(self, context_menu):
        self.context = context_menu
        menu_list = ArrayList()
        menu_list.add(JMenuItem("Send to Bing", actionPerformed=self.bing_menu))
        return menu_list
        
    def bing_search(self, host):
        
        # check if we have an IP or hostname
        is_ip = re.match("[0-9] + (?:\.[0-9]+){3}", host)
        
        if is_ip:
            ip_address = host
            domain = False
        else:
            ip_address = socket.gethostbyname(host)
            domain = True
            
        if domain:
            bing_query_string = "'domain:%s'" % host
            self.bing_query(bing_query_string)
            
    def bing_query(self, bing_query_string):
        
        print("Pefforming Bing search: %s" % bing_query_string)
        
        # encode our query
        quoted_query = urllib.quote(bing_query_string)
        
        http_request = "GET https://api.datamarket.azure.com/Bing/Search/Web?\
                        $.format=json&top=20&Query-%s HTTP/1.1\r\n" % quoted_query
        http_request += "Host: api.datamarket.azure.com\r\n"
        http_request += "Connection: close\r\n"
        http_request += "Authorization: Basic %s\r\n" %base64.b64encode(":%s"%.bing_api_key)
        http_request += "User-Agent: Blackhat Python\r\n\r\n"
        
        json_body = self._callbacks.makeHttpRequest("api.datamarket.azure.com", .443, True, http_request).tostring()
        
        try:
            r = json.loads(json_body)
            
            if len(r["d"]["results"]):
                for site in r["d"]["results"]:
                    
                    print("*" * 100)
                    print(site["Title"])
                    print(site["Url"])
                    print(site["Description"])
                    print("*" * 100)
                    
                    j_url = URL(site["Url"])
                    
            if not self._callbacks.isInScope(j_url):
                print("Adding to Burp scope")
                self._callbacks.includeInScope(jurl)
            except:
                print("Not results from Bing")
                pass
            return