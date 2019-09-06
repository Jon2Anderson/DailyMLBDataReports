import requests, os, datetime, json
from bs4 import BeautifulSoup
from collections import Counter
import pandas as pd

month = datetime.date.today().strftime("%B")
day = datetime.date.today().strftime("%d")
date = month + day

# For daily fantasy players, we need to get the player salary and other
# information. This function uses rotogrinders.com to get each day's player 
# salaries and matchups.
def dfsData():
    os.chdir('/home/Jon2Anderson/mlb/dailysheets')
    month = datetime.date.today().strftime("%B")
    day = datetime.date.today().strftime("%d")
    date = month + day

    ###################
    #####DRAFTKINGS####
    ###################
    dkdata = requests.get('https://rotogrinders.com/projected-stats/mlb-hitter.csv?site=draftkings')
    dkdata.raise_for_status()
    dkfile = open('/home/Jon2Anderson/mlb/dailysheets/%s_DKDatahit.csv' %date, 'wb')

    for chunk in dkdata.iter_content(100000):
        dkfile.write(chunk.lower())

    dkfile.close()

    dkdatahit = pd.read_csv('/home/Jon2Anderson/mlb/dailysheets/%s_DKDatahit.csv' %date, names=['Name', 'sal', 'team', 'pos', 'opp', 'nan', 'nan', 'proj'])
    dkdatahit = dkdatahit[['Name', 'pos', 'sal', 'team', 'opp']]
    ###################
    ###################
    dkdata = requests.get('https://rotogrinders.com/projected-stats/mlb-pitcher.csv?site=draftkings')
    dkdata.raise_for_status()
    dkfile = open('/home/Jon2Anderson/mlb/dailysheets/%s_DKDatapitch.csv' %date, 'wb')

    for chunk in dkdata.iter_content(100000):
        dkfile.write(chunk.lower())

    dkfile.close()

    dkdatapitch = pd.read_csv('/home/Jon2Anderson/mlb/dailysheets/%s_DKDatapitch.csv' %date, names=['Name', 'sal', 'team', 'pos', 'opp', 'nan', 'nan', 'proj'])
    dkdatapitch = dkdatapitch[['Name', 'pos', 'sal', 'team', 'opp']]
    dkdatapitch['Name']=dkdatapitch['Name'].str.replace('matt boyd', 'matthew boyd')
    dkdatapitch['Name']=dkdatapitch['Name'].str.replace('vincent velasquez', 'vince velasquez')
    dkdatapitch['Name']=dkdatapitch['Name'].str.replace('christopher paddack', 'chris paddack')
    dkdatapitch['Name']=dkdatapitch['Name'].str.replace('matthew strahm', 'matt strahm')

    ###################

    DKData = dkdatahit.append(dkdatapitch)
    DKData.to_csv('/home/Jon2Anderson/mlb/dailysheets/%s_DKData.csv' %date)

    ###################
    ######FANDUEL######
    ###################
    fddata = requests.get('https://rotogrinders.com/projected-stats/mlb-hitter.csv?site=fanduel')
    fddata.raise_for_status()
    fdfile = open('/home/Jon2Anderson/mlb/dailysheets/%s_FDDatahit.csv' %date, 'wb')

    for chunk in fddata.iter_content(100000):
        fdfile.write(chunk.lower())

    fdfile.close()

    fddatahit = pd.read_csv('/home/Jon2Anderson/mlb/dailysheets/%s_FDDatahit.csv' %date, names=['Name', 'sal', 'team', 'pos', 'opp', 'nan', 'nan', 'proj'])
    fddatahit = fddatahit[['Name', 'pos', 'sal', 'team', 'opp']]
    fddatahit.to_csv('%s_FDDatahit.csv' %date)
    ###################

    ###################
    fddata = requests.get('https://rotogrinders.com/projected-stats/mlb-pitcher.csv?site=fanduel')
    fddata.raise_for_status()
    fdfile = open('/home/Jon2Anderson/mlb/dailysheets/%s_FDDatapitch.csv' %date, 'wb')

    for chunk in fddata.iter_content(100000):
        fdfile.write(chunk.lower())

    fdfile.close()

    fddatapitch = pd.read_csv('/home/Jon2Anderson/mlb/dailysheets/%s_FDDatapitch.csv' %date, names=['Name', 'sal', 'team', 'pos', 'opp', 'nan', 'nan', 'proj'])
    fddatapitch = fddatapitch[['Name', 'pos', 'sal', 'team', 'opp']]
    fddatapitch.to_csv('%s_FDDatapitch.csv' %date)
    ###################

    FDData = fddatahit.append(fddatapitch)
    FDData.to_csv('/home/Jon2Anderson/mlb/dailysheets/%s_FDData.csv' %date)

    os.remove('/home/Jon2Anderson/mlb/dailysheets/%s_DKDatahit.csv' %date)
    os.remove('/home/Jon2Anderson/mlb/dailysheets/%s_DKDatapitch.csv' %date)
    os.remove('/home/Jon2Anderson/mlb/dailysheets/%s_FDDatapitch.csv' %date)
    os.remove('/home/Jon2Anderson/mlb/dailysheets/%s_FDDatahit.csv' %date)

