import pandas as pd, json, datetime, csv, os

month = datetime.date.today().strftime("%B")
day = datetime.date.today().strftime("%d")
date = month + day
os.chdir('/home/Jon2Anderson/mlb/dailysheets/')

def getLineupBreakdownvr(team, lineup):
    frame = pd.DataFrame()
    for player in lineup:
        if player in allhitters:
            frame = frame.append(statsdfvr[statsdfvr['Name']==player])
        else:
            dummydict = {'Name':player, 'vs.': pitcher, 'AB':0, 'PA':0, 'H':0, '1B':0, '2B':0, '3B':0, 'HR':0, 'BB':0, 'IBB':0, 'SO':0, 'HBP':0, 'SF': 0, 'wRC+': 0}
            frame = frame.append(dummydict, ignore_index=True)

    ab = float(frame['AB'].sum())
    pa = float(frame['PA'].sum())
    hits = float(frame['H'].sum())
    singles = float(frame['1B'].sum())
    doubles = float(frame['2B'].sum())
    triples = float(frame['3B'].sum())
    hr = float(frame['HR'].sum())
    bb = float(frame['BB'].sum())
    ibb = float(frame['IBB'].sum())
    ubb = bb-ibb
    so = float(frame['SO'].sum())
    hbp = float(frame['HBP'].sum())
    sf = float(frame['SF'].sum())
    wrc = float(frame['wRC+'].mean())
    wrcstr = str(round(wrc, 2))
    ubbw = .693
    hbpw = .723
    singlew = .877
    doublew = 1.232
    triplew = 1.552
    hrw = 1.979
    krate = so/pa
    kratestr = ("{:.1%}".format(krate))
    bbrate = bb/pa
    bbratestr = ("{:.1%}".format(bbrate))
    hrrate = hr/pa
    hrratestr = ("{:.1%}".format(hrrate))
    avg = hits/ab
    avgstr = str(round(avg, 3))
    slg = ((singles + (doubles*2) + (triples*3) + (hr*4))/ab)
    slgstr = str(round(slg, 3))
    iso = slg - avg
    isostr = str(round(iso, 3))
    woba = ((ubb*ubbw)+(hbp*hbpw)+(singles*singlew)+(doubles*doublew)+(triples*triplew)+(hr*hrw))/(ab+bb-ibb+sf+hbp)
    wobastr = str(round(woba, 3))

    teamDict = {'Team': team, 'vs.': pitcher, 'AVG': avgstr, 'SLG': slgstr, 'ISO': isostr, 'wOBA': wobastr, 'wRC+': wrcstr, 'K%': kratestr, 'BB%': bbratestr, 'HR%': hrratestr}
    teamdf = pd.DataFrame()
    teamdf = teamdf.append(teamDict, ignore_index=True)
    return(teamdf)

def getLineupBreakdownvl(team, lineup):
    frame = pd.DataFrame()
    for player in lineup:
        if player in allhitters:
            frame = frame.append(statsdfvl[statsdfvl['Name']==player])
        else:
            dummydict = {'Name':player, 'vs.': pitcher, 'AB':0, 'PA':0, 'H':0, '1B':0, '2B':0, '3B':0, 'HR':0, 'BB':0, 'IBB':0, 'SO':0, 'HBP':0, 'SF': 0, 'wRC+': 0}
            frame = frame.append(dummydict, ignore_index=True)

    ab = float(frame['AB'].sum())
    pa = float(frame['PA'].sum())
    hits = float(frame['H'].sum())
    singles = float(frame['1B'].sum())
    doubles = float(frame['2B'].sum())
    triples = float(frame['3B'].sum())
    hr = float(frame['HR'].sum())
    bb = float(frame['BB'].sum())
    ibb = float(frame['IBB'].sum())
    ubb = bb-ibb
    so = float(frame['SO'].sum())
    hbp = float(frame['HBP'].sum())
    sf = float(frame['SF'].sum())
    wrc = float(frame['wRC+'].mean())
    wrcstr = str(round(wrc, 2))
    ubbw = .693
    hbpw = .723
    singlew = .877
    doublew = 1.232
    triplew = 1.552
    hrw = 1.979
    krate = so/pa
    kratestr = ("{:.1%}".format(krate))
    bbrate = bb/pa
    bbratestr = ("{:.1%}".format(bbrate))
    hrrate = hr/pa
    hrratestr = ("{:.1%}".format(hrrate))
    avg = hits/ab
    avgstr = str(round(avg, 3))
    slg = ((singles + (doubles*2) + (triples*3) + (hr*4))/ab)
    slgstr = str(round(slg, 3))
    iso = slg - avg
    isostr = str(round(iso, 3))
    woba = ((ubb*ubbw)+(hbp*hbpw)+(singles*singlew)+(doubles*doublew)+(triples*triplew)+(hr*hrw))/(ab+bb-ibb+sf+hbp)
    wobastr = str(round(woba, 3))

    teamDict = {'Team': team, 'vs.': pitcher, 'AVG': avgstr, 'SLG': slgstr, 'ISO': isostr, 'wOBA': wobastr, 'wRC+': wrcstr, 'K%': kratestr, 'BB%': bbratestr, 'HR%': hrratestr}
    teamdf = pd.DataFrame()
    teamdf = teamdf.append(teamDict, ignore_index=True)
    return(teamdf)

