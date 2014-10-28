from bs4 import BeautifulSoup
import urllib2
import pg_config
import psycopg2

page = urllib2.urlopen('http://kenpom.com')
soup = BeautifulSoup(page)


try:
    conn = psycopg2.connect(pg_config.conn_string)
except:
    print "can't connect to db"


# get each row of the big table
trs = soup.find_all('tr')

for tr in trs:
    tds = tr.find_all('td')
    if tds: 
        rank = int(tds[0].string)
        school = tds[1].a.string
        conference = tds[2].string
        wins = int(tds[3].string.split('-')[0])
        losses = int(tds[3].string.split('-')[1])

        pyth = float(tds[4].string)

        adj_o = float(tds[5].string)
        adj_o_rank = int(tds[6].string)

        adj_d = float(tds[7].string)
        adj_d_rank = int(tds[8].string)

        adj_t = float(tds[9].string)
        adj_t_rank = int(tds[10].string)

        luck = float(tds[11].string)
        luck_rank = int(tds[12].string)

        sos_pyth = float(tds[13].string)
        sos_pyth_rank = int(tds[14].string)

        sos_opp_o = float(tds[15].string)
        sos_opp_o_rank = int(tds[16].string)

        sos_opp_d = float(tds[17].string)
        sos_opp_d_rank = int(tds[18].string)

        ncsos_pyth = float(tds[19].string)
        ncsos_pyth_rank = int(tds[20].string)

        #print rank, school, wins, losses
