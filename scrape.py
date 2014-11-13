from bs4 import BeautifulSoup
import urllib2
import pg_config
import psycopg2


try:
    conn = psycopg2.connect(pg_config.conn_string)
except:
    print "can't connect to db"

# map team to id
c = conn.cursor()
c.execute("""SELECT * from team""")
rows = c.fetchall() 
team_to_id = {}
for row in rows:
    team_to_id[row[0]] = row[2]

# init team_data_dict
team_datas = {}

def main_page():
    page = urllib2.urlopen('http://kenpom.com')
    soup = BeautifulSoup(page)

    # get all rows
    trs = soup.find_all('tr')

    for tr in trs:
        tds = tr.find_all('td')
        if tds:
            team_dict = {}
            team_dict['rank']  = int(tds[0].string)
            school = tds[1].a.string
            team_dict['id'] = team_to_id[school]
            team_dict['school'] = school
            team_dict['wins'] = int(tds[3].string.split('-')[0])
            team_dict['losses'] = int(tds[3].string.split('-')[1])

            team_dict['pyth'] = float(tds[4].string)

            team_dict['adj_o'] = float(tds[5].string)
            team_dict['adj_o_rank'] = int(tds[6].string)

            team_dict['adj_d'] = float(tds[7].string)
            team_dict['adj_d_rank'] = int(tds[8].string)

            team_dict['adj_t'] = float(tds[9].string)
            team_dict['adj_t_rank'] = int(tds[10].string)

            team_dict['luck'] = float(tds[11].string)
            team_dict['luck_rank'] = int(tds[12].string)

            team_dict['sos_pyth'] = float(tds[13].string)
            team_dict['sos_pyth_rank'] = int(tds[14].string)

            team_dict['sos_opp_o'] = float(tds[15].string)
            team_dict['sos_opp_o_rank'] = int(tds[16].string)

            team_dict['sos_opp_d'] = float(tds[17].string)
            team_dict['sos_opp_d_rank'] = int(tds[18].string)

            team_dict['ncsos_pyth'] = float(tds[19].string)
            team_dict['ncsos_pyth_rank'] = int(tds[20].string)

            team_datas[school] = team_dict


def four_factors():
    page = urllib2.urlopen('http://kenpom.com/stats.php')
    soup = BeautifulSoup(page)

def team_stats():
    page = urllib2.urlopen('http://kenpom.com/teamstats.php')
    soup = BeautifulSoup(page)

main_page()

team_datas_list = team_datas.values()

print "Inserting", len(team_datas_list), "team data points"
c.executemany("""INSERT INTO team_data (team_id, wins, losses, pyth, adj_o, adj_o_rank, adj_d, adj_d_rank,
                adj_t, adj_t_rank, luck, luck_rank, sos_pyth, sos_pyth_rank, sos_opp_o, sos_opp_d, sos_opp_o_rank,
                sos_opp_d_rank, ncsos_pyth, ncsos_pyth_rank, thru_date)
                VALUES (%(id)s, %(wins)s, %(losses)s, %(pyth)s, %(adj_o)s, %(adj_o_rank)s, %(adj_d)s, %(adj_d_rank)s,
                    %(adj_t)s, %(adj_t_rank)s, %(luck)s, %(luck_rank)s, %(sos_pyth)s, %(sos_pyth_rank)s, %(sos_opp_o)s, %(sos_opp_o)s, %(sos_opp_o_rank)s,
                    %(sos_opp_d_rank)s, %(ncsos_pyth)s, %(ncsos_pyth_rank)s, (CURRENT_DATE - INTERVAL '1 day'))""", team_datas_list)

conn.commit()
