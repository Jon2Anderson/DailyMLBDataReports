# -*- coding: utf-8 -*-
import pandas as pd, requests, os, collections as co, json
from bs4 import BeautifulSoup
from functools import reduce
import shutil

## The getstan function retrieves standard statistics from fangraphs.com
def getStan():
    
    # Send URL through BeautifulSoup to retrieve the web page source code
    url = 'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=10&type=0&season=2019&month=0&season1=2018&ind=0&team=0&rost=0&age=0&filter=&players=0&page=1_5000'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    
    # Isolated rgMasterTable, where our desired data lives
    table = soup.find('table', {'class': 'rgMasterTable'})
    
    # Split table body and table head so we know what to name the columns
    table_body = table.find('tbody')
    table_head = table.find('thead')

    # Loop through column names and store them in list
    header=[]
    for th in table_head.findAll('th'):
        key = th.get_text()
        header.append(key)

    # Loop through table row data and store them in list
    trlist=[]
    for tr in table_body.findAll('tr'):
        trlist.append(tr)

    # Create a list that we will store dictionaries in before compiling them all together
    listofdicts=[]

    # Loop through all the rows and match each up with the table header
    for row in trlist:
        the_row=[]
        for td in row.findAll('td'):
            the_row.append(td.text)
        od = co.OrderedDict(zip(header, the_row))
        listofdicts.append(od)

    # Create dataframe with pandas, making everything lower case
    standf = pd.DataFrame(listofdicts)
    standf = standf.apply(lambda x: x.astype(str).str.lower())
    
    # We are using two different websites for data collection, and both websites do not necessarily
    # use the same name for players, so we will use these two lists to change names so they match
    oldnames=['nick castellanos', 'yulieski gurriel', 'nick delmonico', 'gregory bird',
                'dan vogelbach', 'chris bostick', 'nori aoki', 'j.t. riddle', 'cam perkins',
                'daniel winkler', 'samuel tuivailala', 'jake faria', 'chase bradford',
                'a.j. ramos', 'nathan karns', 'lance mccullers', 'matt boyd', 'jake junis',
                'luke sims', 'ben gamel']
    newnames=['nicholas castellanos', 'yuli gurriel', 'nicky delmonico', 'greg bird',
                'daniel vogelbach', 'christopher bostick', 'norichika aoki', 'jt riddle',
                'cameron perkins', 'dan winkler', 'sam tuivailala', 'jacob faria',
                'chasen bradford', 'aj ramos', 'nate karns', 'lance mccullers jr.', 'matthew boyd',
                'jakob junis', 'lucas sims', 'benjamin gamel']
    
    for i in range(len(newnames)):
        standf['Name'] = standf['Name'].str.replace(oldnames[i], newnames[i])
    
    # Select desired columsn from data frame and we are done
    standf = standf[['Name', 'AB', 'PA', 'H', '1B', '2B', '3B', 'HR', 'BB', 'IBB', 'SO', 'HBP', 'SF']]
    return(standf)

# Retrieve advanced statistics from fangraphs
def getAdv():
    url = 'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=10&type=1&season=2019&month=0&season1=2018&ind=0&team=0&rost=0&age=0&filter=&players=0&page=1_5000'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.find('table', {'class': 'rgMasterTable'})
    table_body = table.find('tbody')
    table_head = table.find('thead')

    header=[]
    for th in table_head.findAll('th'):
        key = th.get_text()
        header.append(key)

    trlist=[]
    for tr in table_body.findAll('tr'):
        trlist.append(tr)

    listofdicts=[]

    for row in trlist:
        the_row=[]
        for td in row.findAll('td'):
            the_row.append(td.text)
        od = co.OrderedDict(zip(header, the_row))
        listofdicts.append(od)

    advdf = pd.DataFrame(listofdicts)
    advdf = advdf.apply(lambda x: x.astype(str).str.lower())
    oldnames=['nick castellanos', 'yulieski gurriel', 'nick delmonico', 'gregory bird',
                'dan vogelbach', 'chris bostick', 'nori aoki', 'j.t. riddle', 'cam perkins',
                'daniel winkler', 'samuel tuivailala', 'jake faria', 'chase bradford',
                'a.j. ramos', 'nathan karns', 'lance mccullers', 'matt boyd', 'jake junis',
                'luke sims', 'ben gamel']
    newnames=['nicholas castellanos', 'yuli gurriel', 'nicky delmonico', 'greg bird',
                'daniel vogelbach', 'christopher bostick', 'norichika aoki', 'jt riddle',
                'cameron perkins', 'dan winkler', 'sam tuivailala', 'jacob faria',
                'chasen bradford', 'aj ramos', 'nate karns', 'lance mccullers jr.', 'matthew boyd',
                'jakob junis', 'lucas sims', 'benjamin gamel']
    for i in range(len(newnames)):
        advdf['Name'] = advdf['Name'].str.replace(oldnames[i], newnames[i])

    advdf = advdf[advdf.Name != 'daniel robertson']
    advdf = advdf[['Name', 'wRC+']]
    return(advdf)

