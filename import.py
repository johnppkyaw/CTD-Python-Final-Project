import csv, sqlite3

try:
  with sqlite3.connect('db/baseball.db') as conn:
    cursor = conn.cursor()

    cursor.execute("""
    DROP TABLE IF EXISTS Hitters
    """)

    cursor.execute("""
    DROP TABLE IF EXISTS Pitchers
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Hitters (
        row_id INTEGER PRIMARY KEY,
        Year INTEGER NOT NULL,
        Statistic TEXT NOT NULL,
        Name TEXT NOT NULL,
        Team TEXT NOT NULL,
        Value REAL NOT NULL        
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Pitchers (
        row_id INTEGER PRIMARY KEY,
        Year INTEGER NOT NULL,
        Statistic TEXT NOT NULL,
        Name TEXT NOT NULL,
        Team TEXT NOT NULL,
        Value REAL NOT NULL        
    )
    """)


  with open('hitting_player_stats.csv', 'r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['Year'], i['Statistic'], i['Name'], i['Team'], i['Value']) for i in dr]

  cursor.executemany("INSERT INTO Hitters (Year, Statistic, Name, Team, Value) VALUES (?, ?, ?, ?, ?);", to_db)

  with open('pitching_player_stats.csv', 'r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['Year'], i['Statistic'], i['Name'], i['Team'], i['Value']) for i in dr]

  cursor.executemany("INSERT INTO Pitchers (Year, Statistic, Name, Team, Value) VALUES (?, ?, ?, ?, ?);", to_db)

  conn.commit()
  conn.close()

except sqlite3.OperationalError as e:
  print(e) 
