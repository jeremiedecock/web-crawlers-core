#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015,2016 Jérémie DECOCK (http://www.jdhp.org)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Required package (on Debian8):
# - BeautifulSoup4: python3-bs4

# Online documentation:
# - BeautifulSoup4: http://www.crummy.com/software/BeautifulSoup/bs4/doc/
# - Urllib:         https://docs.python.org/3/library/internet.html
#                   https://docs.python.org/3/library/urllib.request.html

import argparse
from bs4 import BeautifulSoup
import json
import os
import os.path
import random
import re
import shutil
import time
import urllib.request
from urllib.parse import urljoin
from urllib.parse import urlparse

import crawler
from http_headers_yellowkorner import HTTP_HEADERS,URL_DOMAIN

# Waiting time parameters applied before getting the HTML code of the node
INIT_MEAN_TIME_SLEEP = 5
INIT_STD_TIME_SLEEP = 3

# Waiting time parameters applied before downloading files (PDF, AVI, ...)
MEAN_TIME_SLEEP = 1
STD_TIME_SLEEP = 1

class GalleryNode(crawler.Node):

    def __init__(self, url, page_number):
        self.url = url
        self.page_number = page_number

        # Wait a litte bit
        wt = abs(random.gauss(INIT_MEAN_TIME_SLEEP, INIT_STD_TIME_SLEEP))
        print("Waiting {} seconds...".format(wt))
        time.sleep(wt)

        # Get HTML with a customized user-agent
        print("Request", self.url)
        self.html = crawler.download_html(self.url, HTTP_HEADERS)
        
        #with open("root.html", 'wb') as out_file:
        #    out_file.write(self.html)


#    @property
#    def is_final(self):
#        return self.page_number < 1
#
#
#    @property
#    def child_nodes(self):
#        child_nodes_set = set()
#
#        if not self.is_final:
#            child_page_number = self.page_number - 1
#            start = child_page_number * 24
#            child_url = URL_DOMAIN + "?sz=24&start=" + str(start)
#
#            child_node = GalleryNode(child_url, child_page_number)
#
#            child_nodes_set.add(child_node)
#
#        return child_nodes_set


    def visit(self):
        """Do something with node value."""
        print("Visiting {}...".format(self.url))

        soup = BeautifulSoup(self.html)
        for ul_results_elem in soup.find_all(id='search-result-items'):
            for li_elem in ul_results_elem.find_all('li'):
                author = ""
                name = ""
                img_url = ""

                for div_prod_name_elem in li_elem.find_all('div', 'product-name'):
                    author = div_prod_name_elem.h2.a.string.strip()
                    name = [name_anchor.string.strip() for name_anchor in div_prod_name_elem.find_all('a', 'name-link')][0]

                for img_elem in li_elem.find_all('img'):
                    img_url = img_elem.get('src')[:-7]

                print("AUTHOR:", author)
                print("NAME:", name)
                print("IMG:", img_url)
                
                author = re.sub('[^A-Za-z0-9 _-]+', '', author)
                author = "-".join(author.lower().split())
                author = "-".join(author.lower().split("-"))

                name = re.sub('[^A-Za-z0-9 _-]+', '', name)
                name = "-".join(name.lower().split())
                name = "-".join(name.lower().split("-"))

                ext = img_url.lower().split(".")[-1]

                img_output_path = author + "_" + name + "." + ext

                print("Write", img_output_path)
                print()

                crawler.download_img(img_url, img_output_path, HTTP_HEADERS)

                # Wait a litte bit
                wt = abs(random.gauss(MEAN_TIME_SLEEP, STD_TIME_SLEEP))
                print("Waiting {} seconds...".format(wt))
                time.sleep(wt)


def main():
    """Main function"""

    for page_number in range(84):
        print()
        print("PAGE NUMBER:", page_number)
        print()
        print()

        start = max(0, (page_number - 1) * 24)
        node = GalleryNode(URL_DOMAIN + "?sz=24&start=" + str(start),
                           page_number=page_number)
        node.visit()

#    # TRAVERSE THE GRAPH ######################################################
#
#    start_page_number = 83
#    start_node = GalleryNode(URL_DOMAIN + "?sz=24&start=" + str((start_page_number - 1) * 24),
#                             page_number=start_page_number)
#    crawler.walk(start_node)
#    #print(start_node.is_final)
#    #print(start_node.child_nodes)
#    #print(start_node.visit())

if __name__ == '__main__':
    main()

