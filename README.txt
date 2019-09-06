Daily MLB Data Collection Scripts

I am an avid fantasy baseball player, and you really can't play that game responsibly without relying heavily on data. There is so much raw data out there for baseball, but it's just all over the place and not really quickly accessible. Because of this, I wanted to have a way to go out and create a report on every pitcher and hitter playing each day without too much effort. That's what these scripts do. This document gives you a high level view of what each script does.

After we run all of these scripts, we are left with 2 CSV files that we then run a pre-recorded macro on to format everything nicely. It gives us data for each hitter and pitcher playing that day, as well as data about their opponent. Examples of those two files are present in this repo.

getMLBData.py:
This script goes out and collects the up-to-date data for every hitter and pitcher in the league. It uses Fangraphs.com and baseballsavant.mlb.com to retrieve the numbers for every statistic I want. It collects a couple dozen statistics for every hitter and pitcher, as well as getting the "split" statistics for each stat as well (this means that for each hitter, you will see their stats against all pitchers, against left handed pitchers, and against right handed pitchers - and the same is true for pitchers vs. hitters). The script scrapes those websites and saves all the data into CSV files.

getDailyData.py:
This script scrapes a few different websites to get each day's team lineups, opponents, probable pitchers, active rosters, and daily fantasy sports information like each player's salary (from sites like Draftkings and Fanduel).

dailyHitterReport.py:
This script loads in all the hitting and pitching data, and then loops through every team that is playing that day to get the data we need for each player. If there is no official lineup out yet, it will use a projected lineup. It looks up the handedness of the pitcher the team is facing that day, and gets each player's statistics against that type of pitcher and puts them all together in a CSV file.

dailyPitcherReport.py:
This script loops through every probable pitcher for the given day and collects all of their up-to-date statistics and puts them in a CSV file.

dailyPitcherReportSplits.py:
This does the same as the dailyPitchersReport script but runs through each pitcher twice to get their stats against both righties and lefties. 

dailyLineupBreakdown.py:
This script takes each team's lineup, gets all the stats for every individual player, and then does the math to get the numbers for the lineup as a whole. There is a problem with just averaging the batting average of every player in a lineup, since a player with more at-bats should have a much heavier weight on the total lineup batting average than someone with just a handful of at-bats. This script adds all the raw numbers up together first, and then calculates the statistics we want, which gives us a good picture of how strong the lineup is. It creates a CSV with a table a row for every team playing that day.

createMaster.py:
This script puts everything we have together into two files, one for that day's pitchers, and one for that day's hitters. It loops through every lineup and gets each hitter's up-to-date statistics against the handedness of the pitcher they are facing that day, and puts that pitcher's statistics against their own handedness in the same row. It prints all the data into a CSV file. It does the same for pitchers, putting all their relevant stats into a CSV file along with their opposing lineup's statistics that were created in the dailyLineupBreakdown file.