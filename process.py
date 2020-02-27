import sqlite3 as sql

get_dense = lambda p, d: None if d == 0 else p/d

headers = [
	#"Cleanup_ID", 	
	#"Zone",	
	#"State",	
	#"Country",	
	#"GPS",	
	#"Lat",	
	#"Long",	
	#"Cleanup_Type",	
	#"Cleanup_Date",	
	#"Month",	
	#"Date",	
	#"Year",	
	#"Group_Name",	
	"Adults",	
	"Children",	
	"People",	
	#"Pounds",	
	"Miles",	
	"_of_bags",	
	"Cigarette_Butts",	
	"Food_Wrappers_candy_chips_etc",	
	"Take_OutAway_Containers_Plastic",	
	"Take_OutAway_Containers_Foam",	
	"Bottle_Caps_Plastic",	
	"Bottle_Caps_Metal",	
	"Lids_Plastic",	
	"Straws_Stirrers",	
	"Forks_Knives_Spoons",	
	"Beverage_Bottles_Plastic",	
	"Beverage_Bottles_Glass",	
	"Beverage_Cans",	
	"Grocery_Bags_Plastic",	
	"Other_Plastic_Bags",	
	"Paper_Bags",	
	"Cups_Plates_Paper",	
	"Cups_Plates_Plastic",	
	"Cups_Plates_Foam",	
	"Fishing_Buoys_Pots_Traps",	
	"Fishing_Net_Pieces",	
	"Fishing_Line_1_yardmeter_1_piece",	
	"Rope_1_yardmeter_1_piece",	
	"Fishing_Gear_Clean_Swell",	
	"Six_Pack_Holders",	
	"Other_PlasticFoam_Packaging",	
	"Other_Plastic_Bottles_oil_bleach_etc",	
	"Strapping_Bands",	
	"Tobacco_PackagingWrap",	
	"Other_Packaging_Clean_Swell",	
	"Appliances_refrigerators_washers_etc",	
	"Balloons",	
	"Cigar_Tips",	
	"Cigarette_Lighters",	
	"Construction_Materials",	
	"Fireworks",	
	"Tires",	
	"Toys",	
	"Other_Trash_Clean_Swell",	
	"Condoms",	
	"Diapers",	
	"Syringes",	
	"TamponsTampon_Applicators",	
	"Personal_Hygiene_Clean_Swell",	
	"Foam_Pieces",	
	"Glass_Pieces",	
	"Plastic_Pieces"#,	
	#"Total_Items_Collected"
]

head_nums = {e:i for i,e in enumerate(headers) if e != ""}


def init():
	conn = sql.connect("cleanup.db")
	curs = conn.cursor()
	return conn, curs

def close():
	conn.commit()
	conn.close()

def get_headers():
	return headers

def analyze_row(row, filters):
	cnt = 0
	mil = 0
	lbs = 0
	peo = 0
	adu = 0

	for i,f in enumerate(filters):
		if f == "Pounds": lbs = row[i]
		elif f == "Miles": mil = row[i]
		elif f == "People": peo = row[i]
		elif f == "Adults": adu = row[i]
		elif f == "Children" or f=="_of_bags": continue
		else: cnt += row[i]
	
	res = {f:row[i] for i,f in enumerate(filters)}
	res["num_items"] = cnt
	res["lbs"] = lbs

	res["lbs_mile"] = get_dense(lbs, mil)
	res["lbs_person"] = get_dense(lbs, peo)
	res["lbs_adult"] = get_dense(lbs, adu)

	res["cnt_mile"] = get_dense(cnt, mil)
	res["cnt_person"] = get_dense(cnt, peo)
	res["cnt_adult"] = get_dense(cnt, adu)
	
	return res

sel_fil = lambda filters, custom: "select " + ', '.join(["sum(%s)" % s for s in filters]) + ("", ", ")[len(custom)>0] + ', '.join(custom) + " from cleanup"

def analyze_dataset(filters=headers):
	conn, curs = init()
	
	filters = [f for f in filters if f in head_nums]
	filters.append("Pounds")
	cmd =  sel_fil(filters, []) + " where Year >= 2010 and Year < 2020;"
	
	row = [r for r in curs.execute(cmd)][0]
	
	res = analyze_row(row, filters)

	conn.close()
	return res
 
def analyze_dataset_by_months(filters=headers):
	conn, curs = init()

	filters = [f for f in filters if f in head_nums]
	filters.append("Pounds")
	cmd = sel_fil(filters, ["Month", "Year"]) + " where Year >= 2010 and Year < 2020 group by Month, Year order by Year ASC, Month ASC"

	rows = curs.execute(cmd)
	ind = len(filters)
	res = {(r[ind], r[ind+1]): analyze_row(r, filters) for r in rows}

	conn.close()
	return res