with open('/home/Jon2Anderson/mlb/dailystore/%slineups.json' %date, 'r') as f:
    lineups = json.load(f)

with open('/home/Jon2Anderson/mlb/dailystore/%sprobables.json'  % date, 'r') as f:
    probables = json.load(f)

with open('/home/Jon2Anderson/mlb/dailystore/%slineups.json' %date, 'r') as f:
    lineups = json.load(f)

with open('/home/Jon2Anderson/mlb/dailystore/rostersmaster.json', 'r') as f:
    masterhand = json.load(f)

with open('/home/Jon2Anderson/mlb/dailystore/%smatchups.json' %date, 'r') as f:
    matchups = json.load(f)


statsdfvr = pd.read_csv('/home/Jon2Anderson/mlb/datarepo/master/lubreakdown_statsvr19.csv')
statsdfvl = pd.read_csv('/home/Jon2Anderson/mlb/datarepo/master/lubreakdown_statsvl19.csv')
allhitters = statsdfvr['Name'].tolist()
masterdf = pd.DataFrame()
teams = list(lineups.keys())

for team in teams:
    print('working on ' + team)
    lineup = lineups.get(team)
    opponent = matchups.get(team)
    pitcher = probables.get(opponent)
    pitcherhand = masterhand.get(pitcher)

    if lineup == 'no lineup has been posted yet':
        team = team.replace('2', '')
        team = team.replace('1', '')
        print('no lineup for ' + team + ', importing projected lineup.')

        with open('/home/Jon2Anderson/mlb/lineups/%sprojlineup.json' %team, 'r') as f:
            reader = csv.reader(f)
            lineuplist = list(reader)
            lineuplist = lineuplist[0]
            lineup=[]
        for x in lineuplist:
            x = str(x)
            x = x.replace("\"", "")
            x = x.replace("[", "")
            x = x.replace("]", "")
            x = x.lstrip()
            lineup.append(x)

        if pitcherhand == 'l':
            teamdf = getLineupBreakdownvl(team, lineup)
            teamdf['LU Conf?']='n'
            masterdf = masterdf.append(teamdf)
        else:
            teamdf = getLineupBreakdownvr(team, lineup)
            teamdf['LU Conf?']='n'
            masterdf = masterdf.append(teamdf)

    else:
        print(team + ' lineup has been posted.')
        if pitcherhand == 'l':
            teamdf = getLineupBreakdownvl(team, lineup)
            teamdf['LU Conf?']='y'
            masterdf = masterdf.append(teamdf)
        else:
            teamdf = getLineupBreakdownvr(team, lineup)
            teamdf['LU Conf?']='y'
            masterdf = masterdf.append(teamdf)

dkdata = pd.read_csv('/home/Jon2Anderson/mlb/dailysheets/%s_DKData.csv' %date)
dkdata=dkdata[['Name', 'sal']]
dkdata=dkdata.rename(index=str, columns={'Name': 'vs.'})
masterdf = pd.merge(masterdf, dkdata, on='vs.')

cols=['Team', 'LU Conf?', 'vs.', 'sal', 'AVG', 'SLG', 'ISO', 'wOBA', 'wRC+', 'K%', 'BB%', 'HR%']
masterdf = masterdf[cols]
print(masterdf)
masterdf.to_csv('%s_LineupBreakdown_Splits19.csv' %date)