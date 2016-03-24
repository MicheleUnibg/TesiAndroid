import urllib
import sqlite3
import os



conn=sqlite3.connect("/home/michele/Scrivania/Tesi/Crawler/database.db")
c=conn.cursor()

#url="http://f.giveawaycrew.com/f.php?p=4&i=com.camelgames.fantasyland&v=1.24.0&h=N0Y4UWdjYlN1K1BVd0VYanRqdTl2Zz09&d=K010RjU3RlVxcEdTT1c5T0hFdHpyQT09"
c.execute("select titolo,linkDownload from prova2 where scaricato='false' LIMIT 1")
ris=c.fetchone()
testfile = urllib.URLopener()
testfile.retrieve(ris[1], "App/"+ris[0])