# This function uses the DKData file created in the dfsData function, and then 
# just pulls each team and that team's opponent for the day into a dictionary and
# saves it off as a json file.
def getMatchups():
    df = pd.read_csv('/home/Jon2Anderson/mlb/dailysheets/%s_DKData.csv' %date)
    dict1 = dict(zip(df.team, df.opp))
    dict2 = dict(zip(df.opp, df.team))
    matchups = dict(dict1, **dict2)
    with open('/home/Jon2Anderson/mlb/dailystore/%smatchups.json'  % date, 'w') as file:
        file.write(json.dumps(matchups))
    print('Matchups retrieved successfully.')

# This function uses the DKData file to get the probable starting pitchers for that
# day
def getProbables():
    df = pd.read_csv('/home/Jon2Anderson/mlb/dailysheets/%s_DKData.csv' %date)
    df = df[df['pos']=='sp']
    probables = dict(zip(df.team, df.Name))

    with open('/home/Jon2Anderson/mlb/dailystore/%sprobables.json'  % date, 'w') as file:
        file.write(json.dumps(probables))
    print('Probable pitchers retrieved successfully.')

# This function scrapes baseballpress.com to get each team's lineup for that day. 
# Lineups are usuall posted 3-5 hours before the start of each game.
def getLineups():
    os.chdir('/home/Jon2Anderson/mlb/lineups')

    ## Get the HTML from the lineups web page online and ##
    ##  narrow it down to section of code that we want ##
    url = 'http://www.baseballpress.com/lineups'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    data = soup.find('div', {'class': 'lineup-card-body'})

    ## Finds all code segments with lineups in them ##
    lucode = soup.findAll('div', {'class': 'team-lineup clearfix'})

    ## Make blank list that we will store team names in later, and then ##
    ## parse through code to find all team names.##
    teams=[]
    for div in data.findAll('div', {'class': 'team-name'}):
        team = div.text.lower()
        team = team.replace(' ', '')
        team = team.replace('diamondbacks', 'dbacks')
        teams.append(team)

    ## In case any teams are playing 2 games today, we will need to ##
    ## rename their 2nd lineup to avoid duplicates and confusion, this ##
    ## code will add a '2' to the name of any team's second lineup ##
    counts = Counter(teams)
    for s, num in counts.items():
        if num > 1:
            for suffix in range(1, num+1):
                teams[teams.index(s)] = s + str(suffix)

    ## Make blank dictionary where we will store the lineups ##
    lineupdict = dict()

    ## Loop through all lineups, adding team names as keys in the ##
    ## dictionary, and the listed lineup as the values ##
    i=0
    for lu in lucode:
        lineup = []
        team = teams[i]
        if team == 'diamondbacks':
            team == 'dbacks'

        if lu.text == '':
            lineup = 'no lineup has been posted yet'
            newdict = {team: lineup}
            lineupdict.update(newdict)
        else:
            for div in lu.findAll('a', {'class': 'player-link'}):
                lineup.append(div.text.lower())
            newdict = {team: lineup}
            lineupdict.update(newdict)
        i=i+1

    ## Print the dictionary to a file and we are done ##
    with open('/home/Jon2Anderson/mlb/dailystore/%slineups.json' %date, 'w') as f:
        f.write(json.dumps(lineupdict))

    print('Lineups retrieved successfully.')

