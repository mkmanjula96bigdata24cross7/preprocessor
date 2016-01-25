"""
preprocessor.parse
~~~~~~~~~~~~
This module includes parse functionality

"""

import re
from .constants import Patterns
from .utils import Util

class ParseResult:
    urls = None
    hashtags = None
    mentions = None
    reserved_words = None

    def __init__(self):
        pass


class ParseItem:
    def __init__(self, start_index, end_index, match):
        self.start_index = start_index
        self.end_index = end_index
        self.match = match

    def __repr__(self):
        return '(%d:%d) => %s' % (self.start_index, self.end_index, self.match)


class Parse:

    def __init__(self):
        self.u = Util()

    def parse(self, tweet_string):
        parse_result_obj = ParseResult()

        parser_methods = self.u.get_worker_methods(self, 'parse_')

        for a_cleaner_method in parser_methods:
            method_to_call = getattr(self, a_cleaner_method)
            attr = a_cleaner_method.split('_')[1]

            items = method_to_call(tweet_string)
            setattr(parse_result_obj, attr, items)

        return parse_result_obj

    def parser(self, pattern, string):

        items = []

        for match_object in re.finditer(pattern, string):
            parse_item = ParseItem(match_object.start(), match_object.end(), match_object.group())
            items.append(parse_item)

        if len(items):
            return items

    def parse_urls(self, tweet_string):
        return self.parser(Patterns.URL_PATTERN, tweet_string)

    def parse_hashtags(self, tweet_string):
        return self.parser(Patterns.HASHTAG_PATTERN, tweet_string)

    def parse_mentions(self, tweet_string):
        return self.parser(Patterns.MENTION_PATTERN, tweet_string)

    def parse_reserved_words(self, tweet_string):
        return self.parser(Patterns.RESERVED_WORDS_PATTERN, tweet_string)
