import os, datetime, json, pandas as pd

month = datetime.date.today().strftime("%B")
day = datetime.date.today().strftime("%d")
date = month + day
############## Import data #################
os.chdir('/home/Jon2Anderson/mlb/datarepo/master')

hitmaster = pd.read_csv('hitmaster19.csv')
hitvrmaster = pd.read_csv('hitvrmaster19.csv')
hitvlmaster = pd.read_csv('hitvlmaster19.csv')

pitchmaster = pd.read_csv('pitchmaster19.csv')
pitchvrmaster = pd.read_csv('pitchvrmaster19.csv')
pitchvlmaster = pd.read_csv('pitchvlmaster19.csv')

pitcherlist = pitchmaster['Name'].tolist()
############################################

with open('/home/Jon2Anderson/mlb/dailystore/%sprobables.json'  % date, 'r') as f:
    probables = json.load(f)

with open('/home/Jon2Anderson/mlb/dailystore/%slineups.json' %date, 'r') as f:
    lineups = json.load(f)

with open('/home/Jon2Anderson/mlb/dailystore/rostersmaster.json', 'r') as f:
    masterhand = json.load(f)

with open('/home/Jon2Anderson/mlb/dailystore/%smatchups.json' %date, 'r') as f:
    matchups = json.load(f)

dkdata = pd.read_csv('/home/Jon2Anderson/mlb/dailysheets/%s_DKData.csv' %date)
pteam = dict(zip(dkdata.Name, dkdata.team))

teams = list(lineups.keys())
nolineup = []
masterframe = pd.DataFrame()

for team in teams:
    pitcher = probables.get(team)
    pitcherhand = masterhand.get(pitcher)
    opponent = matchups.get(team)
    pframe = pd.DataFrame()

    if pitcher in pitcherlist:
        pframe = pframe.append(pitchmaster[pitchmaster['Name']==pitcher])
        pframe['Opp']=opponent
        pframe['R/L']=pitcherhand
        pframe['Team']=pteam.get(pitcher)

    else:
        print('no pitcher data available for ' + pitcher)
        dummydict = {'Name': pitcher, 'R/L': pitcherhand, 'Team': pteam, 'Opp': opponent, 'IP': '', 'K%': '',
                        'BB%': '', 'BABIP': '', 'ERA': '', 'xFIP': '', 'WHIP': '', 'xwoba': '', 'AVG': '',
                        'xba': '', 'FB%': '', 'GB%': '', 'LD%': '', 'HR/9': '', 'Soft%': '', 'Hard%': '',
                        'HR/FB': '', 'K-BB%': '', 'LOB%': '', 'angle': '', 'velo': ''}
        pframe = pframe.append(dummydict, ignore_index=True)

    cols=['Name', 'R/L', 'Team', 'Opp', 'IP', 'K%', 'BB%', 'BABIP',
            'ERA', 'xFIP', 'WHIP', 'xwoba', 'AVG', 'xba', 'FB%', 'GB%', 'LD%', 'HR/9', 'Soft%',
            'Hard%', 'HR/FB', 'K-BB%', 'LOB%', 'angle', 'velo']

    masterframe = masterframe.append(pframe)
    masterframe = masterframe[cols]
masterframe.to_csv('/home/Jon2Anderson/mlb/dailysheets/%s_PitchersReport.csv' %date)
print('done')