# This function gets projected and confirmed lineups from rotogrindres. This site is
# nice because they show a projected lineup until the real lineup is posted, this
# makes it so we can do analysis on a team before their lineup is posted
def getLineupsRG():
    os.chdir('/home/Jon2Anderson/mlb/lineups')
    path='/home/Jon2Anderson/mlb/lineups'
    files = [f for f in os.listdir(path)]
    for f in files:
        os.remove(os.path.join(path, f))
    url = 'https://rotogrinders.com/lineups/mlb?site=fanduel'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    hitters = []
    for span in soup.findAll('span', {'class': 'pname'}):
        for player in span.findAll('a'):
            hitter = player.text.lower()
            hitter = hitter.replace('albert almora', 'albert almora jr.')
            hitter = hitter.replace('manuel pina', 'manny pina')
            hitter = hitter.replace('jackie bradley', 'jackie bradley jr.')
            hitter = hitter.replace('christopher taylor', 'chris taylor')
            hitter = hitter.replace('nick castellanos', 'nicholas castellanos')
            hitter = hitter.replace('thomas pham', 'tommy pham')
            hitter = hitter.replace('michael taylor', 'michael a. taylor')
            hitter = hitter.replace('nick delmonico', 'nicky delmonico')
            hitter = hitter.replace('timothy anderson', 'tim anderson')
            hitter = hitter.replace('ronald acuna', 'ronald acuna jr.')
            hitter = hitter.replace('yulieski gurriel', 'yuli gurriel')
            hitter = hitter.replace('gregory bird', 'greg bird')
            hitter = hitter.replace('jakob bauers', 'jake bauers')
            hitter = hitter.replace('j.t. riddle', 'jt riddle')
            hitter = hitter.replace('lourdes gurriel', 'lourdes gurriel jr.')
            hitters.append(hitter)

    teams=[]
    for span in soup.findAll('span', {'class': 'mascot'}):
        team = span.text.lower()
        team = team.replace('rays', 'tbr')
        team = team.replace('mets', 'nym')
        team = team.replace('cardinals', 'stl')
        team = team.replace('braves', 'atl')
        team = team.replace('rangers', 'tex')
        team = team.replace('tigers', 'det')
        team = team.replace('athletics', 'oak')
        team = team.replace('red sox', 'bos')
        team = team.replace('royals', 'kcr')
        team = team.replace('dodgers', 'lad')
        team = team.replace('padres', 'sdp')
        team = team.replace('indians', 'cle')
        team = team.replace('giants', 'sfg')
        team = team.replace('twins', 'min')
        team = team.replace('pirates', 'pit')
        team = team.replace('mariners', 'sea')
        team = team.replace('blue jays', 'tor')
        team = team.replace('reds', 'cin')
        team = team.replace('brewers', 'mil')
        team = team.replace('phillies', 'phi')
        team = team.replace('angels', 'laa')
        team = team.replace('astros', 'hou')
        team = team.replace('marlins', 'mia')
        team = team.replace('white sox', 'chw')
        team = team.replace('cubs', 'chc')
        team = team.replace('diamondbacks', 'ari')
        team = team.replace('nationals', 'was')
        team = team.replace('yankees', 'nyy')
        team = team.replace('rockies', 'col')
        team = team.replace('orioles', 'bal')
        teams.append(team)

    i=0
    for x in range(len(teams)):
        lineup = hitters[0:9]
        with open('%s.json' %teams[i], 'w') as f:
            f.write(json.dumps(lineup))
        del hitters[0:9]
        i=i+1

    path='/home/Jon2Anderson/mlb/lineups'
    ludict={}
    files = [f for f in os.listdir(path)]
    for f in files:
        teamname = f.split('.')[0]
        with open('%s' %f, 'r') as f:
            lineup = json.load(f)
            ludict.update({teamname: lineup})
    with open('/home/Jon2Anderson/mlb/dailystore/%slineups.json' %date, 'w') as f:
        f.write(json.dumps(ludict))

