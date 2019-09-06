import os, datetime, json
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

month = datetime.date.today().strftime("%B")
day = datetime.date.today().strftime("%d")
date = month + day

def sendFile(df):
    recipients = ['jon2anderson@gmail.com']
    emaillist = [elem.strip().split(',') for elem in recipients]
    msg = MIMEMultipart()
    msg['Subject'] ="Pitching Info"
    msg['From'] = 'Jon'
    msg['Reply-to'] = 'jon2anderson@gmail.com'

    msg.preamble = 'Multipart massage.\n'

    bodytext = MIMEText("Well, here you go.")
    msg.attach(bodytext)
    os.chdir('/home/Jon2Anderson/mlb/dailysheets/')
    part = MIMEApplication(open('%s_Top.csv' %date,'rb').read())
    part1 = MIMEApplication(open('%s_Cheap.csv' %date, 'rb').read())
    part2 = MIMEApplication(open('%s_ShortPitchersReport.csv' %date, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename='%s_Top.csv' %date)
    part1.add_header('Content-Disposition', 'attachment', filename='%s_Cheap.csv' %date)
    part2.add_header('Content-Disposition', 'attachment', filename='%s_ShortPitchersReport.csv' %date)
    msg.attach(part)
    msg.attach(part1)
    msg.attach(part2)

    server = smtplib.SMTP("smtp.gmail.com:587")
    server.ehlo()
    server.starttls()
    server.login("jonsbot0@gmail.com", "@llenb3rryDr!")

    server.sendmail(msg['From'], emaillist , msg.as_string())

def sendText(df):
    x=list(df['Name'])
    gmail_user = 'jonsbot0@gmail.com'
    gmail_password = '@llenb3rryDr!'

    sent_from = 'jonsbot0@gmail.com'
    #to = '7249806694@vtext.com'
    recip = ['7249806694@vtext.com']
    subject = 'Lineup'

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, recip, subject, x)

    #try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, recip, email_text)
    server.close()

os.chdir('/home/Jon2Anderson/mlb/dailysheets')
dkdata = pd.read_csv('/home/Jon2Anderson/mlb/dailysheets/%s_DKData.csv' %date)
dkdata=dkdata[['Name', 'pos', 'sal']]
pdkdata=dkdata[dkdata['pos']=='sp']
pdkdata=pdkdata.rename(index=str, columns={'Name': 'Pitcher', 'sal': 'psal', 'pos': 'ppos'})
hitdata = pd.read_csv('/home/Jon2Anderson/mlb/dailysheets/%s_HittersReport_Splits19.csv' %date)
pitdata = pd.read_csv('/home/Jon2Anderson/mlb/dailysheets/%s_PitchersReport_Splits19.csv' %date)
pitchingdf = pd.read_csv('/home/Jon2Anderson/mlb/dailysheets/%s_PitchersReport.csv' %date)
lubreak = pd.read_csv('/home/Jon2Anderson/mlb/dailysheets/%s_LineupBreakdown_Splits19.csv' %date)
pitchmerged = pd.merge(pitchingdf, lubreak, left_on="Opp", right_on="Team")
pitchmerged = pitchmerged.rename(index=str, columns={'Team_x': 'pTeam', 'K%_x': 'pK%', 'BB%_x': 'pBB%', 'AVG_x': 'pAVG', 'Team_y': 'luTeam', 'AVG_y': 'luAVG', 'K%_y': 'luK%', 'BB%_y': 'luBB%'})

hitdata = hitdata[['Name', 'Team', 'hand', 'LU Spot', 'Pitcher', 'R/L', 'PA', 'wOBA', 'xwoba', 'wRC+',
                    'AVG', 'xba', 'OBP', 'K%', 'BB%', 'GB%', 'FB%', 'BABIP', 'velo', 'angle']]

pitdata = pitdata[['Name', 'Tm', 'R/L', 'Opp', 'Split', 'IP', 'xwoba', 'xba', 'K%', 'BB%',
                    'ERA' ,'xFIP' , 'WHIP', 'GB%', 'FB%', 'HR/9']]

pitdata = pitdata.rename(index=str, columns={'Name': 'Pitcher', 'Split': 'hand'})
pitdata['hand'] = pitdata['hand'].str.replace('vs all', 'all')
pitdata['hand'] = pitdata['hand'].str.replace('vs R', 'r')
pitdata['hand'] = pitdata['hand'].str.replace('vs L', 'l')

master = pd.merge(hitdata, pitdata, how='left', on='Pitcher')

for i in range(len(master['Name'])):
    if str(master.iloc[i,2]) == 'nan':
        master.iloc[i,2] = 'r'
    if str(master.iloc[i,2]) == 's':
        if str(master.iloc[i,5]) == 'l':
            master.iloc[i,2] = 'r'
        else:
            master.iloc[i,2] = 'l'

master = pd.merge(master, dkdata, on='Name')
master = pd.merge(master, pdkdata, on='Pitcher')
master = master[master['hand_x'] == master['hand_y']]
master['|'] = '|'
master = master[['Name', 'sal', 'pos', 'Team', 'Tm', 'hand_x', 'LU Spot', 'R/L_x', 'PA', 'wOBA', 'xwoba_x',
                'xba_x', 'K%_x', 'BB%_x', 'GB%_x', 'FB%_x', '|', 'Pitcher', 'psal', 'hand_y', 'IP',
                'xwoba_y', 'xba_y', 'K%_y', 'BB%_y', 'xFIP', 'WHIP', 'GB%_y', 'FB%_y', 'HR/9']]

