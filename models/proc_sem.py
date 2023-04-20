from models import LogicalForm, CheckQuery, VarCounter, SrcFlight, TgtFlight, DurFlight
from typing import List
from dataclasses import dataclass
import re


@dataclass
class WHQueryProc:
    var: List[str]

    def __repr__(self) -> str:
        return f"(QUERY {','.join([v for v in self.var])})"


class CheckQueryProc:
    def __repr__(self) -> str:
        return f"(CHECK)"


@dataclass
class FlightProc:
    flightname: str
    brandname: str

    def __repr__(self) -> str:
        return f"(FLIGHT {self.flightname} {self.brandname})"


@dataclass
class ATimeProc:
    flightname: str
    city: str
    time: str

    def __repr__(self) -> str:
        return f"(ATIME {self.flightname} {self.city} {self.time})"


@dataclass
class DTimeProc:
    flightname: str
    city: str
    time: str

    def __repr__(self) -> str:
        return f"(DTIME {self.flightname} {self.city} {self.time})"


@dataclass
class RTimeProc:
    flightname: str
    city1: str
    city2: str
    time: str

    def __repr__(self) -> str:
        return f"(RUN-TIME {self.flightname} {self.city1} {self.city2} {self.time})"


class ProcSemHelper:
    def __init__(self) -> None:
        self.city_mapper = {
            "Huế": "HUE",
            "Đà_Nẵng": "DN",
            "Hồ_Chí_Minh": "HCM",
            "Hà_Nội": "HN",
            "Khánh_Hòa": "KH",
            "Hải_Phòng": "HP"
        }

    def city_lookup(self, city_name: str) -> str:
        return self.city_mapper[city_name]

    def time_format(self, time: str) -> str:
        # input will be 45_phút, 1_giờ
        # format into 0:45HR, 1:00HR
        time_value, time_unit = time.split("_")
        if time_unit == "phút":
            return f"0:{time_value}HR"
        else:
            return f"{time_value}:00HR"


class ProceduralSem:
    def __init__(self, logic: LogicalForm) -> None:
        self.counter = VarCounter()
        self.helper = ProcSemHelper()
        if type(logic.query_param) == CheckQuery:
            self.query = CheckQueryProc()
        else:
            self.query = WHQueryProc(logic.query_param.var)

        self.flight = None
        if type(logic.flight.flight) == str:
            # flight query
            self.flight = FlightProc(
                self.query.var[0], self.counter.get_var("b"))
        else:
            text = logic.flight.flight.text
            if (text == "VietJet_Air" or text == "Vietnam_Airline"):
                # check if this is flight query or not
                if self.query.var[0][0] == 'f':
                    # flight query
                    self.flight = FlightProc(self.query.var[0], text.upper())
                else:
                    self.flight = FlightProc(
                        self.counter.get_var('f'), text.upper())
            else:
                self.flight = FlightProc(
                    text.upper(), self.counter.get_var("b"))

        self.flight_time = None
        if type(logic.flight) == SrcFlight:
            city = logic.flight.from_loc
            time = logic.flight.at_time
            if time is None:
                # variable
                at_time = self.counter.get_var('t')
            elif type(time) != str:
                # Name value
                at_time = time.text
            else:
                # str
                # query
                at_time = re.sub("\?", "", time)
            if type(city) == str:
                # variable
                city_name = city
            else:
                # Name
                city_name = self.helper.city_lookup(city.text)
            self.flight_time = DTimeProc(
                self.flight.flightname, city_name, at_time)
        elif type(logic.flight) == TgtFlight:
            city = logic.flight.to_loc
            time = logic.flight.at_time
            if time is None:
                # variable
                at_time = self.counter.get_var('t')
            elif type(time) != str:
                # Name value
                at_time = time.text
            else:
                # str
                # query
                at_time = re.sub("\?", "", time)
            if type(city) == str:
                # variable
                city_name = city
            else:
                # Name
                city_name = self.helper.city_lookup(city.text)
            self.flight_time = ATimeProc(
                self.flight.flightname, city_name, at_time)
        else:
            city1 = logic.flight.from_loc
            city2 = logic.flight.to_loc
            time = logic.flight.last_time
            if time is None:
                # variable
                last_time = self.counter.get_var('t')
            elif type(time) != str:
                # Name value
                last_time = self.helper.time_format(time.text)
            else:
                # str
                # query
                last_time = re.sub("\?", "", time)

            if type(city1) == str:
                # variable
                city_name1 = city1
            else:
                # Name
                city_name1 = self.helper.city_lookup(city1.text)

            if type(city2) == str:
                # variable
                city_name2 = city2
            else:
                # Name
                city_name2 = self.helper.city_lookup(city2.text)
            self.flight_time = RTimeProc(
                self.flight.flightname, city_name1, city_name2, last_time)

    def __repr__(self) -> str:
        return f"{self.query} (& {self.flight} {self.flight_time})"

    def easy_query(self) -> str:
        # Query will parse directly from this string, using this way, we can capture common variable
        # to select and link between table
        return re.sub("\(|\)", "", f"{self.query}+{self.flight}+{self.flight_time}")