def analyze_month_data(month, year, filters=headers):
	conn, curs = init()
	
	filters = [f for f in filters if f in head_nums]
	filters.append("Pounds")
	cmd = sel_fil(filters, ["Zone", "avg(Lat)", "avg(Long)"]) + " where Month=? and Year=? group by Zone order by Pounds"
	
	rows = curs.execute(cmd, (month, year))
	ind = len(filters)
	res = {r[ind]: {**analyze_row(r, filters), **{"Lat": r[ind+1], "Long": r[ind+2]}} for r in rows}

	cmd = sel_fil(filters, []) + " where Month=? and Year=?;"
	row = [r for r in curs.execute(cmd, (month, year))][0]
	res = {**res, **analyze_row(row, filters)}
	
	conn.close()
	return res

def analyze_zone_data(zone, filters=headers):
	conn, curs = init()
	
	filters = [f for f in filters if f in head_nums]
	filters.append("Pounds")
	cmd = sel_fil(filters, ["Month", "Year", "avg(Lat)", "avg(Long)"]) + " where Year >= 2010 and Year < 2020 and Zone=? group by Month, Year order by Pounds"
	
	rows = curs.execute(cmd, (zone,))
	ind = len(filters)
	res = {(r[ind], r[ind+1]): {**analyze_row(r, filters), **{"Lat": r[ind+2], "Long": r[ind+3]}} for r in rows}

	cmd = sel_fil(filters, ["avg(Lat)", "avg(Long)"]) + " where Year >= 2010 and Year < 2020 and Zone=?"	
	row = [r for r in curs.execute(cmd, (zone,))][0]
	res = {**res, **analyze_row(row, filters)}
	res["lat"] = row[ind]
	res["long"] = row[ind+1]

	conn.close()
	return res

def analyze_zone_data_by_month(zone, month, year, filters=headers):
	conn, curs = init()
	
	filters = [f for f in filters if f in head_nums]
	filters.append("Pounds")
	cmd = sel_fil(filters, ["Lat", "Long"]) + " where Year=? and Month=? and Zone=? group by Lat, Long order by Pounds"
	
	rows = curs.execute(cmd, (year, month, zone))
	ind = len(filters)
	res = {(r[ind], r[ind+1]): analyze_row(r, filters) for r in rows}

	cmd = sel_fil(filters, ["Lat", "Long"]) + " where Year=? and Month=? and Zone=?"	
	row = [r for r in curs.execute(cmd, (year, month, zone))][0]
	res = {**res, **analyze_row(row, filters)}
	res["lat"] = row[ind]
	res["long"] = row[ind+1]

	conn.close()
	return res

#OUTDATED METHODS
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

def get_month_data(month=None, year=None):
	conn, curs = init()
	if month != None and year != None:
		rows = curs.execute('select zone, sum(Total_Items_Collected), sum(Miles), sum(Pounds), avg(Lat), avg(Long), sum(People), sum(Adults) from cleanup where Month=? and Year=? group by Zone order by Total_Items_Collected DESC', (month, year))
	else:
		rows = curs.execute('select zone, sum(Total_Items_Collected), sum(Miles), sum(Pounds), avg(Lat), avg(Long), sum(People), sum(Adults) from cleanup group by Zone order by Total_Items_Collected DESC')
	res = {r[0]: {"num_items": r[1], "pounds/mile": get_dense(r[3], r[2]), "lat":r[4], "lng": r[5], "pounds/people": get_dense(r[3], r[6]), "pounds/adults": get_dense(r[3], r[7])} for r in rows} 
	conn.close()
	return res

def get_zone_data(zone, month=None, year=None):
	conn, curs = init()
	if month != None and year != None:
		rows = curs.execute('select Cleanup_ID, sum(Total_Items_Collected), sum(Miles), sum(Pounds), Lat, Long, sum(People), sum(Adults) from cleanup where zone=? and Month=? and Year=? group by lat, long order by Total_Items_Collected DESC', (zone, month, year))
	else:
		rows = curs.execute('select Cleanup_ID, sum(Total_Items_Collected), sum(Miles), sum(Pounds), Lat, Long, sum(People), sum(Adults) from cleanup where zone=? group by lat, long order by Total_Items_Collected DESC', (zone,))
		
	res = {r[0]: {"num_items": r[1], "desnity": get_dense(r[3], r[2]), "lat": r[4], "lng": r[5], "pounds/people": get_dense(r[3], r[6]), "pounds/adults": get_dense(r[3], r[7])} for r in rows}
	conn.close()
	return res

if __name__ == '__main__':
	print(analyze_dataset(), end="\n\n")
	print(analyze_dataset_by_months(), end="\n\n")
	print(analyze_month_data(5,2019), end="\n\n")
	print(analyze_zone_data("Kings County, Brooklyn, NY, USA"), end="\n\n")
	print(analyze_zone_data_by_month("Kings County, Brooklyn, NY, USA", 5, 2019), end="\n\n")
	#print(analyze_dataset(), end="\n\n")
	#print(analyze_dataset(), end="\n\n")
	#print(get_data(), end="\n\n")
	#print(get_months_data(), end="\n\n")
	#print(get_month_data(5, 2019), end="\n\n")
	#print(get_zone_data('Kings County, Brooklyn, NY, USA', 5, 2019), end="\n\n")
	#print(get_zone_data('Kings County, Brooklyn, NY, USA'), end="\n\n")
