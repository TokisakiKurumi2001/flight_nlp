from dataclasses import dataclass
from typing import List
import re


@dataclass
class Token:
    text: str
    tag: str

    def __repr__(self):
        return f"{{ \"text\": \"{self.text}\", \"tag\": \"{self.tag}\" }}"


class WordSegmentor:
    def __init__(self):
        self.words = ["Máy bay", "Thành phố", "Đà Nẵng", "Hồ Chí Minh", "cho biết", "mã hiệu", "hạ cánh", "xuất phát",
                      "Hà Nội", "Thời gian", "Khánh Hòa", "Hải Phòng", "hãng hàng không", "VietJet Air", "Vietname Airline"]

    def __call__(self, sent: str) -> str:
        for word in self.words:
            sent = re.sub(word, word.replace(" ", "_"), sent)
            sent = re.sub(word.lower(), word.lower().replace(" ", "_"), sent)

        # 1 giờ, 42 phút will be merged
        sent = re.sub("(\d+)\s(giờ|phút)", r"\1_\2", sent)
        return sent


class Tokenizer:
    def __init__(self):
        self.word_segmentor = WordSegmentor()

    def normalize(self, sent: str):
        """
        - Remove the punctuation dot '.' if exists at the end of the question
        - Convert Tp., TP, TP.,thành phố into "Thành phố"
        - Add around punctuation
        - Remove redundant spaces if exists
        """
        if sent[-1] == '.':
            sent = sent[:-1]

        sent = re.sub("TP.|Tp.|TP|Tp|thành phố", "Thành phố ", sent)
        sent = re.sub('([.,!?()])', r' \1 ', sent)
        sent = re.sub('\s{2,}', ' ', sent)
        return sent

    def tokenize(self, sent: str, normalized: bool = True) -> List[str]:
        if normalized:
            sent = self.normalize(sent)
        segmented_sent = self.word_segmentor(sent)
        return segmented_sent.split(" ")