# This function scrapes each team's website to get their active roster for the day,
# we use this to look up the handedness of each player so we can later look at
# specific splits statistics
def getRosters():
    teams = ['redsox', 'bluejays', 'yankees', 'orioles', 'rays', 'whitesox', 'royals', 'twins', 'indians', 'tigers', 'mariners', 'angels', 'athletics',
        'rangers', 'astros', 'mets', 'braves', 'nationals', 'phillies', 'marlins', 'pirates', 'cubs', 'brewers', 'reds', 'cardinals', 'giants', 'rockies',
        'padres', 'dbacks', 'dodgers']

    for team in teams:
        url = 'http://m.%s.mlb.com/roster' % team

        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')

        pitcherstable = soup.find_all('table', {'class': 'data roster_table'})[0]
        hitterstable = soup.find_all('table', {'class': 'data roster_table'})[1:]

        pitchers=[]
        pitcherhand=[]

        for tr in pitcherstable('tr', {'index': '0'}):
            for td in tr('td', {'index': '2'}):
                pitcher = td.text.lower()
                pitcher = pitcher.replace('\n', '')
                pitchers.append(pitcher)
            for td in tr('td', {'index': '3'}):
                pitchhand = td.text.lower()
                pitchhand = pitchhand.replace('r/', '')
                pitchhand = pitchhand.replace('l/', '')
                pitchhand = pitchhand.replace('s/', '')
                pitcherhand.append(pitchhand)

        teampitdict = dict(zip(pitchers, pitcherhand))
        with open('/home/Jon2Anderson/mlb/rosters/%s_pitchers.json' %team, 'w') as f:
            json.dump(teampitdict, f)

        hitters=[]
        hitterhand=[]

        for table in hitterstable:
            for tr in table('tr', {'index': '0'}):
                for td in tr('td', {'index': '2'}):
                    hitter = td.text.lower()
                    hitter = hitter.replace('\n', '')
                    hitters.append(hitter)
                for td in tr('td', {'index': '3'}):
                    hithand = td.text.lower()
                    hithand = hithand.replace('/r', '')
                    hithand = hithand.replace('/l', '')
                    hitterhand.append(hithand)
        teamhitdict = dict(zip(hitters, hitterhand))
        with open('/home/Jon2Anderson/mlb/rosters/%s_hitters.json' %team, 'w') as f:
            json.dump(teamhitdict, f)

        hitmaster = dict()
        for team in teams:
            with open('/home/Jon2Anderson/mlb/rosters/%s_hitters.json' %team, 'r') as f:
                dump = json.load(f)
                hitmaster.update(dump)

        with open('/home/Jon2Anderson/mlb/dailystore/hitmaster.json', 'w') as f:
             json.dump(hitmaster, f)

        pitchmaster = dict()
        for team in teams:
            with open('/home/Jon2Anderson/mlb/rosters/%s_pitchers.json' %team, 'r') as f:
                dump = json.load(f)
                pitchmaster.update(dump)

        with open('/home/Jon2Anderson/mlb/dailystore/pitchmaster.json', 'w') as f:
            json.dump(pitchmaster, f)

        master = dict()
        files = ['/home/Jon2Anderson/mlb/dailystore/pitchmaster.json', '/home/Jon2Anderson/mlb/dailystore/hitmaster.json']
        for f in files:
            with open(f, 'r') as f:
                dump = json.load(f)
                master.update(dump)

        with open('/home/Jon2Anderson/mlb/dailystore/rostersmaster.json', 'w') as f:
            json.dump(master, f)


# Run all functions to update all of our files that we 
# save off
dfsData()
getProbables()
getLineupsRG()
getRosters()
getMatchups()
#############
print('done')