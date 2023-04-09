import sqlite3
conn = sqlite3.connect('nlp.db')
conn.execute('''CREATE TABLE FLIGHTS (ID TEXT PRIMARY KEY NOT NULL);''')
conn.execute('''CREATE TABLE ARRIVES (ID TEXT PRIMARY KEY NOT NULL, CITY TEXT NOT NULL, TIME TEXT NOT NULL);''')
conn.execute('''CREATE TABLE DEPARTS (ID TEXT PRIMARY KEY NOT NULL, CITY TEXT NOT NULL, TIME TEXT NOT NULL);''')
conn.execute('''CREATE TABLE RUNS (ID TEXT PRIMARY KEY NOT NULL, CITY1 TEXT NOT NULL, CITY2 TEXT NOT NULL, TIME TEXT NOT NULL);''')

conn.execute("INSERT INTO FLIGHTS (ID) VALUES ('VN1'), ('VN2'), ('VN3'), ('VN4'), ('VN5'), ('VJ1'), ('VJ2'), ('VJ3'), ('VJ4'), ('VJ5');")
conn.execute("INSERT INTO ARRIVES (ID, CITY, TIME) VALUES ('VN1', 'HUE', '11:00HR'), ('VN2', 'HCM', '16:30HR'), ('VN3', 'HN', '6:30HR'), ('VN4', 'DN', '11:30HR'), ('VN5', 'KH', '17:45HR');")
conn.execute("INSERT INTO ARRIVES (ID, CITY, TIME) VALUES ('VJ1', 'HUE', '13:30HR'), ('VJ2', 'HN', '11:00HR'), ('VJ3', 'HP', '11:45HR'), ('VJ4', 'DN', '9:30HR'), ('VJ5', 'KH', '10:45HR');")
conn.execute("INSERT INTO DEPARTS (ID, CITY, TIME) VALUES ('VN1', 'HCM', '10:00HR'), ('VN2', 'DN', '15:30HR'), ('VN3', 'HCM', '4:30HR'), ('VN4', 'HN', '9:30HR'), ('VN5', 'HCM', '17:00HR');")
conn.execute("INSERT INTO DEPARTS (ID, CITY, TIME) VALUES ('VJ1', 'HN', '13:00HR'), ('VJ2', 'DN', '9:30HR'), ('VJ3', 'HCM', '9:45HR'), ('VJ4', 'HCM', '8:30HR'), ('VJ5', 'HN', '9:00HR');")
conn.execute("INSERT INTO RUNS (ID, CITY1, CITY2, TIME) VALUES ('VN1', 'HCM', 'HUE', '1:00HR'), ('VN2', 'DN', 'HCM', '1:00HR'), ('VN3', 'HCM', 'HN', '2:00HR'), ('VN4', 'HN', 'DN', '2:00HR'), ('VN5', 'HCM', 'KH', '00:45HR');")
conn.execute("INSERT INTO RUNS (ID, CITY1, CITY2, TIME) VALUES ('VJ1', 'HN', 'HUE', '1:00HR'), ('VJ2', 'DN', 'HN', '1:30HR'), ('VJ3', 'HCM', 'HP', '2:00HR'), ('VJ4', 'HCM', 'DN', '1:00HR'), ('VJ5', 'HN', 'KH', '1:45HR');")
conn.commit()
conn.close()