#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Jérémie DECOCK (http://www.jdhp.org)

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
from urllib.parse import urljoin

import webcrawlers.crawler
from webcrawlers.deadlinks.http_headers import HTTP_HEADERS

class DeadLinksNode(webcrawlers.crawler.Node):

    def __init__(self, url, depth):
        print("Creating node (level {}) {}...".format(depth, url))

        self.url = url
        self.depth = depth

        # Get HTML with a customized user-agent
        print("Request", self.url)
        self.html = webcrawlers.crawler.download_html(self.url, HTTP_HEADERS)


    @property
    def child_nodes(self):
        child_nodes_set = set()

        if not self.is_final:
            #html = urllib.request.urlopen(self.url).read()
            soup = BeautifulSoup(self.html)

            for anchor in soup.find_all('a'):
                relative_url = anchor.get('href')
                absolute_url = urljoin(self.url, relative_url)
                child_node = DeadLinksNode(absolute_url, self.depth + 1)
                #print(id(child_node))
                child_nodes_set.add(child_node)

        return child_nodes_set


    def visit(self):
        """Do something with node value."""
        print("Visiting {}...".format(self.url))


    @property
    def is_final(self):
        # TODO: if self.url start with self.allowed_url_roots return True
        return self.depth >= 2


def main():
    """Main function"""

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Detect deadlinks in web pages.")
    parser.add_argument("url", nargs=1, metavar="URL",
                        help="The URL of the webpage to parse.")
    args = parser.parse_args()

    url = args.url[0]

    # TRAVERSE THE GRAPH ######################################################

    start_node = DeadLinksNode(url, depth=0)
    webcrawlers.crawler.walk(start_node)


if __name__ == '__main__':
    main()

