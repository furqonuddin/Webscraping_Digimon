from bs4 import BeautifulSoup
import requests
import csv
import unicodedata

# from website
url = 'https://wikimon.net/Visual_List_of_Digimon'
x = requests.get(url)
y = BeautifulSoup(x.content, 'html.parser')

data = y.find_all('td')


lcsv = [['id','Nama','Gambar']]
lsql = []
n = 0
for i in data:
    data2 = i.find_all('img', src=True, alt=True)
    for q in data2:
        gbr = 'https://wikimon.net' + q['src']
        nama = q['alt']
        nama_normal = unicodedata.normalize('NFD', nama)
        hasil = ''.join(c for c in nama_normal if not unicodedata.combining(c))
        digimon = unicodedata.normalize('NFC', hasil).strip('\u200e')

        n += 1
        nama = list((str(n),digimon,gbr))
        
        lcsv.append(nama)
        
        # untuk sql
        sqldata = (n,digimon,gbr)
        lsql.append(sqldata)


# ke CSV
with open('Digimon.csv', 'w', newline='') as csvFile:
    writer = csv.writer(csvFile, delimiter=';')
    writer.writerows(lcsv)

csvFile.close()

# ke mysql
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="furqon",
  passwd="0987654321",
  database="digimon"
)

mycursor = mydb.cursor()

hapus = "DELETE FROM list_digimon"
mycursor.execute(hapus)
mydb.commit()

sql = "INSERT INTO list_digimon (id, nama, gambar) VALUES (%s, %s, %s)"
mycursor.executemany(sql, lsql)
mydb.commit()

print(mycursor.rowcount, "data telah dimasukkan.")