import configparser
import json

from collections import defaultdict

config = configparser.ConfigParser()
config.read('./config.ini')

DIRECTIONS = json.loads(config.get('mapping', 'directions'))
STREET_TYPES = json.loads(config.get('mapping', 'street_types'))
OCCUPANCY_IDENTIFIERS = {'SUITE', 'STE', 'APTT'}
TRANSITIONS = json.loads(config.get('transitions', 'transitions'))
dispatch_table = {
                    'junk': lambda tkn: True,
                    'house_num': lambda tkn: tkn[0].isdigit(),
                    'pre_dir': lambda tkn: tkn in DIRECTIONS,
                    'str_nm': lambda tkn: True,
                    'str_type': lambda tkn: tkn in STREET_TYPES,
                    'post_dir': lambda tkn: tkn in DIRECTIONS,
                    'occ_id': lambda tkn: tkn in OCCUPANCY_IDENTIFIERS,
                    'occ_num': lambda tkn: True
                }


class Address:

    def __init__(self, address):
        self.address = address
        self.__labels = defaultdict(list)

        Address.__tag_components(self)

        self.house_num = ' '.join(self.__labels.get('house_num', ''))
        self.pre_dir = ' '.join(self.__labels.get('pre_dir', ''))
        self.str_nm = ' '.join(self.__labels.get('str_nm', ''))
        self.str_type = ' '.join(self.__labels.get('str_type', ''))
        self.post_dir = ' '.join(self.__labels.get('post_dir', ''))
        self.occ_id = ' '.join(self.__labels.get('occ_id', ''))
        self.occ_num = ' '.join(self.__labels.get('occ_num', ''))
        self.stdrd_addr = Address.__standardize_address(self)

    def __str__(self):
        return f'(House #: "{self.house_num}", ' \
               f'Pre-Direction: "{self.pre_dir}", ' \
               f'Street Name: "{self.str_nm}", ' \
               f'Street Type: "{self.str_type}", ' \
               f'Post-Direction: "{self.post_dir}", ' \
               f'Occupancy Identifier: "{self.occ_id}", ' \
               f'Occupancy #: "{self.occ_num}")'

    @staticmethod
    def __cleanse(addr):
        """
        Removes special characters from the address

        :param addr: Address
        :type addr: str
        :return: Cleansed Address
        :rtype: str
        """
        return addr.upper().replace('.', '')

    @staticmethod
    def __standardize_street_type(str_type):
        """
        Standardizes Street Types

        :param str_type: Street Type Label
        :type str_type: str
        :return: Standardized Street Type (e.g. 'AVENUE' -> 'AVE')
        :rtype: str
        """
        return STREET_TYPES.get(str_type, '')

    @staticmethod
    def __standardize_direction(direction):
        """
        Standardizes Street Directions

        :param direction: Pre/Post Direction Label
        :type direction: str
        :return: Standardized Direction (e.g. 'NORTHEAST' -> 'NE')
        :rtype: str
        """
        return DIRECTIONS.get(direction, '')
    
    def __tokenize(self):
        """
        Tokenizes the Address String

        :return: iterable of tokens
        """
        cleansed_addr = self.__cleanse(self.address)
        return iter(cleansed_addr.split()[::-1])

    def __tag_components(self):
        """
        Tags Address Component Labels to the tokens
        """
        tokens = self.__tokenize()
        current_tag = 'STOP'

        for token in tokens:
            next_tags = TRANSITIONS.get(current_tag, False)
            for tag in next_tags:
                if dispatch_table[tag](token):
                    current_tag = tag
                    break
            self.__labels[current_tag].insert(0, token)

    def __standardize_address(self):
        """
        Standardizes the input Address

        :return: Standardized Address
        :rtype: str
        """
        stdrd_tkns = [self.house_num, self.__standardize_direction(self.pre_dir),
                      self.str_nm, self.__standardize_street_type(self.str_type),
                      self.__standardize_direction(self.post_dir), self.occ_id,
                      self.occ_num]
        return ' '.join(filter(None, stdrd_tkns))


if __name__ == '__main__':

    addresses = ['318 Orange Street', '134 Jennings Ave.', '237 Tarkiln Hill St.',
                 '336 Bay Ave.', '111 Riverside Dr.', '380 Trout St.', '859 Roosevelt Road',
                 '8459 South Tower Drive', '276 Rock Creek Street', '17 Ridge St.',
                 '9160 Glenholme St.', '763 West Ketch Harbour Drive', '66 Amherst Street',
                 '962 East Shipley Lane', '9463 Saxon St.', '7814 Arlington Rd.', '39 Creekside Ave.',
                 '486 Van Dyke Rd.', '7074 Warren Dr.', '45 2nd Ave.', '8605 Lake Circle',
                 '102 Eagle Ave.', '93 Mammoth St.', '377 West Queen Ave.', '2 Peg Shop St.',
                 '34 Morris St.', '80 Williams Dr.', '329 North Chestnut Dr.', '629 River St.',
                 '323 Bayberry Ave.', '44 Oklahoma St.', '9137 Sleepy Hollow St.', '80 Greenrose St.',
                 '9338B Olive Drive', '97 Shirley St.', '158 Ridge Ave.', '19 Bank Dr.',
                 '994 East Garfield St.', '7179 Holly Ave.', '7515 Greystone Street',
                 '212 Newbridge Ave.', '378 Goldfield Ave.', '606 Shub Farm Ave.', '166 Nichols Street',
                 '8152B N Longfellow Street', '176 Bridgeton Road', '8955 Manor St.', '236 Lookout Street',
                 '31 Wayne Court', '936 Manhattan Dr.']

    for address_ in addresses:
        addr_ = Address(address_)
        print(addr_)

