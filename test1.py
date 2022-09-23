import sqlite3
# import datetime

conn = sqlite3.connect('iots.sqlite3')
c = conn.cursor()
# print("***" * 30)
#
# cursor = c.execute("SELECT id, temperature, humidity, lux, tvoc, co2, pm25, time  from iots")
# for row in cursor:
#     print("ID = ", row[0])
#     print("temperature = ", row[1])
#     print("humidity = ", row[2])
#     print("lux = ", row[3])
#     print("tvoc = ", row[4])
#     print("co2 = ", row[5])
#     print("pm25 = ", row[6])
#     print("time = ", row[7], "\n")
#
# print("***" * 30)

cousor1 = c.execute("SELECT humidity from iots where temperature >28")
print(cousor1.fetchone())

# timenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# print(type(timenow))
# print(timenow)

# cousor2 = c.execute("INSERT INTO iots (iot, temperature, humidity, lux, tvoc, co2, pm25, time) VALUES (001,25,50,60,100,100,100,datetime('now','localtime'))")

c.execute(
        "SELECT iot,temperature,humidity,lux,tvoc,co2,pm25,time FROM iots ORDER by time DESC")
print(c.fetchone())
conn.commit()
conn.close()