# Retrieve standard statistics for hitters against right handed pitchers from fangraphs
def getStanVR():
    url = 'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=10&type=0&season=2019&month=14&season1=2018&ind=0&team=0&rost=0&age=0&filter=&players=0&page=1_5000'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.find('table', {'class': 'rgMasterTable'})
    table_body = table.find('tbody')
    table_head = table.find('thead')

    header=[]
    for th in table_head.findAll('th'):
        key = th.get_text()
        header.append(key)

    trlist=[]
    for tr in table_body.findAll('tr'):
        trlist.append(tr)

    listofdicts=[]

    for row in trlist:
        the_row=[]
        for td in row.findAll('td'):
            the_row.append(td.text)
        od = co.OrderedDict(zip(header, the_row))
        listofdicts.append(od)

    standf = pd.DataFrame(listofdicts)
    standf = standf.apply(lambda x: x.astype(str).str.lower())
    oldnames=['nick castellanos', 'yulieski gurriel', 'nick delmonico', 'gregory bird',
                'dan vogelbach', 'chris bostick', 'nori aoki', 'j.t. riddle', 'cam perkins',
                'daniel winkler', 'samuel tuivailala', 'jake faria', 'chase bradford',
                'a.j. ramos', 'nathan karns', 'lance mccullers', 'matt boyd', 'jake junis',
                'luke sims', 'ben gamel']
    newnames=['nicholas castellanos', 'yuli gurriel', 'nicky delmonico', 'greg bird',
                'daniel vogelbach', 'christopher bostick', 'norichika aoki', 'jt riddle',
                'cameron perkins', 'dan winkler', 'sam tuivailala', 'jacob faria',
                'chasen bradford', 'aj ramos', 'nate karns', 'lance mccullers jr.', 'matthew boyd',
                'jakob junis', 'lucas sims', 'benjamin gamel']
    for i in range(len(newnames)):
        standf['Name'] = standf['Name'].str.replace(oldnames[i], newnames[i])
    standf = standf[standf.Name != 'daniel robertson']
    standf = standf[['Name', 'AB', 'PA', 'H', '1B', '2B', '3B', 'HR', 'BB', 'IBB', 'SO', 'HBP', 'SF']]
    return(standf)

# Retrieve advanced statistics for hitters against right handed pitchers from fangraphs

def getAdvVR():
    url = 'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=10&type=1&season=2019&month=14&season1=2018&ind=0&team=0&rost=0&age=0&filter=&players=0&page=1_5000'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.find('table', {'class': 'rgMasterTable'})
    table_body = table.find('tbody')
    table_head = table.find('thead')

    header=[]
    for th in table_head.findAll('th'):
        key = th.get_text()
        header.append(key)

    trlist=[]
    for tr in table_body.findAll('tr'):
        trlist.append(tr)

    listofdicts=[]

    for row in trlist:
        the_row=[]
        for td in row.findAll('td'):
            the_row.append(td.text)
        od = co.OrderedDict(zip(header, the_row))
        listofdicts.append(od)

    advdf = pd.DataFrame(listofdicts)
    advdf = advdf.apply(lambda x: x.astype(str).str.lower())
    oldnames=['nick castellanos', 'yulieski gurriel', 'nick delmonico', 'gregory bird',
                'dan vogelbach', 'chris bostick', 'nori aoki', 'j.t. riddle', 'cam perkins',
                'daniel winkler', 'samuel tuivailala', 'jake faria', 'chase bradford',
                'a.j. ramos', 'nathan karns', 'lance mccullers', 'matt boyd', 'jake junis',
                'luke sims', 'ben gamel']
    newnames=['nicholas castellanos', 'yuli gurriel', 'nicky delmonico', 'greg bird',
                'daniel vogelbach', 'christopher bostick', 'norichika aoki', 'jt riddle',
                'cameron perkins', 'dan winkler', 'sam tuivailala', 'jacob faria',
                'chasen bradford', 'aj ramos', 'nate karns', 'lance mccullers jr.', 'matthew boyd',
                'jakob junis', 'lucas sims', 'benjamin gamel']
    for i in range(len(newnames)):
        advdf['Name'] = advdf['Name'].str.replace(oldnames[i], newnames[i])

    advdf = advdf[advdf.Name != 'daniel robertson']
    advdf = advdf[['Name', 'wRC+']]
    return(advdf)

