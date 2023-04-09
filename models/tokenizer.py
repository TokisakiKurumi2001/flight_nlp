from dataclasses import dataclass
from typing import List
import re

@dataclass
class Token:
    text: str
    pos_tags: List[str]
    pos: str

    def __repr__(self):
        return f"\{'text': {text}, 'pos_tags': [{[pos_tag for pos_tag in pos_tags]}], 'pos': {pos}\}"

class WordSegmentor:
    def __init__(self):
        self.words = ["Máy bay", "Thành phố", "Đà Nẵng", "Hồ Chí Minh", "cho biết", "mã hiệu", "hạ cánh", "xuất phát", "Hà Nội", "Thời gian", "Khánh Hòa", "Hải Phòng", "hãng hàng không", "VietJet Air", "Vietname Airline"]

    def __call__(self, sent: str) -> str:
        for word in self.words:
            sent = re.sub(word, word.replace(" ", "_"), sent)
            sent = re.sub(word.lower(), word.lower().replace(" ", "_"), sent)
        return sent

class Tokenizer:
    def __init__(self):
        self.word_segmentor = WordSegmentor()
    
    def normalize(self, sent: str):
        """
        - Remove the punctuation dot '.' if exists at the end of the question
        - Convert Tp., TP, TP.,thành phố into "Thành phố"
        - Remove redundant spaces if exists
        """
        if sent[-1] == '.':
            sent = sent[:-1]

        sent = re.sub("TP.|Tp.|TP|Tp|thành phố", "Thành phố ", sent)
        sent = re.sub("\s+", " ", sent)
        return sent

    def tokenize(self, sent: str, normalized: bool = True) -> List[str]:
        if normalized:
            sent = self.normalize(sent)
        segmented_sent = self.word_segmentor(sent)
        return segmented_sent.split(" ")