master = master.rename(index=str, columns={'Tm': 'Opp', 'hand_x': 'bHand', 'LU Spot': 'Slot',
                        'R/L_x': 'pHand', 'xba_x': 'bXBA', 'K%_x': 'bK%', 'BB%_x': 'bBB%',
                        'GB%_x': 'bGB%', 'FB%_x': 'bFB%', 'hand_y': 'pHand', 'xwoba_y': 'pXWOBA',
                        'xba_y': 'pXBA', 'K%_y': 'pK%', 'BB%_y': 'pBB%', 'GB%_y': 'pGB%',
                        'FB%_y': 'pFB%', 'xwoba_x': 'bXWOBA'})
master.to_csv('%s_Master.csv' %date)

matchups = master
matchups['bK%'] = matchups['bK%'].str.replace(' %', '')
matchups['pK%'] = matchups['pK%'].str.replace(' %', '')
matchups['bBB%'] = matchups['bBB%'].str.replace(' %', '')
matchups['pBB%'] = matchups['pBB%'].str.replace(' %', '')
matchups['bGB%'] = matchups['bGB%'].str.replace(' %', '')
matchups['pGB%'] = matchups['pGB%'].str.replace(' %', '')
matchups['bFB%'] = matchups['bFB%'].str.replace(' %', '')
matchups['pFB%'] = matchups['pFB%'].str.replace(' %', '')

matchups['bK%'] = pd.to_numeric(matchups['bK%'])
matchups['pK%'] = pd.to_numeric(matchups['pK%'])
matchups['bBB%'] = pd.to_numeric(matchups['bBB%'])
matchups['pBB%'] = pd.to_numeric(matchups['pBB%'])
matchups['bGB%'] = pd.to_numeric(matchups['bGB%'])
matchups['pGB%'] = pd.to_numeric(matchups['pGB%'])
matchups['bFB%'] = pd.to_numeric(matchups['bFB%'])
matchups['pFB%'] = pd.to_numeric(matchups['pFB%'])

matchups['vxwoba'] = matchups['bXWOBA'] + matchups['pXWOBA']
matchups['vxba'] = matchups['bXBA'] + matchups['pXBA']
matchups['vK%'] = matchups['bK%'] + matchups['pK%']
matchups['vBB%'] = matchups['bBB%'] + matchups['pBB%']
matchups['vGB%'] = matchups['bGB%'] + matchups['pGB%']
matchups['vFB%'] = matchups['bFB%'] + matchups['pFB%']
matchups = matchups[['Name', 'Team', 'pos', 'sal','Pitcher', 'psal', 'PA', 'IP', 'vxwoba', 'vxba', 'vK%',
                        'vBB%', 'vGB%', 'vFB%']]
#print(matchups.head(5))
matchups.to_csv('%s_Matchups.csv' %date)
matchups['vK%'] = round(matchups['vK%'],1)
matchups['vxwoba'] = round(matchups['vxwoba'], 3)
matchups['vxba'] = round(matchups['vxba'], 3)
matchups=matchups.sort_values(by='vxwoba', ascending=False)
cheap = matchups[matchups['sal']<4000]
cheap = cheap.head(20)
cheap = cheap[['Name', 'pos', 'sal', 'Pitcher', 'vxwoba', 'vxba', 'vK%']]
cheap.to_csv('%s_Cheap.csv' %date)
top = matchups.head(30)
top = top[['Name', 'pos', 'sal', 'Pitcher', 'vxwoba', 'vxba', 'vK%']]
top.to_csv('%s_Top.csv' %date)
pitchmerged = pitchmerged[['Name', 'sal', 'R/L', 'pTeam', 'IP', 'pK%', 'pBB%',
       'BABIP', 'xFIP', 'WHIP', 'xwoba', 'pAVG', 'xba', 'FB%', 'GB%',
       'LD%', 'HR/9', 'Soft%', 'Hard%', 'HR/FB', 'K-BB%', 'LOB%', 'angle',
       'velo', 'luTeam', 'luAVG','SLG', 'wOBA', 'wRC+', 'luK%', 'luBB%', 'HR%']]
pitchmerged.to_csv('%s_PitchingMaster.csv' %date)
#sendFile(top)

os.chdir('/home/Jon2Anderson/mlb/dailysheets/')
keeplist = ['%s_Top.csv' %date, '%s_Cheap.csv' %date, '%s_DKData.csv' %date, '%s_FDData.csv' %date,
            '%s_HittersReport_Splits19.csv' %date, '%s_LineupBreakdown_Splits19.csv' %date,
            '%s_Master.csv'  %date, '%s_Matchups.csv' %date, '%s_PitchersReport.csv' %date,
            '%s_PitchersReport_Splits19.csv' %date, '%s_PitchingMaster.csv' %date,
            '%s_ShortPitchersReport.csv' %date]
files = os.listdir()
for f in files:
    if f not in keeplist:
        os.remove(f)

print('done')