# Retrieve standard statistics for hitters against left handed pitchers from fangraphs
def getStanVL():
    url = 'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=10&type=0&season=2019&month=13&season1=2018&ind=0&team=0&rost=0&age=0&filter=&players=0&page=1_5000'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.find('table', {'class': 'rgMasterTable'})
    table_body = table.find('tbody')
    table_head = table.find('thead')

    header=[]
    for th in table_head.findAll('th'):
        key = th.get_text()
        header.append(key)

    trlist=[]
    for tr in table_body.findAll('tr'):
        trlist.append(tr)

    listofdicts=[]

    for row in trlist:
        the_row=[]
        for td in row.findAll('td'):
            the_row.append(td.text)
        od = co.OrderedDict(zip(header, the_row))
        listofdicts.append(od)

    standf = pd.DataFrame(listofdicts)
    standf = standf.apply(lambda x: x.astype(str).str.lower())
    oldnames=['nick castellanos', 'yulieski gurriel', 'nick delmonico', 'gregory bird',
                'dan vogelbach', 'chris bostick', 'nori aoki', 'j.t. riddle', 'cam perkins',
                'daniel winkler', 'samuel tuivailala', 'jake faria', 'chase bradford',
                'a.j. ramos', 'nathan karns', 'lance mccullers', 'matt boyd', 'jake junis',
                'luke sims', 'ben gamel']
    newnames=['nicholas castellanos', 'yuli gurriel', 'nicky delmonico', 'greg bird',
                'daniel vogelbach', 'christopher bostick', 'norichika aoki', 'jt riddle',
                'cameron perkins', 'dan winkler', 'sam tuivailala', 'jacob faria',
                'chasen bradford', 'aj ramos', 'nate karns', 'lance mccullers jr.', 'matthew boyd',
                'jakob junis', 'lucas sims', 'benjamin gamel']
    for i in range(len(newnames)):
        standf['Name'] = standf['Name'].str.replace(oldnames[i], newnames[i])
    standf = standf[standf.Name != 'daniel robertson']
    standf = standf[['Name', 'AB', 'PA', 'H', '1B', '2B', '3B', 'HR', 'BB', 'IBB', 'SO', 'HBP', 'SF']]
    return(standf)

# Retrieve advanced statistics for hitters against left handed pitchers from fangraphs
def getAdvVL():
    url = 'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=10&type=1&season=2019&month=13&season1=2018&ind=0&team=0&rost=0&age=0&filter=&players=0&page=1_5000'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.find('table', {'class': 'rgMasterTable'})
    table_body = table.find('tbody')
    table_head = table.find('thead')

    header=[]
    for th in table_head.findAll('th'):
        key = th.get_text()
        header.append(key)

    trlist=[]
    for tr in table_body.findAll('tr'):
        trlist.append(tr)

    listofdicts=[]

    for row in trlist:
        the_row=[]
        for td in row.findAll('td'):
            the_row.append(td.text)
        od = co.OrderedDict(zip(header, the_row))
        listofdicts.append(od)

    advdf = pd.DataFrame(listofdicts)
    advdf = advdf.apply(lambda x: x.astype(str).str.lower())
    oldnames=['nick castellanos', 'yulieski gurriel', 'nick delmonico', 'gregory bird',
                'dan vogelbach', 'chris bostick', 'nori aoki', 'j.t. riddle', 'cam perkins',
                'daniel winkler', 'samuel tuivailala', 'jake faria', 'chase bradford',
                'a.j. ramos', 'nathan karns', 'lance mccullers', 'matt boyd', 'jake junis',
                'luke sims', 'ben gamel']
    newnames=['nicholas castellanos', 'yuli gurriel', 'nicky delmonico', 'greg bird',
                'daniel vogelbach', 'christopher bostick', 'norichika aoki', 'jt riddle',
                'cameron perkins', 'dan winkler', 'sam tuivailala', 'jacob faria',
                'chasen bradford', 'aj ramos', 'nate karns', 'lance mccullers jr.', 'matthew boyd',
                'jakob junis', 'lucas sims', 'benjamin gamel']
    for i in range(len(newnames)):
        advdf['Name'] = advdf['Name'].str.replace(oldnames[i], newnames[i])

    advdf = advdf[advdf.Name != 'daniel robertson']
    advdf = advdf[['Name', 'wRC+']]
    return(advdf)

