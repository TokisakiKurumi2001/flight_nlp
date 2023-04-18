from models import Token
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple


class Arc(Enum):
    LEFT = 1
    RIGHT = 2


@dataclass
class Relation:
    name: str
    head: Token
    tail: Token

    def __repr__(self):
        return f"{self.name}({self.head} -> {self.tail})"


class Relations:
    def __init__(self):
        self.relations = {
            "FLIGHT-N+WH-QDET": "FLIGHT-QUERY",
            "FLIGHT-V+FLIGHT-N": "NSUBJ",
            "ROOT+FLIGHT-V": "ROOT",
            "FLIGHT-V+CITYNAME-N": "DOBJ",
            "CITYNAME-N+ARRIVE-P": "ARRIVE-CASE",
            "FLIGHT-V+TIME-NUM": "TIME-ADVMOD",
            "TIME-NUM+TIME-P": "ATTIME-NMOD",
            "FLIGHT-V+Q-PUNCT": "PUNCT",
            "CITYNAME-N+DEPART-P": "DEPART-CASE",
            "TIME-NUM+LAST-V": "LAST-NUMMOD",
            "FLIGHT-N+FLIGHTNAME-N": "FLIGHTNAME-NMOD",
            "TIME-N+WH-QDET": "TIME-QUERY",
            "FLIGHT-V+TIME-N": "TIME-ADVMOD",
            "FLIGHT-N+BRAND-N": "BRAND-NMOD",
            "BRAND-N+POSS-ADJ": "BRAND-APOSS",
            "CITY-N+ARRIVE-P": "ARRIVE-CASE",
            "FLIGHT-V+CITY-N": "DOBJ",
            "CITY-N+WH-QDET": "CITY-QUERY",
        }

    def lookup(self, tag1: str, tag2: str) -> Tuple[str, str]:
        if f"{tag1}+{tag2}" in self.relations:
            return self.relations[f"{tag1}+{tag2}"], Arc.RIGHT
        elif f"{tag2}+{tag1}" in self.relations:
            return self.relations[f"{tag2}+{tag1}"], Arc.LEFT
        else:
            return "", -1


class Action(Enum):
    SHIFT = 1
    LEFT = 2
    RIGHT = 3
    REDUCE = 4


class MaltParser:
    def __init__(self, tokens: List[Token]):
        self.input = tokens
        self.stack = [Token('root', 'ROOT')]
        self.relations = []
        self.relation_table = Relations()

    def act(self, action: Action, *args) -> None:
        if action == Action.SHIFT:
            self.stack.append(self.input.pop(0))
        elif action == Action.LEFT:
            tail = self.stack.pop(-1)
            head = self.input[0]
            self.relations.append(Relation(args[0], head, tail))
        elif action == Action.RIGHT:
            tail = self.input.pop(0)
            head = self.stack[-1]
            self.relations.append(Relation(args[0], head, tail))
            self.stack.append(tail)
        elif action == Action.REDUCE:
            self.stack.pop(-1)

    def __call__(self) -> List[Relations]:
        initial = True
        reducible = 0
        while (len(self.input) != 0):
            if initial:
                self.act(Action.SHIFT)
                initial = False
            tag1 = self.stack[-1].tag
            tag2 = self.input[0].tag
            relname, direction = self.relation_table.lookup(tag1, tag2)
            if direction == -1:
                # no relation
                if reducible > 0:
                    self.act(Action.REDUCE)
                    reducible -= 1
                else:
                    self.act(Action.SHIFT)
            elif direction == Arc.LEFT:
                self.act(Action.LEFT, relname)
            else:
                self.act(Action.RIGHT, relname)
                if relname == "ROOT":
                    pass
                elif len(self.input) > 0 and self.input[0].tag == "WH-QDET":
                    reducible += 1
                elif len(self.input) > 0 and self.input[0].tag == "Q-PUNCT":
                    reducible = len(self.stack) - 2
                else:
                    self.act(Action.REDUCE)
            # breakpoint()

        return self.relations
