import sqlite3 as sql

conn = sql.connect("cleanup.db")
curs = conn.cursor()

get_dense = lambda p, d: None if d == 0 else p/d

def get_months_data():
	rows = curs.execute("select Month, Year, sum(Total_Items_Collected) from cleanup where Year >= 2010 and Year < 2020 group by Month, Year order by Year ASC, Month ASC;")
	return [(r[0], r[1], r[2]) for r in rows]

def get_month_data(month, year):
	rows = curs.execute('select zone, sum(Total_Items_Collected), sum(Miles), sum(Pounds), avg(Lat), avg(Long) from cleanup where Month=? and Year=? group by Zone order by Total_Items_Collected DESC', (month, year))
	return [(r[0], r[1], get_dense(r[3], r[2]), r[4], r[5]) for r in rows]  