# Scrape through baseball savant pages
def savantScrape(url):
    # Use BeautifulSoup to scrape the source code for the given URL from baseball savant
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    
    # Isolate the desired table, and split off the head and body
    table = soup.find('table', {'class': 'tablesorter table table-bordered table-hover'})
    table_body = table.find('tbody')
    table_head = table.find('thead')

    # Loop through th tags and store the values in a list
    header = []
    for th in table_head.findAll('th'):
        key = th.get_text()
        key =  key.replace('\n', '')
        key = key.replace(' ', '')
        header.append(key)

    # We are only interested in the first five columns of the table, so let's cut down the list
    header = header[0:5]
    
    # Loop through tr values, storing them in a listt
    trlist = []
    for tr in table_body.findAll('tr'):
        trlist.append(tr)
    
    # Loop through td values and store them in a list
    listofdicts = []
    namelist=[]
    for row in trlist:
        for td in row.findAll('td', {'class': 'player_name'}):
            name = td.text.lower()
            namelist.append(name)

    # Go through data and pair each row with the header so we can join them all together
    for row in trlist:
        therow=[]
        for td in row.findAll('td', {'class': 'numeric'}):
            text = td.text
            text = text.replace(' ', '')
            text = text.replace('\n', '')
            therow.append(text)
        od = co.OrderedDict(zip(header, therow))
        listofdicts.append(od)

    # Create the dataframe
    savdf = pd.DataFrame(listofdicts)
    savdf = savdf.iloc[::2, :]
    savdf['Name']=namelist
    savdf = savdf[['Name', 'Player']]
    savdf = savdf.rename(index=str, columns={'Player': 'Stat'})
    oldnames=['nick castellanos', 'yulieski gurriel', 'nick delmonico', 'gregory bird',
                'dan vogelbach', 'chris bostick', 'nori aoki', 'j.t. riddle', 'cam perkins',
                'daniel winkler', 'samuel tuivailala', 'jake faria', 'chase bradford',
                'a.j. ramos', 'nathan karns', 'lance mccullers', 'matt boyd', 'jake junis',
                'luke sims', 'felipe rivero', 'ben gamel']
    newnames=['nicholas castellanos', 'yuli gurriel', 'nicky delmonico', 'greg bird',
                'daniel vogelbach', 'christopher bostick', 'norichika aoki', 'jt riddle',
                'cameron perkins', 'dan winkler', 'sam tuivailala', 'jacob faria',
                'chasen bradford', 'aj ramos', 'nate karns', 'lance mccullers jr.', 'matthew boyd',
                'jakob junis', 'lucas sims', 'felipe vazquez', 'benjamin gamel']
    
    for i in range(len(newnames)):
        savdf['Name'] = savdf['Name'].str.replace(oldnames[i], newnames[i])
    return(savdf)

