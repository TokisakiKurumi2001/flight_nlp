import string
from typing import List
import sqlite3


class DBQueryHelper:
    def __init__(self):
        self.table_map = {
            "FLIGHT": "FLIGHTS",
            "ATIME": "ARRIVES",
            "DTIME": "DEPARTS",
            "RUN-TIME": "RUNS",
        }

        self.table_schema = {
            "FLIGHTS": ['ID', 'BRAND'],
            "ARRIVES": ['ID', 'CITY', 'TIME'],
            "DEPARTS": ['ID', 'CITY', 'TIME'],
            "RUNS": ['ID', 'CITY1', 'CITY2', 'TIME'],
        }

        self.city_abbr_reverse_map = {
            "HUE": "Huế",
            "DN": "Đà Nẵng",
            "HCM": "Hồ Chí Minh",
            "HN": "Hà Nội",
            "KH": "Khánh Hòa",
            "HP": "Hải Phòng",
        }

    def islower(self, c: str) -> bool:
        return c in string.ascii_lowercase

    def isupper(self, c: str) -> bool:
        return c in string.ascii_uppercase

    def lookup_table(self, name: str) -> str:
        return self.table_map[name]

    def lookup_schema(self, name: str) -> List[str]:
        return self.table_schema[name]

    def convert_abbr(self, name: str) -> str:
        if name.startswith('V'):
            # flight name
            return name
        elif name[0].isnumeric():
            # time
            return name
        else:
            return self.city_abbr_reverse_map[name]


class QueryTransform:
    def __init__(self, proc_sem: str):
        self.helper = DBQueryHelper()
        query_type, flightname, flighttype = proc_sem.split("+")

        # answer postprocess
        self.answer_engineer = None
        if query_type == "CHECK":
            self.answer_engineer = "check"

        # main query
        self.query = ""
        # SELECT {query_var} FROM {main_table} [JOIN {}] WHERE {};
        query_var = []
        if query_type != "CHECK":
            query_var = query_type.split(" ")[1].split(",")

        # ignore flight table or not
        _, flight_name, brand_name = flightname.split(" ")
        ignore_flight_table = False
        if self.helper.islower(brand_name[0]) or self.helper.isupper(flight_name[0]):
            # if the brand is lower --> variable, but no query ask for brandname --> ignore flight
            # since flight name will appear on other table as well
            # if the flightname is upper --> already know the flight name --> does not need for flight table
            ignore_flight_table = True

        # decide the main table, other table (if have) will be secondary table to join
        main_table = None
        flighttype_table = flighttype.split(" ")[0]
        main_table = self.helper.lookup_table(flighttype_table)

        # secondary table and join
        tables = []
        join = ""
        tables.append(main_table)
        if not ignore_flight_table:
            # tables.append(self.helper.lookup_table("FLIGHT"))
            join = f" INNER JOIN FLIGHTS ON {main_table}.ID = FLIGHTS.ID"

        # condition & query column
        condition = []
        query_col = []
        schema = self.helper.lookup_schema(main_table)
        filled_schema = {x[0]: x[1]
                         for x in zip(schema, flighttype.split(" ")[1:])}
        for k, v in filled_schema.items():
            if self.helper.isupper(v[0]) or v[0].isnumeric():
                condition.append(f"{main_table}.{k} = \"{v}\"")
            if self.helper.islower(v[0]):
                if v in query_var:
                    query_col.append(k)

        if not ignore_flight_table:
            flight_schema = self.helper.lookup_schema("FLIGHTS")
            filled_schema = {x[0]: x[1] for x in zip(
                flight_schema, flightname.split(" ")[1:])}
            for k, v in filled_schema.items():
                if self.helper.isupper(v[0]):
                    condition.append(f"FLIGHTS.{k} = \"{v}\"")

        condition_str = " AND ".join(condition)

        table_str = ",".join(tables)
        if len(query_col) > 0:
            # normal query
            query_var_str = ",".join(
                [f"{main_table}.{col}" for col in query_col])
        else:
            # check query
            query_var_str = "*"

        self.query = f"SELECT {query_var_str} FROM {table_str}{join} WHERE {condition_str};"

    def __repr__(self) -> str:
        return self.query


class QueryDB:
    def __init__(self, db: str) -> None:
        try:
            self.conn = sqlite3.connect(db)
            self.helper = DBQueryHelper()
        except:
            raise Exception('Please make the database first')

    def query_db(self, query: QueryTransform):
        cursor = self.conn.execute(query.query)
        res = []

        check_flag = False
        if query.answer_engineer is not None:
            check_flag = True

        for row in cursor:
            if check_flag:
                res.append("YES")
            else:
                if len(row) == 1:
                    # ask for 1 columns
                    res.append(self.helper.convert_abbr(row[0]))
                elif len(row) == 2:
                    # ask for 2 columns
                    res.append((self.helper.convert_abbr(
                        row[0]), self.helper.convert_abbr(row[1])))

        if len(res) == 0:
            res.append("NO")
        return res

    def close(self):
        self.conn.close()
