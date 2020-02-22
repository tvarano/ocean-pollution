import sqlite3 as sql

get_dense = lambda p, d: None if d == 0 else p/d

def init():
	conn = sql.connect("cleanup.db")
	curs = conn.cursor()
	return conn, curs

def close():
	conn.commit()
	conn.close()

def get_months_data():
	conn, curs = init()
	rows = curs.execute("select Month, Year, sum(Total_Items_Collected), sum(Miles), sum(Pounds) from cleanup where Year >= 2010 and Year < 2020 group by Month, Year order by Year ASC, Month ASC;")
	res = [(r[0], r[1], r[2], get_dense(r[4], r[3])) for r in rows]
	conn.close()
	return res

def get_month_data(month, year):
	conn, curs = init()
	rows = curs.execute('select zone, sum(Total_Items_Collected), sum(Miles), sum(Pounds), avg(Lat), avg(Long) from cleanup where Month=? and Year=? group by Zone order by Total_Items_Collected DESC', (month, year))
	res = {r[0]: {"num_items": r[1], "density": get_dense(r[3], r[2]), "lat":r[4], "lng": r[5]} for r in rows} 
	conn.close()
	return res

def get_zone_data(zone, month, year):
	conn, curs = init()
	rows = curs.execute('select Cleanup_ID, sum(Total_Items_Collected), sum(Miles), sum(Pounds), Lat, Long from cleanup where zone= ? and Month=? and Year=? group by lat, long order by Total_Items_Collected DESC', (zone, month, year))
	res = {r[0]: {"num_items": r[1], "desnity": get_dense(r[3], r[2]), "lat": r[4], "lng": r[5]} for r in rows}
	conn.close()
	return res

print(get_month_data(5, 2019))
print(get_zone_data('Kings County, Brooklyn, NY, USA', 5, 2019))

 

