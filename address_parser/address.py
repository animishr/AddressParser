from collections import defaultdict

from utils.config import DISPATCH_TABLE, TRANSITIONS
from utils.format_strings import tokenize
from utils.standardize import standardize_direction, standardize_street_type


class Address:

    def __init__(self, address):
        self.address = address
        self.__labels = defaultdict(list)
        Address.__tag_components(self)

    def __str__(self):
        return f'(House #: "{self.house_num}", ' \
               f'Pre-Direction: "{self.pre_dir}", ' \
               f'Street Name: "{self.str_nm}", ' \
               f'Street Type: "{self.str_type}", ' \
               f'Post-Direction: "{self.post_dir}", ' \
               f'Occupancy Identifier: "{self.occ_id}", ' \
               f'Occupancy #: "{self.occ_num}")'

    def __tag_components(self):
        """
        Tags Address Component Labels to the tokens
        """
        tokens = tokenize(self.address)
        current_tag = 'STOP'

        for token in tokens:
            next_tags = TRANSITIONS.get(current_tag, False)
            for tag in next_tags:
                if DISPATCH_TABLE[tag](token):
                    current_tag = tag
                    break
            self.__labels[current_tag].insert(0, token)

    @property
    def house_num(self):
        return ' '.join(self.__labels.get('house_num', ''))

    @property
    def pre_dir(self):
        return ' '.join(self.__labels.get('pre_dir', ''))

    @property
    def str_nm(self):
        return ' '.join(self.__labels.get('str_nm', ''))

    @property
    def str_type(self):
        return ' '.join(self.__labels.get('str_type', ''))

    @property
    def post_dir(self):
        return ' '.join(self.__labels.get('post_dir', ''))

    @property
    def occ_id(self):
        return ' '.join(self.__labels.get('occ_id', ''))

    @property
    def occ_num(self):
        return ' '.join(self.__labels.get('occ_num', ''))

    def __standardize_address(self):
        """
        Standardizes the input Address

        :return: Standardized Address
        :rtype: str
        """
        stdrd_tkns = [self.house_num,
                      standardize_direction(self.pre_dir),
                      self.str_nm,
                      standardize_street_type(self.str_type),
                      standardize_direction(self.post_dir),
                      self.occ_id,
                      self.occ_num]
        return ' '.join(filter(None, stdrd_tkns))

    @property
    def standardized_address(self):
        return self.__standardize_address()

    @property
    def components(self):
        tags = {}
        for tag in self.__labels:
            value = ' '.join(self.__labels.get(tag, ''))
            if value:
                tags[tag] = value
            else:
                pass
        return tags