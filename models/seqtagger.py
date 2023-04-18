from typing import List
from models.utils import remove_items, add_items, flatten
from models import Token
import re


class SequenceTagger:
    def __init__(self):
        self.stopwords = ['Hãy', 'không', 'Có', 'các', 'không?',
                          'mã_hiệu', 'có', 'những', 'ở', 'hãng_hàng_không', 'Thời_gian']
        self.exact_match = {
            "Máy_bay": "FLIGHT-N",
            "nào": "WH-QDET",
            "bay": "FLIGHT-V",
            "đến": "ARRIVE-P",
            "Huế": "CITYNAME-N",
            "lúc": "TIME-P",
            # "13:30HR": 'TIME-NUM'
            "?": "Q-PUNCT",
            "từ": "DEPART-P",
            "Đà_Nẵng": "CITYNAME-N",
            "mất": "LAST-V",
            # "1_giờ": "TIME-NUM"
            "giờ": "TIME-N",
            "cho_biết": "WH-QDET",
            "máy_bay": "FLIGHT-N",
            ",": "C-PUNCT",
            "mấy": "WH-QDET",
            "Hà_Nội": "CITYNAME-N",
            # VN4: 'FLIGHTNAME-N'
            "Hồ_Chí_Minh": "CITYNAME-N",
            "Khánh_Hòa": "CITYNAME-N",
            "Hải_Phòng": "CITYNAME-N",
            "của": "POSS-ADJ",
            "VietJet_Air": "BRAND-N",
            "Vietnam_Airline": "BRAND-N",
            "Thành_phố": "CITY-N",
        }

    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """
        - Remove unneccessary word from the sentence to parse easier
            + Some stopwords are defined in self.stopwords
            + Some stopwords such as "Thành_phố" will be checked with special rules
        - Remove token with length == 0
        """
        rm_idxes = []
        city_names = ['Hồ_Chí_Minh', 'Huế', 'Đà_Nẵng',
                      'Hải_Phòng', 'Hà_Nội', 'Khánh_Hòa']
        for i, token in enumerate(tokens):
            if token in self.stopwords:
                rm_idxes.append(i)

            if token == "Thành_phố" and tokens[i + 1] in city_names:
                rm_idxes.append(i)

            if token == "mất" and tokens[i+1] == "mấy":
                rm_idxes.append(i)
        # print(tokens)
        # breakpoint()
        return list(filter(lambda x: len(x) > 0, remove_items(tokens, rm_idxes)))

    def add_words(self, tokens: List[str]) -> List[str]:
        city_names = ['Hồ_Chí_Minh', 'Huế', 'Đà_Nẵng',
                      'Hải_Phòng', 'Hà_Nội', 'Khánh_Hòa']
        add_idxes = []
        add_words = []
        for i, token in enumerate(tokens):
            if token == "đến" and tokens[i-1] == "nào" and tokens[i+1] in city_names:
                add_idxes.append(i)
                add_words.append("bay")

        return add_items(tokens, add_idxes, add_words)

    def replace_words(self, tokens: List[str]) -> List[str]:
        self.map = {
            "hạ_cánh": ["bay", "đến"],
            "xuất_phát": "bay"
        }
        for i, token in enumerate(tokens):
            for k, v in self.map.items():
                if token == k:
                    tokens[i] = v

        return flatten(tokens)

    def __preprocess(self, ls: List[str]) -> List[str]:
        tokens = self.remove_stopwords(ls)
        tokens = self.add_words(tokens)
        tokens = self.replace_words(tokens)
        return tokens

    def __call__(self, tokens: List[str]) -> List[Token]:
        ls = []
        tokens = self.__preprocess(tokens)
        for token in tokens:
            if re.search('\d+_(giờ|phút)', token) is not None:
                ls.append(Token(token, 'TIME-NUM'))
            elif re.search('\d{2}:\d{2}HR', token) is not None:
                ls.append(Token(token, 'TIME-NUM'))
            elif re.search('V(J|N)\d', token) is not None:
                ls.append(Token(token, 'FLIGHTNAME-N'))
            else:
                ls.append(Token(token, self.exact_match[token]))
        return ls