def getFangraphs(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.find('table', {'class': 'rgMasterTable'})
    tbody = table.find('tbody')
    thead = table.find('thead')
    header=[]
    for th in thead.findAll('th'):
        key = th.get_text()
        header.append(key)
    trlist=[]
    for tr in tbody.findAll('tr'):
        trlist.append(tr)
    listofdicts=[]
    for row in trlist:
        the_row=[]
        for td in row.findAll('td'):
            the_row.append(td.text)
        od = co.OrderedDict(zip(header, the_row))
        listofdicts.append(od)
    df = pd.DataFrame(listofdicts)
    df = df.apply(lambda x: x.astype(str).str.lower())
    oldnames=['peter alonso', 'nick castellanos', 'yulieski gurriel', 'nick delmonico', 'gregory bird',
                'dan vogelbach', 'chris bostick', 'nori aoki', 'j.t. riddle', 'cam perkins',
                'eric young', 'dwight smith', 'daniel winkler', 'samuel tuivailala',
                'jake faria', 'chase bradford', 'a.j. ramos', 'nathan karns', 'lance mccullers',
                'matt boyd', 'jake junis', 'luke sims', 'ben gamel']
    newnames=['pete alonso', 'nicholas castellanos', 'yuli gurriel', 'nicky delmonico', 'greg bird',
                'daniel vogelbach', 'christopher bostick', 'norichika aoki', 'jt riddle',
                'cameron perkins', 'eric young jr.', 'dwight smith jr.', 'dan winkler',
                'sam tuivailala', 'jacob faria', 'chasen bradford', 'aj ramos',
                'nate karns', 'lance mccullers jr.', 'matthew boyd', 'jakob junis',
                'lucas sims', 'benjamin gamel']
    for i in range(len(newnames)):
        df['Name'] = df['Name'].str.replace(oldnames[i], newnames[i])
    df = df[df.Name != 'daniel robertson']
    return df

# Functions to merge all of the tables we got from fangraphs to make one master data frame
def mergeFangraphsHit(standf, advdf, bbdf):
    standf = standf[['Name', 'Team', 'PA', 'HR', 'AVG']]
    advdf = advdf[['Name', 'BB%', 'K%', 'OBP', 'SLG', 'ISO', 'BABIP', 'wOBA', 'wRC+']]
    bbdf = bbdf[['Name', 'LD%', 'GB%', 'FB%', 'HR/FB', 'Soft%', 'Hard%']]
    bridge = pd.merge(standf, advdf, on='Name')
    hitdf = pd.merge(bridge, bbdf, on='Name')
    return(hitdf)

def mergeFangraphsPitch(standf, advdf, bbdf):
    standf = standf[['Name', 'Team', 'IP', 'ERA']]
    advdf = advdf[['Name', 'HR/9', 'K%', 'BB%', 'K-BB%', 'AVG', 'WHIP', 'BABIP', 'LOB%', 'xFIP']]
    bbdf = bbdf[['Name', 'LD%', 'GB%', 'FB%', 'HR/FB', 'Soft%', 'Hard%']]
    bridge = pd.merge(standf, advdf, on='Name')
    pitchdf = pd.merge(bridge, bbdf, on='Name')
    return(pitchdf)

# Functions to merge the fangraphs data and the baseball savant data
def mergeHittingData(fgdf, savdf):
    df = pd.merge(fgdf, savdf, on="Name")
    return(df)

def mergePitchingData(fgdf, savdf):
    df = pd.merge(fgdf, savdf, on="Name")
    return(df)


# We have a bunch of different URL's to use for the fangraphs data, so I stored them
# all in a file that we will load and then send each URL to a function to get the tables
with open('/home/Jon2Anderson/mlb/datarepo/master/urldict/urldict1819.json', 'r') as f:
    urldict = json.load(f)

titles = list(urldict.keys())
urls = list(urldict.values())
i=0

# Send each URL through the getFangraphs function, this will create CSV files for
# each table we want and save them off
print('working on fangraphs data...')
for url in urls:
    print('working on ' + titles[i])
    print(url)
    df = getFangraphs(url)
    df.to_csv('%s18.csv' %titles[i])
    i=i+1
    
# Read in each dataframe we created by looping through all the URLs so we can merge 
# them all together
hitstandf = pd.read_csv('hitstan18.csv')
hitadvdf = pd.read_csv('hitadv18.csv')
hitbbdf = pd.read_csv('hitbb18.csv')
hitvrstandf = pd.read_csv('hitvrstan18.csv')
hitvradvdf = pd.read_csv('hitvradv18.csv')
hitvrbbdf = pd.read_csv('hitvrbb18.csv')
hitvlstandf = pd.read_csv('hitvlstan18.csv')
hitvladvdf = pd.read_csv('hitvladv18.csv')
hitvlbbdf = pd.read_csv('hitvlbb18.csv')

pitchstandf = pd.read_csv('pitchstan18.csv')
pitchadvdf = pd.read_csv('pitchadv18.csv')
pitchbbdf = pd.read_csv('pitchbb18.csv')
pitchvrstandf = pd.read_csv('pitchvrstan18.csv')
pitchvradvdf = pd.read_csv('pitchvradv18.csv')
pitchvrbbdf = pd.read_csv('pitchvrbb18.csv')
pitchvlstandf = pd.read_csv('pitchvlstan18.csv')
pitchvladvdf = pd.read_csv('pitchvladv18.csv')
pitchvlbbdf = pd.read_csv('pitchvlbb18.csv')

# Merge all the hitting and pitching dataframes together 
print('data collected, merging all data...')
hitstan = mergeFangraphsHit(hitstandf, hitadvdf, hitbbdf)
hitvr = mergeFangraphsHit(hitvrstandf, hitvradvdf, hitvrbbdf)
hitvl = mergeFangraphsHit(hitvlstandf, hitvladvdf, hitvlbbdf)
pitchstan = mergeFangraphsPitch(pitchstandf, pitchadvdf, pitchbbdf)
pitchvr = mergeFangraphsPitch(pitchvrstandf, pitchvradvdf, pitchvrbbdf)
pitchvl = mergeFangraphsPitch(pitchvlstandf, pitchvladvdf, pitchvlbbdf)
hitstan.to_csv('hitfgstan18.csv')
hitvr.to_csv('hitfgvr18.csv')
hitvl.to_csv('hitfgvl18.csv')
pitchstan.to_csv('pitchfgstan18.csv')
pitchvr.to_csv('pitchfgvr18.csv')

# Here are all the baseball savant URL's we need to use. Due to how the site
# is set up, we need a different URL for each stat we want. We want to collect
# four different stats in three different "splits" (total, vs. lefties, and vs.
# righties) for both hitters & pitchers, so we have 24 URL's here.
hitxwobaurl = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2019%7C2018%7C&hfSit=&player_type=batter&hfOuts=&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=xwoba&player_event_sort=h_%s&sort_order=desc&min_abs=10#results"
hitxbaurl = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2019%7C2018%7C&hfSit=&player_type=batter&hfOuts=&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=xba&player_event_sort=h_%s&sort_order=desc&min_abs=10#results"
hitvelourl = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2019%7C2018%7C&hfSit=&player_type=batter&hfOuts=&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=launch_speed&player_event_sort=h_%s&sort_order=desc&min_abs=10#results"
hitangleurl = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2019%7C2018%7C&hfSit=&player_type=batter&hfOuts=&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=launch_angle&player_event_sort=h_%s&sort_order=desc&min_abs=10#results"
hitvrxwobaurl = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2019%7C2018%7C&hfSit=&player_type=batter&hfOuts=&opponent=&pitcher_throws=R&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=xwoba&player_event_sort=h_%s&sort_order=desc&min_abs=10#results"
hitvrxbaurl = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2019%7C2018%7C&hfSit=&player_type=batter&hfOuts=&opponent=&pitcher_throws=R&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=xba&player_event_sort=h_%s&sort_order=desc&min_abs=10#results"
hitvrvelourl = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2019%7C2018%7C&hfSit=&player_type=batter&hfOuts=&opponent=&pitcher_throws=R&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=launch_speed&player_event_sort=h_%s&sort_order=desc&min_abs=10#results"
hitvrangleurl = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2019%7C2018%7C&hfSit=&player_type=batter&hfOuts=&opponent=&pitcher_throws=R&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=launch_angle&player_event_sort=h_%s&sort_order=desc&min_abs=10#results"
hitvlxwobaurl = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2019%7C2018%7C&hfSit=&player_type=batter&hfOuts=&opponent=&pitcher_throws=L&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=xwoba&player_event_sort=h_%s&sort_order=desc&min_abs=10#results"
hitvlxbaurl = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2019%7C2018%7C&hfSit=&player_type=batter&hfOuts=&opponent=&pitcher_throws=L&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=xba&player_event_sort=h_%s&sort_order=desc&min_abs=10#results"
hitvlvelourl = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2019%7C2018%7C&hfSit=&player_type=batter&hfOuts=&opponent=&pitcher_throws=L&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=launch_speed&player_event_sort=h_%s&sort_order=desc&min_abs=10#results"
hitvlangleurl = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2019%7C2018%7C&hfSit=&player_type=batter&hfOuts=&opponent=&pitcher_throws=L&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=launch_angle&player_event_sort=h_%s&sort_order=desc&min_abs=10#results"
pitchxwobaurl = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2019%7C2018%7C&hfSit=&player_type=pitcher&hfOuts=&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=xwoba&player_event_sort=h_xwoba&sort_order=desc&min_abs=10#results"
pitchxbaurl = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2019%7C2018%7C&hfSit=&player_type=pitcher&hfOuts=&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=xba&player_event_sort=h_xba&sort_order=desc&min_abs=10#results"
pitchvelourl = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2019%7C2018%7C&hfSit=&player_type=pitcher&hfOuts=&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=launch_speed&player_event_sort=h_launch_speed&sort_order=desc&min_abs=10#results"
pitchangleurl = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2019%7C2018%7C&hfSit=&player_type=pitcher&hfOuts=&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=launch_angle&player_event_sort=h_launch_angle&sort_order=desc&min_abs=10#results"
pitchvrxwobaurl = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2019%7C2018%7C&hfSit=&player_type=pitcher&hfOuts=&opponent=&pitcher_throws=&batter_stands=R&hfSA=&game_date_gt=&game_date_lt=&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=xwoba&player_event_sort=h_xwoba&sort_order=desc&min_abs=10#results"
pitchvrxbaurl = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2019%7C2018%7C&hfSit=&player_type=pitcher&hfOuts=&opponent=&pitcher_throws=&batter_stands=R&hfSA=&game_date_gt=&game_date_lt=&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=xba&player_event_sort=h_xba&sort_order=desc&min_abs=10#results"
pitchvrvelourl = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2019%7C2018%7C&hfSit=&player_type=pitcher&hfOuts=&opponent=&pitcher_throws=&batter_stands=R&hfSA=&game_date_gt=&game_date_lt=&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=launch_speed&player_event_sort=h_launch_speed&sort_order=desc&min_abs=10#results"
pitchvrangleurl = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2019%7C2018%7C&hfSit=&player_type=pitcher&hfOuts=&opponent=&pitcher_throws=&batter_stands=R&hfSA=&game_date_gt=&game_date_lt=&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=launch_angle&player_event_sort=h_launch_angle&sort_order=desc&min_abs=10#results"
pitchvlxwobaurl = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2019%7C2018%7C&hfSit=&player_type=pitcher&hfOuts=&opponent=&pitcher_throws=&batter_stands=L&hfSA=&game_date_gt=&game_date_lt=&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=xwoba&player_event_sort=h_xwoba&sort_order=desc&min_abs=10#results"
pitchvlxbaurl = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2019%7C2018%7C&hfSit=&player_type=pitcher&hfOuts=&opponent=&pitcher_throws=&batter_stands=L&hfSA=&game_date_gt=&game_date_lt=&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=xba&player_event_sort=h_xba&sort_order=desc&min_abs=10#results"
pitchvlvelourl = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2019%7C2018%7C&hfSit=&player_type=pitcher&hfOuts=&opponent=&pitcher_throws=&batter_stands=L&hfSA=&game_date_gt=&game_date_lt=&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=launch_speed&player_event_sort=h_launch_speed&sort_order=desc&min_abs=10#results"
pitchvlangleurl = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea=2019%7C2018%7C&hfSit=&player_type=pitcher&hfOuts=&opponent=&pitcher_throws=&batter_stands=L&hfSA=&game_date_gt=&game_date_lt=&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=launch_angle&player_event_sort=h_launch_angle&sort_order=desc&min_abs=10#results"


# You will see some repetition here, we are sending each URL through the savantscrape function
# to get the tables for each desired stat
print('starting savant data...')
print('hitters, no hand')
hitxwobadf = savantScrape(hitxwobaurl)
hitxbadf = savantScrape(hitxbaurl)
hitvelodf = savantScrape(hitvelourl)
hitangledf = savantScrape(hitangleurl)
hitdfs = [hitxwobadf, hitxbadf, hitvelodf, hitangledf]
hitsav = reduce(lambda left,right: pd.merge(left,right,on='Name'), hitdfs)
hitsav.columns = ['Name', 'xwoba', 'xba', 'velo', 'angle']
hitsav['velo'] = hitsav['velo'].str.replace('MPH', '')
hitsav['angle'] = hitsav['angle'].str.replace('°', '')
hitsav.to_csv('/home/Jon2Anderson/mlb/datarepo/master/hitsavant18.csv')

print('hitters, vs righties')
hitvrxwobadf = savantScrape(hitvrxwobaurl)
hitvrxbadf = savantScrape(hitvrxbaurl)
hitvrvelodf = savantScrape(hitvrvelourl)
hitvrangledf = savantScrape(hitvrangleurl)
hitvrdfs = [hitvrxwobadf, hitvrxbadf, hitvrvelodf, hitvrangledf]
hitvrsav = reduce(lambda left,right: pd.merge(left,right,on='Name'), hitdfs)
hitvrsav.columns = ['Name', 'xwoba', 'xba', 'velo', 'angle']
hitvrsav['velo'] = hitvrsav['velo'].str.replace('MPH', '')
hitvrsav['angle'] = hitvrsav['angle'].str.replace('°', '')
hitvrsav.to_csv('/home/Jon2Anderson/mlb/datarepo/master/hitvrsavant18.csv')

print('hitters, vs lefties')
hitvlxwobadf = savantScrape(hitvlxwobaurl)
hitvlxbadf = savantScrape(hitvlxbaurl)
hitvlvelodf = savantScrape(hitvlvelourl)
hitvlangledf = savantScrape(hitvlangleurl)
hitvldfs = [hitvlxwobadf, hitvlxbadf, hitvlvelodf, hitvlangledf]
hitvlsav = reduce(lambda left,right: pd.merge(left,right,on='Name'), hitdfs)
hitvlsav.columns = ['Name', 'xwoba', 'xba', 'velo', 'angle']
hitvlsav['velo'] = hitvlsav['velo'].str.replace('MPH', '')
hitvlsav['angle'] = hitvlsav['angle'].str.replace('°', '')
hitvlsav.to_csv('/home/Jon2Anderson/mlb/datarepo/master/hitvlsavant18.csv')

print('pitchers, no hand')
pitchxwobadf = savantScrape(pitchxwobaurl)
pitchxbadf = savantScrape(pitchxbaurl)
pitchvelodf = savantScrape(pitchvelourl)
pitchangledf = savantScrape(pitchangleurl)
pitchdfs = [pitchxwobadf, pitchxbadf, pitchvelodf, pitchangledf]
pitchsav = reduce(lambda left,right: pd.merge(left,right,on='Name'), pitchdfs)
pitchsav.columns = ['Name', 'xwoba', 'xba', 'velo', 'angle']
pitchsav['velo'] = pitchsav['velo'].str.replace('MPH', '')
pitchsav['angle'] = pitchsav['angle'].str.replace('°', '')
pitchsav.to_csv('/home/Jon2Anderson/mlb/datarepo/master/pitchsavant18.csv')

print('pitchers, vs righties')
pitchvrxwobadf = savantScrape(pitchvrxwobaurl)
pitchvrxbadf = savantScrape(pitchvrxbaurl)
pitchvrvelodf = savantScrape(pitchvrvelourl)
pitchvrangledf = savantScrape(pitchvrangleurl)
pitchvrdfs = [pitchvrxwobadf, pitchvrxbadf, pitchvrvelodf, pitchvrangledf]
pitchvrsav = reduce(lambda left,right: pd.merge(left,right,on='Name'), pitchvrdfs)
pitchvrsav.columns = ['Name', 'xwoba', 'xba', 'velo', 'angle']
pitchvrsav['velo'] = pitchvrsav['velo'].str.replace('MPH', '')
pitchvrsav['angle'] = pitchvrsav['angle'].str.replace('°', '')
pitchvrsav.to_csv('/home/Jon2Anderson/mlb/datarepo/master/pitchvrsavant18.csv')

print('pitchers, vs lefties')
pitchvlxwobadf = savantScrape(pitchvlxwobaurl)
pitchvlxbadf = savantScrape(pitchvlxbaurl)
pitchvlvelodf = savantScrape(pitchvlvelourl)
pitchvlangledf = savantScrape(pitchvlangleurl)
pitchvldfs = [pitchvlxwobadf, pitchvlxbadf, pitchvlvelodf, pitchvlangledf]
pitchvlsav = reduce(lambda left,right: pd.merge(left,right,on='Name'), pitchvldfs)
pitchvlsav.columns = ['Name', 'xwoba', 'xba', 'velo', 'angle']
pitchvlsav['velo'] = pitchvlsav['velo'].str.replace('MPH', '')
pitchvlsav['angle'] = pitchvlsav['angle'].str.replace('°', '')
pitchvlsav.to_csv('/home/Jon2Anderson/mlb/datarepo/master/pitchvlsavant18.csv')

## Merge everything together
masterhitting = mergeHittingData(hitstan, hitsav)
masterhittingvr = mergeHittingData(hitvr, hitvrsav)
masterhittingvl = mergeHittingData(hitvl, hitvlsav)
masterpitching = mergePitchingData(pitchstan, pitchsav)
masterpitchingvr = mergePitchingData(pitchvr, pitchvrsav)
masterpitchingvl = mergePitchingData(pitchvl, pitchvlsav)

masterhitting.to_csv('hitmaster18.csv')
masterhittingvr.to_csv('hitvrmaster18.csv')
masterhittingvl.to_csv('hitvlmaster18.csv')
masterpitching.to_csv('pitchmaster18.csv')
masterpitchingvr.to_csv('pitchvrmaster18.csv')
masterpitchingvl.to_csv('pitchvlmaster18.csv')

# These functions are used to get overall stats in order to
# break down each team's lineup later on.
standf = getStan()
advdf = getAdv()
standfvr = getStanVR()
advdfvr = getAdvVR()
standfvl = getStanVL()
advdfvl = getAdvVL()

stats = pd.merge(standf, advdf, on="Name")
statsvr = pd.merge(standfvr, advdfvr, on="Name")
statsvl = pd.merge(standfvl, advdfvl, on="Name")

stats = stats.apply(lambda x: x.astype(str).str.lower())
statsvr = statsvr.apply(lambda x: x.astype(str).str.lower())
statsvl = statsvl.apply(lambda x: x.astype(str).str.lower())
stats.to_csv('lubreakdown_stats18.csv')
statsvr.to_csv('lubreakdown_statsvr18.csv')
statsvl.to_csv('lubreakdown_statsvl18.csv')