import os, datetime, json, pandas as pd

month = datetime.date.today().strftime("%B")
day = datetime.date.today().strftime("%d")
date = month + day

os.chdir('/home/Jon2Anderson/mlb/datarepo/master')
pitchmaster = pd.read_csv('pitchmaster19.csv')
pitchvrmaster = pd.read_csv('pitchvrmaster19.csv')
pitchvlmaster = pd.read_csv('pitchvlmaster19.csv')
pitcherlist = pitchmaster['Name'].tolist()

def getPitcherData(team):
    pitcher = probables.get(team)
    pitcherhand = masterhand.get(pitcher)
    opponent = matchups.get(team)
    frame = pd.DataFrame()

    if pitcher in pitcherlist:
        frame = frame.append(pitchmaster[pitchmaster['Name']==pitcher])
        frame['Opp'] = opponent
        frame['R/L'] = pitcherhand
        frame['Split'] = 'vs all'
        frame['Tm'] = team
    else:
        dummydict = {'Name': pitcher, 'R/L': pitcherhand, 'Tm': team, 'Opp': opponent, 'Split': 'vs all', 'IP': '', 'K%': '',
                        'BB%': '', 'BABIP': '', 'ERA': '', 'xFIP': '', 'WHIP': '', 'xwoba': '', 'AVG': '',
                        'xba': '', 'FB%': '', 'GB%': '', 'LD%': '', 'HR/9': '', 'Soft%': '', 'Hard%': '',
                        'HR/FB': '', 'K-BB%': '', 'LOB%': '', 'angle': '', 'velo': ''}
        frame = frame.append(dummydict, ignore_index=True)

    cols=['Name', 'R/L', 'Tm', 'Opp', 'Split', 'IP', 'K%', 'BB%', 'BABIP',
            'ERA', 'xFIP', 'WHIP', 'xwoba', 'AVG', 'xba', 'FB%', 'GB%', 'LD%', 'HR/9', 'Soft%',
            'Hard%', 'HR/FB', 'K-BB%', 'LOB%', 'angle', 'velo']
    frame = frame[cols]
    return frame

def getPitcherDataVR(team):
    pitcher = probables.get(team)
    pitcherhand = masterhand.get(pitcher)
    opponent = matchups.get(team)
    frame = pd.DataFrame()

    if pitcher in pitcherlist:
        frame = frame.append(pitchvrmaster[pitchvrmaster['Name']==pitcher])
        frame['Opp'] = opponent
        frame['R/L'] = pitcherhand
        frame['Split'] = 'vs R'
        frame['Tm'] = team
    else:
        dummydict = {'Name': pitcher, 'R/L': pitcherhand, 'Tm': team, 'Opp': opponent, 'Split': 'vs R', 'IP': '', 'K%': '',
                        'BB%': '', 'BABIP': '', 'ERA': '', 'xFIP': '', 'WHIP': '', 'xwoba': '', 'AVG': '',
                        'xba': '', 'FB%': '', 'GB%': '', 'LD%': '', 'HR/9': '', 'Soft%': '', 'Hard%': '',
                        'HR/FB': '', 'K-BB%': '', 'LOB%': '', 'angle': '', 'velo': ''}
        frame = frame.append(dummydict, ignore_index=True)

    cols=['Name', 'R/L', 'Tm', 'Opp', 'Split', 'IP', 'K%', 'BB%', 'BABIP',
            'ERA', 'xFIP', 'WHIP', 'xwoba', 'AVG', 'xba', 'FB%', 'GB%', 'LD%', 'HR/9', 'Soft%',
            'Hard%', 'HR/FB', 'K-BB%', 'LOB%', 'angle', 'velo']
    frame = frame[cols]
    return frame

def getPitcherDataVL(team):
    pitcher = probables.get(team)
    pitcherhand = masterhand.get(pitcher)
    opponent = matchups.get(team)
    frame = pd.DataFrame()

    if pitcher in pitcherlist:
        frame = frame.append(pitchvlmaster[pitchvlmaster['Name']==pitcher])
        frame['Opp'] = opponent
        frame['R/L'] = pitcherhand
        frame['Split'] = 'vs L'
        frame['Tm'] = team
    else:
        dummydict = {'Name': pitcher, 'R/L': pitcherhand, 'Tm': team, 'Opp': opponent, 'Split': 'vs L', 'IP': '', 'K%': '',
                        'BB%': '', 'BABIP': '', 'ERA': '', 'xFIP': '', 'WHIP': '', 'xwoba': '', 'AVG': '',
                        'xba': '', 'FB%': '', 'GB%': '', 'LD%': '', 'HR/9': '', 'Soft%': '', 'Hard%': '',
                        'HR/FB': '', 'K-BB%': '', 'LOB%': '', 'angle': '', 'velo': ''}
        frame = frame.append(dummydict, ignore_index=True)

    cols=['Name', 'R/L', 'Tm', 'Opp', 'Split', 'IP', 'K%', 'BB%', 'BABIP',
            'ERA', 'xFIP', 'WHIP', 'xwoba', 'AVG', 'xba', 'FB%', 'GB%', 'LD%', 'HR/9', 'Soft%',
            'Hard%', 'HR/FB', 'K-BB%', 'LOB%', 'angle', 'velo']
    frame = frame[cols]
    return frame

with open('/home/Jon2Anderson/mlb/dailystore/%sprobables.json' %date, 'r') as f:
    probables = json.load(f)

with open('/home/Jon2Anderson/mlb/dailystore/%smatchups.json' %date, 'r') as f:
    matchups = json.load(f)

with open('/home/Jon2Anderson/mlb/dailystore/rostersmaster.json', 'r') as f:
    masterhand = json.load(f)

teams = list(matchups.keys())
masterframe = pd.DataFrame()
for team in teams:
    print(team)
    frame = getPitcherData(team)
    masterframe = masterframe.append(frame)
    framevr = getPitcherDataVR(team)
    masterframe = masterframe.append(framevr)
    framevl = getPitcherDataVL(team)
    masterframe = masterframe.append(framevl)

masterframe.to_csv('/home/Jon2Anderson/mlb/dailysheets/%s_PitchersReport_Splits19.csv' %date)
print('done')
