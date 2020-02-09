# -*- coding: utf-8 -*-

class Spider:
    def get_page(self, address):
        raise NotImplementedError

    def parse_page(self, page):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError
