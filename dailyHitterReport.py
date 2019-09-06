import os, datetime, json, csv, pandas as pd

month = datetime.date.today().strftime("%B")
day = datetime.date.today().strftime("%d")
date = month + day

############### Import Everything We Need ###############
os.chdir('/home/Jon2Anderson/mlb/datarepo/master')
hitmaster = pd.read_csv('hitmaster19.csv')
hitmaster = hitmaster.drop(['Team'], axis=1)
hitvrmaster = pd.read_csv('hitvrmaster19.csv')
hitvrmaster = hitvrmaster.drop(['Team'], axis=1)
hitvlmaster = pd.read_csv('hitvlmaster19.csv')
hitvlmaster = hitvlmaster.drop(['Team'], axis=1)
allhitters = hitmaster['Name'].tolist()
with open('/home/Jon2Anderson/mlb/dailystore/%sprobables.json'  % date, 'r') as f:
    probables = json.load(f)
with open('/home/Jon2Anderson/mlb/dailystore/%slineups.json' %date, 'r') as f:
    lineups = json.load(f)
with open('/home/Jon2Anderson/mlb/dailystore/rostersmaster.json', 'r') as f:
    masterhand = json.load(f)
with open('/home/Jon2Anderson/mlb/dailystore/%smatchups.json' %date, 'r') as f:
    matchups = json.load(f)
#########################################################

def getStatsvr(team, lineup, pitcher, pitcherhand):
    print('Input received, working on ' + team)
    df = pd.DataFrame()

    for player in lineup:
        df['Pitcher']=pitcher
        hitterhand = masterhand.get(player)
        if player in allhitters:
            row = hitvrmaster[hitvrmaster['Name']==player]
            if row.empty:
                luspot = lineup.index(player)+1
                dummydict = {'Name': player, 'Team': team, 'hand': hitterhand, 'LU Spot': luspot, 'Pitcher': pitcher,
                            'R/L': pitcherhand, 'PA':'', 'wOBA':'', 'wRC+':'', 'AVG':'',
                            'OBP':'', 'SLG':'', 'ISO':'', 'K%':'', 'BB%':'', 'GB%':'', 'FB%':'',
                            'LD%':'', 'Soft%':'', 'Hard%':'', 'BABIP':'', 'HR':'', 'HR/FB':'',
                            'xwoba': '', 'xba': '', 'velo': '', 'angle': ''}
                row2=pd.DataFrame()
                row2 = row2.append(dummydict, ignore_index=True)
                row2['LU Spot']=luspot
                row2['hand'] = hitterhand
                df = df.append(row2)
            else:
                luspot = lineup.index(player)+1
                row['LU Spot'] = luspot
                row['hand'] = hitterhand
                row['R/L'] = pitcherhand
                df = df.append(row)
        elif player not in allhitters:
            luspot = lineup.index(player)+1
            dummydict = {'Name': player, 'Team': team, 'hand': hitterhand, 'LU Spot': luspot, 'Pitcher': pitcher,
                        'R/L': pitcherhand, 'PA':'', 'wOBA':'', 'wRC+':'', 'AVG':'',
                        'OBP':'', 'SLG':'', 'ISO':'', 'K%':'', 'BB%':'', 'GB%':'', 'FB%':'',
                        'LD%':'', 'Soft%':'', 'Hard%':'', 'BABIP':'', 'HR':'', 'HR/FB':'',
                        'xwoba': '', 'xba': '', 'velo': '', 'angle': ''}
            df = df.append(dummydict, ignore_index=True)
        df['Team']=team
        df['Pitcher']=pitcher
        df['LU?']='y'
        df['R/L']=pitcherhand
    return(df)

def getStatsvl(team, lineup, pitcher, pitcherhand):
    print('Input received, working on ' + team)
    df = pd.DataFrame()

    for player in lineup:
        df['Pitcher']=pitcher
        hitterhand = masterhand.get(player)
        if player in allhitters:
            row = hitvlmaster[hitvlmaster['Name']==player]
            if row.empty:
                luspot = lineup.index(player)+1
                dummydict = {'Name': player, 'Team': team, 'hand': hitterhand, 'LU Spot': luspot, 'Pitcher': pitcher,
                            'R/L': pitcherhand, 'PA':'', 'wOBA':'', 'wRC+':'', 'AVG':'',
                            'OBP':'', 'SLG':'', 'ISO':'', 'K%':'', 'BB%':'', 'GB%':'', 'FB%':'',
                            'LD%':'', 'Soft%':'', 'Hard%':'', 'BABIP':'', 'HR':'', 'HR/FB':'',
                            'xwoba': '', 'xba': '', 'velo': '', 'angle': ''}
                row2=pd.DataFrame()
                row2 = row2.append(dummydict, ignore_index=True)
                row2['LU Spot']=luspot
                row['hand'] = hitterhand
                df = df.append(row2)
            else:
                luspot = lineup.index(player)+1
                row['LU Spot'] = luspot
                row['hand'] = hitterhand
                row['R/L'] = pitcherhand
                df = df.append(row)
        elif player not in allhitters:
            luspot = lineup.index(player)+1
            dummydict = {'Name': player, 'Team': team, 'hand': hitterhand, 'LU Spot': luspot, 'Pitcher': pitcher,
                            'R/L': pitcherhand, 'PA':'', 'wOBA':'', 'wRC+':'', 'AVG':'',
                            'OBP':'', 'SLG':'', 'ISO':'', 'K%':'', 'BB%':'', 'GB%':'', 'FB%':'',
                            'LD%':'', 'Soft%':'', 'Hard%':'', 'BABIP':'', 'HR':'', 'HR/FB':'',
                            'xwoba': '', 'xba': '', 'velo': '', 'angle': ''}
            df = df.append(dummydict, ignore_index=True)
        df['Team']=team
        df['Pitcher']=pitcher
        df['Pitch R/L']=pitcherhand
        df['LU?']='y'
    return(df)

def getStatsNoLineupvr(team, lineup, pitcher, pitcherhand):
    print('Input received, working on ' + team)
    df = pd.DataFrame()

    for player in lineup:
        df['Pitcher']=pitcher
        hitterhand = masterhand.get(player)
        if player in allhitters:
            row = hitvrmaster[hitvrmaster['Name']==player]
            if row.empty:
                luspot = lineup.index(player)+1
                dummydict = {'Name': player, 'Team': team, 'hand': hitterhand, 'LU Spot': luspot, 'Pitcher': pitcher,
                            'R/L': pitcherhand, 'PA':'', 'wOBA':'', 'wRC+':'', 'AVG':'',
                            'OBP':'', 'SLG':'', 'ISO':'', 'K%':'', 'BB%':'', 'GB%':'', 'FB%':'',
                            'LD%':'', 'Soft%':'', 'Hard%':'', 'BABIP':'', 'HR':'', 'HR/FB':'',
                            'xwoba': '', 'xba': '', 'velo': '', 'angle': ''}
                row2=pd.DataFrame()
                row2 = row2.append(dummydict, ignore_index=True)
                row2['LU Spot']=luspot
                row2['hand'] = hitterhand
                df = df.append(row2)
            else:
                luspot = lineup.index(player)+1
                row['LU Spot'] = luspot
                row['hand'] = hitterhand
                row['R/L'] = pitcherhand
                df = df.append(row)
        elif player not in allhitters:
            luspot = lineup.index(player)+1
            dummydict = {'Name': player, 'Team': team, 'hand': hitterhand, 'LU Spot': luspot, 'Pitcher': pitcher,
                            'R/L': pitcherhand, 'PA':'', 'wOBA':'', 'wRC+':'', 'AVG':'',
                            'OBP':'', 'SLG':'', 'ISO':'', 'K%':'', 'BB%':'', 'GB%':'', 'FB%':'',
                            'LD%':'', 'Soft%':'', 'Hard%':'', 'BABIP':'', 'HR':'', 'HR/FB':'',
                            'xwoba': '', 'xba': '', 'velo': '', 'angle': ''}
            df = df.append(dummydict, ignore_index=True)
        df['Team']=team
        df['Pitcher']=pitcher
        df['Pitch R/L']=pitcherhand
        df['LU?']='n'
    return(df)

def getStatsNoLineupvl(team, lineup, pitcher, pitcherhand):
    print('Input received, working on ' + team)
    df = pd.DataFrame()

    for player in lineup:
        df['Pitcher']=pitcher
        hitterhand = masterhand.get(player)
        if player in allhitters:
            row = hitvlmaster[hitvlmaster['Name']==player]
            if row.empty:
                luspot = lineup.index(player)+1
                dummydict = {'Name': player, 'Team': team, 'hand': hitterhand, 'LU Spot': luspot, 'Pitcher': pitcher,
                            'R/L': pitcherhand, 'PA':'', 'wOBA':'', 'wRC+':'', 'AVG':'',
                            'OBP':'', 'SLG':'', 'ISO':'', 'K%':'', 'BB%':'', 'GB%':'', 'FB%':'',
                            'LD%':'', 'Soft%':'', 'Hard%':'', 'BABIP':'', 'HR':'', 'HR/FB':'',
                            'xwoba': '', 'xba': '', 'velo': '', 'angle': ''}
                row2=pd.DataFrame()
                row2 = row2.append(dummydict, ignore_index=True)
                row2['LU Spot']=luspot
                row['hand'] = hitterhand
                df = df.append(row2)
            else:
                luspot = lineup.index(player)+1
                row['LU Spot'] = luspot
                row['hand'] = hitterhand
                row['R/L'] = pitcherhand
                df = df.append(row)
        elif player not in allhitters:
            luspot = lineup.index(player)+1
            dummydict = {'Name': player, 'Team': team, 'hand': hitterhand, 'LU Spot': luspot, 'Pitcher': pitcher,
                            'R/L': pitcherhand, 'PA':'', 'wOBA':'', 'wRC+':'', 'AVG':'',
                            'OBP':'', 'SLG':'', 'ISO':'', 'K%':'', 'BB%':'', 'GB%':'', 'FB%':'',
                            'LD%':'', 'Soft%':'', 'Hard%':'', 'BABIP':'', 'HR':'', 'HR/FB':'',
                            'xwoba': '', 'xba': '', 'velo': '', 'angle': ''}
            df = df.append(dummydict, ignore_index=True)
        df['Team']=team
        df['Pitcher']=pitcher
        df['Pitch R/L']=pitcherhand
        df['LU?']='n'
    return(df)

masterdf = pd.DataFrame()
teams = list(lineups.keys())
for team in teams:
    lineup = lineups.get(team)
    if lineup == 'no lineup has been posted yet':
        pitcher = probables.get(matchups.get(team))
        pitcherhand = masterhand.get(pitcher)
        team = team.replace('2', '')
        team = team.replace('1', '')
        print('no lineup for ' + team + ', importing projected lineup.')

        with open('/home/Jon2Anderson/mlb/lineups/%sprojlineup.json' %team, 'r') as f:
            lineup = json.load(f)

        if pitcherhand == 'l':
            df = getStatsNoLineupvl(team, lineup, pitcher, pitcherhand)
            cols = ['Name', 'Team', 'hand', 'LU Spot', 'LU?', 'Pitcher', 'R/L', 'PA', 'wOBA', 'wRC+', 'AVG', 'OBP', 'SLG', 'ISO', 'K%', 'BB%', 'GB%', 'FB%', 'LD%', 'Soft%', 'Hard%', 'BABIP', 'HR', 'HR/FB', 'xwoba', 'xba', 'velo', 'angle']
            df = df[cols]
            masterdf = masterdf.append(df)
        else:
            df = getStatsNoLineupvr(team, lineup, pitcher, pitcherhand)
            cols = ['Name', 'Team', 'hand', 'LU Spot', 'LU?', 'Pitcher', 'R/L', 'PA', 'wOBA', 'wRC+', 'AVG', 'OBP', 'SLG', 'ISO', 'K%', 'BB%', 'GB%', 'FB%', 'LD%', 'Soft%', 'Hard%', 'BABIP', 'HR', 'HR/FB', 'xwoba', 'xba', 'velo', 'angle']
            df = df[cols]
            masterdf = masterdf.append(df)
    else:
        pitcher = probables.get(matchups.get(team))
        pitcherhand = masterhand.get(pitcher)
        if pitcherhand == 'l':
            df = getStatsvl(team, lineup, pitcher, pitcherhand)
        else:
            df = getStatsvr(team, lineup, pitcher, pitcherhand)
        cols = ['Name', 'Team', 'hand', 'LU Spot', 'LU?', 'Pitcher', 'R/L', 'PA', 'wOBA', 'wRC+', 'AVG', 'OBP', 'SLG', 'ISO', 'K%', 'BB%', 'GB%', 'FB%', 'LD%', 'Soft%', 'Hard%', 'BABIP', 'HR', 'HR/FB', 'xwoba', 'xba', 'velo', 'angle']
        df = df[cols]
        masterdf = masterdf.append(df)

masterdf.to_csv('/home/Jon2Anderson/mlb/dailysheets/%s_HittersReport_Splits19.csv' %date)
