from typing import List
from models import Relation
from enum import Enum
from dataclasses import dataclass


@dataclass
class Name:
    text: str

    def __repr__(self) -> str:
        return f"(NAME {self.text})"


@dataclass
class Brand:
    text: str

    def __repr__(self) -> str:
        return f"(BRAND {self.text})"


class QueryType(Enum):
    FLIGHT = 1
    TIME = 2
    CITY = 3
    VERIFY = 4


class GrammarRelation:
    def __init__(self, dep_ls: List[Relation]):
        self.dep_ls = dep_ls

        self.query_type = None
        self.lsubj = None
        self.pred = "Bay"
        self.to_loc = None
        self.from_loc = None
        self.at_time = None
        self.last_time = None

        self.second_query = False
        self.second_query_type = None
        self.second_at_time = None
        self.second_last_time = None

        for el in self.dep_ls:
            rel_name = el.name
            if rel_name == "FLIGHT-QUERY":
                self.query_type = QueryType.FLIGHT
                self.lsubj = "Máy_bay"
            elif rel_name == "TIME-QUERY":
                if self.query_type is not None:
                    self.second_query = True
                    self.second_query_type = QueryType.TIME
                else:
                    self.query_type = QueryType.TIME
            elif rel_name == "CITY-QUERY":
                self.query_type = QueryType.CITY
            elif rel_name == "ARRIVE-CASE":
                if self.query_type in [QueryType.FLIGHT, QueryType.TIME]:
                    self.to_loc = Name(el.head.text)
                elif el.head.tag == "CITYNAME-N":
                    self.to_loc = Name(el.head.text)
                else:
                    # city query
                    self.to_loc = "?"
            elif rel_name == "DEPART-CASE":
                if self.query_type in [QueryType.FLIGHT, QueryType.TIME]:
                    self.from_loc = Name(el.head.text)
                elif el.head.tag == "CITYNAME-N":
                    self.from_loc = Name(el.head.text)
                else:
                    # city query
                    self.from_loc = "?"
            elif rel_name == "ATTIME-NMOD":
                if not self.second_query:
                    if self.query_type != QueryType.TIME:
                        self.at_time = el.head.text
                    else:
                        self.at_time = "?"
                else:
                    if self.second_query_type != QueryType.TIME:
                        self.second_at_time = el.head.text
                    else:
                        self.second_at_time = "?"
            elif rel_name == "LAST-NUMMOD":
                if not self.second_query:
                    if self.query_type != QueryType.TIME:
                        self.last_time = el.head.text
                    else:
                        self.last_time = "?"
                else:
                    if self.second_query_type != QueryType.TIME:
                        self.second_last_time = el.head.text
                    else:
                        self.second_last_time = "?"
            elif rel_name == "FLIGHTNAME-NMOD":
                self.lsubj = Name(el.tail.text)
            elif rel_name == "BRAND-NMOD":
                self.lsubj = Brand(el.tail.text)

        if self.query_type is None:
            self.query_type = QueryType.VERIFY

        if self.query_type == QueryType.TIME:
            if self.at_time is None:
                self.last_time = "?"

    def __repr__(self) -> str:
        rt_str = ""
        # query type
        rt_str += f"(s1 QUERY {self.query_type.name})"
        rt_str += "\n"
        # pred
        rt_str += f"(s1 PRED Bay)"
        rt_str += "\n"
        # lsubj
        if self.lsubj is not None:
            rt_str += f"(s1 LSUBJ {self.lsubj})"
        rt_str += "\n"
        # from-loc
        if self.from_loc is not None:
            rt_str += f"(s1 FROM-LOC {self.from_loc})"
            rt_str += "\n"
        # to-loc
        if self.to_loc is not None:
            rt_str += f"(s1 TO-LOC {self.to_loc})"
            rt_str += "\n"
        # at-time
        if self.at_time is not None:
            rt_str += f"(s1 AT-TIME {self.at_time})"
            rt_str += "\n"
        # last-time
        if self.last_time is not None:
            rt_str += f"(s1 LAST-TIME {self.last_time})"
            rt_str += "\n"

        # check second query
        if not self.second_query:
            return rt_str

        rt_str += f"(s2 QUERY {self.second_query_type.name})"
        rt_str += "\n"
        # pred
        rt_str += f"(s2 PRED Bay)"
        rt_str += "\n"
        # lsubj
        if self.lsubj is not None:
            rt_str += f"(s2 LSUBJ {self.lsubj})"
        rt_str += "\n"
        # from-loc
        if self.from_loc is not None:
            rt_str += f"(s2 FROM-LOC {self.from_loc})"
            rt_str += "\n"
        # to-loc
        if self.to_loc is not None:
            rt_str += f"(s2 TO-LOC {self.to_loc})"
            rt_str += "\n"
        # at-time
        if self.second_at_time is not None:
            rt_str += f"(s2 AT-TIME {self.second_at_time})"
            rt_str += "\n"
        # last-time
        if self.second_last_time is not None:
            rt_str += f"(s2 LAST-TIME {self.second_last_time})"
            rt_str += "\n"

        return rt_str
