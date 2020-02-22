import sqlite3 as sql

get_dense = lambda p, d: None if d == 0 else p/d
filters = ["id", "zone", "state", "country", "gps", "lat", "long", "type", "date", "month", "date", "year", "group", "adults", "children", "people", "pounds", "miles", "bags", "cigarretes", "food_wrappers", "take_out_plastic", "take_out_foam", "bottle_caps_plastic", "bottle_caps_metal", "lids_plastic", "staws_stirrers", "forks_knives_spoons", "bottles_plastic", "bottles_glass", "cans", "bags_plastic", "bags_plastic", "paper_bags", "paper_plates", "plastic_plates", "foam_plates"]

def init():
	conn = sql.connect("cleanup.db")
	curs = conn.cursor()
	return conn, curs

def close():
	conn.commit()
	conn.close()

def get_data():
	conn, curs = init()
	rows = curs.execute("select sum(Total_Items_Collected), sum(Miles), sum(Pounds), sum(People), sum(Adults) from cleanup where Year >= 2010 and Year < 2020;")
	r = [r for r in rows][0]
	res = {"num_items":r[0], "pounds/mile": get_dense(r[2], r[1]), "pounds/people": get_dense(r[2], r[3]), "pounds/adult": get_dense(r[2], r[4])}
	conn.close()
	return res
	
def get_months_data():
	conn, curs = init()
	rows = curs.execute("select Month, Year, sum(Total_Items_Collected), sum(Miles), sum(Pounds), sum(People), sum(Adults)  from cleanup where Year >= 2010 and Year < 2020 group by Month, Year order by Year ASC, Month ASC;")
	res = {(r[0], r[1]): {"num_items":r[2], "pounds/mile": get_dense(r[4], r[3]), "pounds/people": get_dense(r[4], r[5]), "pounds/adults": get_dense(r[4], r[6])} for r in rows}
	conn.close()
	return res

def get_month_data(month, year, filters=None):
	conn, curs = init()
	rows = curs.execute('select zone, sum(Total_Items_Collected), sum(Miles), sum(Pounds), avg(Lat), avg(Long), sum(People), sum(Adults) from cleanup where Month=? and Year=? group by Zone order by Total_Items_Collected DESC', (month, year))
	res = {r[0]: {"num_items": r[1], "pounds/mile": get_dense(r[3], r[2]), "lat":r[4], "lng": r[5], "pounds/people": get_dense(r[3], r[6]), "pounds/adults": get_dense(r[3], r[7])} for r in rows} 
	conn.close()
	return res

def get_zone_data(zone, month, year, filters=None):
	conn, curs = init()
	rows = curs.execute('select Cleanup_ID, sum(Total_Items_Collected), sum(Miles), sum(Pounds), Lat, Long, sum(People), sum(Adults) from cleanup where zone= ? and Month=? and Year=? group by lat, long order by Total_Items_Collected DESC', (zone, month, year))
	res = {r[0]: {"num_items": r[1], "desnity": get_dense(r[3], r[2]), "lat": r[4], "lng": r[5], "pounds/people": get_dense(r[3], r[6]), "pounds/adults": get_dense(r[3], r[7])} for r in rows}
	conn.close()
	return res

if __name__ == '__main__':
	print(get_data(), end="\n\n")
	print(get_months_data(), end="\n\n")
	print(get_month_data(5, 2019), end="\n\n")
	print(get_zone_data('Kings County, Brooklyn, NY, USA', 5, 2019), end="\n\n")

 

