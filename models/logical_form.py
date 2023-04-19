from models import GrammarRelation, QueryType
import string
from dataclasses import dataclass
from typing import List, Union, Optional
from models.utils import no_accent_vietnamese


@dataclass
class Name:
    var: str
    text: str

    def __repr__(self) -> str:
        return f"(NAME {self.var} {self.text})"


@dataclass
class Query:
    var: List[str]

    def __repr__(self) -> str:
        return f"(QUERY {','.join([f'?{v}' for v in self.var])})"


class CheckQuery:
    def __repr__(self) -> str:
        return f"(CHECK)"


@dataclass
class TgtFlight:
    flight: Union[str, Name]
    to_loc: Union[str, Name]
    at_time: Optional[Union[Name, str]] = None

    def __repr__(self) -> str:
        flight = f"?{self.flight}" if type(self.flight) == str else self.flight
        to_loc = f"?{self.to_loc}" if type(self.to_loc) == str else self.to_loc
        if self.at_time is not None:
            return f"(TGT-FLIGHT {flight} (TO-LOC {to_loc}) (AT-TIME {self.at_time}))"
        else:
            return f"(TGT-FLIGHT {flight} (TO-LOC {to_loc}))"


@dataclass
class SrcFlight:
    flight: Union[str, Name]
    from_loc: Union[str, Name]
    at_time: Optional[Union[Name, str]] = None

    def __repr__(self) -> str:
        flight = f"?{self.flight}" if type(self.flight) == str else self.flight
        from_loc = f"?{self.from_loc}" if type(
            self.from_loc) == str else self.from_loc
        if self.at_time is not None:
            return f"(SRC-FLIGHT {flight} (FROM-LOC {from_loc}) (AT-TIME {self.at_time}))"
        else:
            return f"(SRC-FLIGHT {flight} (FROM-LOC {from_loc}))"


@dataclass
class DurFlight:
    flight: Union[str, Name]
    from_loc: Union[str, Name]
    to_loc: Union[str, Name]
    last_time: Optional[Union[Name, str]] = None

    def __repr__(self) -> str:
        flight = f"?{self.flight}" if type(self.flight) == str else self.flight
        to_loc = f"?{self.to_loc}" if type(self.to_loc) == str else self.to_loc
        from_loc = f"?{self.from_loc}" if type(
            self.from_loc) == str else self.from_loc
        if self.last_time is not None:
            return f"(DUR-FLIGHT {flight} (FROM-LOC {from_loc}) (TO-LOC {to_loc}) (LAST-TIME {self.last_time}))"
        else:
            return f"(DUR-FLIGHT {flight} (FROM-LOC {from_loc}) (TO-LOC {to_loc}))"


class VarCounter:
    def __init__(self):
        self.dict = {k: 1 for k in string.ascii_lowercase}

    def get_var(self, c: str):
        c = no_accent_vietnamese(c)
        v = self.dict[c]
        self.dict[c] += 1
        return f"{c}{v}"


class LogicalForm:
    def __init__(self, rel: GrammarRelation):
        self.counter = VarCounter()

        # query
        query = []
        self.query_param = None
        if rel.query_type != QueryType.VERIFY:
            query.append(self.counter.get_var(rel.query_type.name[0].lower()))
            if rel.second_query:
                query.append(self.counter.get_var(
                    rel.second_query_type.name[0].lower()))
            self.query_param = Query(query)
        else:
            self.query_param = CheckQuery()

        # flight
        if rel.query_type == QueryType.FLIGHT:
            flight_name = query[0]
        else:
            flight_name = rel.lsubj

        self.flight = None

        # to-loc + from-loc --> DurFlight
        # from-loc --> SrcFlight
        # to-loc --> TgtFlight
        if rel.to_loc is not None and rel.from_loc is not None:
            if type(rel.from_loc) != str and type(rel.to_loc) != str:
                # Name type
                from_loc_text = rel.from_loc.text
                from_loc_var = self.counter.get_var(from_loc_text[0].lower())
                from_loc_name = Name(from_loc_var, from_loc_text)

                to_loc_text = rel.to_loc.text
                to_loc_var = self.counter.get_var(to_loc_text[0].lower())
                to_loc_name = Name(to_loc_var, to_loc_text)

                last_time_name = None
                if rel.last_time is not None or (rel.second_query and rel.second_last_time is not None):
                    if rel.last_time is not None and rel.last_time != "?":
                        last_time_var = self.counter.get_var('t')
                        last_time_name = Name(last_time_var, rel.last_time)
                    else:
                        # time query
                        last_time_name = f"?{query[-1]}"

                self.flight = DurFlight(
                    flight_name, from_loc_name, to_loc_name, last_time_name)

        elif rel.to_loc is not None:
            if type(rel.to_loc) != str:
                # Name type
                to_loc_text = rel.to_loc.text
                to_loc_var = self.counter.get_var(to_loc_text[0].lower())
                to_loc_name = Name(to_loc_var, to_loc_text)

                at_time_name = None
                if rel.at_time is not None or (rel.second_query and rel.second_at_time is not None):
                    if rel.at_time is not None and rel.at_time != "?":
                        at_time_var = self.counter.get_var('t')
                        at_time_name = Name(at_time_var, rel.at_time)
                    else:
                        # time query
                        at_time_name = f"?{query[-1]}"
                self.flight = TgtFlight(flight_name, to_loc_name, at_time_name)
            else:
                # ask for city
                to_loc_name = query[0]
                self.flight = TgtFlight(flight_name, to_loc_name)

        elif rel.from_loc is not None:
            if type(rel.from_loc) != str:
                # Name type
                from_loc_text = rel.from_loc.text
                from_loc_var = self.counter.get_var(from_loc_text[0].lower())
                from_loc_name = Name(from_loc_var, from_loc_text)

                at_time_name = None
                if rel.at_time is not None or (rel.second_query and rel.second_at_time is not None):
                    if rel.at_time is not None and rel.at_time != "?":
                        at_time_var = self.counter.get_var('t')
                        at_time_name = Name(at_time_var, rel.at_time)
                    else:
                        # time query
                        at_time_name = f"?{query[-1]}"
                self.flight = SrcFlight(
                    flight_name, from_loc_name, at_time_name)
            else:
                # ask for city
                from_loc_name = query[0]
                self.flight = SrcFlight(flight_name, from_loc_name)

    def __repr__(self) -> str:
        return f"{self.query_param} {self.flight}"
