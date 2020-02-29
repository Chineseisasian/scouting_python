import mysql.connector as mariaDB

# Connection to AWS database with proper data
conn = mariaDB.connect(user='admin',
                       passwd='Einstein195',
                       host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                       database='team195_scouting')
cursor = conn.cursor()


cursor.execute("SELECT Matches.* FROM Matches LEFT JOIN MatchScouting  "
               "ON (Matches.EventID = MatchScouting.EventID) "
               "AND Matches.MatchID = MatchScouting.MatchID "
               "WHERE (((Matches.EventID) = 1) AND ((MatchScouting.MatchID) is Null));")
rsMatches = cursor.fetchall()
# print(rsMatches)

# Find matches from the Matches table and add new records to the MatchScouting table if they do not already exist
for row in rsMatches:
    i = 1
    while i <= 6:
        rsMatchScoutingRecord = {'MatchID': row[0], 'EventID': row[1], 'Team': row[i + 2], 'AllianceStationID': i}
        # print(rsMatchScoutingRecord)
        items = rsMatchScoutingRecord.items()
        columns = str(tuple([x[0] for x in items])).replace("'", "")
        values = str(tuple([x[1] for x in items]))
        cursor.execute("INSERT INTO MatchScouting "
                       + columns + " VALUES "
                       + values + ";")
        conn.commit()
        i += 1


# Fix Team #s for the six alliance stations. This is good in case a team number changed or was entered incorrectly
updateQuery = "UPDATE MatchScouting INNER JOIN Matches ON (MatchScouting.MatchID = Matches.MatchID) " \
              "INNER JOIN Events ON (Events.EventID = Matches.EventID) " \
              "SET MatchScouting.Team = Matches.RedTeam1 " \
              "WHERE Events.CurrentEvent = 1 AND MatchScouting.AllianceStationID = 1"
cursor.execute(updateQuery)
conn.commit()

updateQuery = "UPDATE MatchScouting INNER JOIN Matches ON (MatchScouting.MatchID = Matches.MatchID) " \
              "INNER JOIN Events ON (Events.EventID = Matches.EventID) " \
              "SET MatchScouting.Team = Matches.RedTeam2 " \
              "WHERE Events.CurrentEvent = 1 AND MatchScouting.AllianceStationID = 2"
cursor.execute(updateQuery)
conn.commit()

updateQuery = "UPDATE MatchScouting INNER JOIN Matches ON (MatchScouting.MatchID = Matches.MatchID) " \
              "INNER JOIN Events ON (Events.EventID = Matches.EventID) " \
              "SET MatchScouting.Team = Matches.RedTeam3 " \
              "WHERE Events.CurrentEvent = 1 AND MatchScouting.AllianceStationID = 3"
cursor.execute(updateQuery)
conn.commit()

updateQuery = "UPDATE MatchScouting INNER JOIN Matches ON (MatchScouting.MatchID = Matches.MatchID) " \
              "INNER JOIN Events ON (Events.EventID = Matches.EventID) " \
              "SET MatchScouting.Team = Matches.BlueTeam1 " \
              "WHERE Events.CurrentEvent = 1 AND MatchScouting.AllianceStationID = 4"
cursor.execute(updateQuery)
conn.commit()

updateQuery = "UPDATE MatchScouting INNER JOIN Matches ON (MatchScouting.MatchID = Matches.MatchID) " \
              "INNER JOIN Events ON (Events.EventID = Matches.EventID) " \
              "SET MatchScouting.Team = Matches.BlueTeam2 " \
              "WHERE Events.CurrentEvent = 1 AND MatchScouting.AllianceStationID = 5"
cursor.execute(updateQuery)
conn.commit()

updateQuery = "UPDATE MatchScouting INNER JOIN Matches ON (MatchScouting.MatchID = Matches.MatchID) " \
              "INNER JOIN Events ON (Events.EventID = Matches.EventID) " \
              "SET MatchScouting.Team = Matches.BlueTeam3 " \
              "WHERE Events.CurrentEvent = 1 AND MatchScouting.AllianceStationID = 6"
cursor.execute(updateQuery)
conn.commit()


# add team match numbers by looping back through each teams matches and counting
cursor.execute("SELECT DISTINCT MatchScouting.Team "
               "FROM MatchScouting INNER JOIN Events ON MatchScouting.EventID = Events.EventID "
               "AND ((Events.CurrentEvent) = 1) "
               "ORDER BY MatchScouting.Team; ")
rsTeams = cursor.fetchall()
# print(rsTeams)

for team in rsTeams:
    # print(team[0])
    cursor.execute("SELECT MatchScouting.MatchScoutingID FROM MatchScouting INNER JOIN Events "
                   "ON MatchScouting.EventID = Events.EventID AND ((Events.CurrentEvent) = 1) "
                   "WHERE MatchScouting.Team = "
                   + team[0] + " ORDER BY MatchScouting.MatchScoutingID; ")
    rsTeamMatchScouting = cursor.fetchall()
    # print(rsTeamMatchScouting)
    matchNum = 0
    for match in rsTeamMatchScouting:
        matchNum += 1
        # print(match[0])
        query = "UPDATE MatchScouting SET MatchScouting.TeamMatchNo = " + str(matchNum) + " WHERE MatchScouting.MatchScoutingID = " + str(match[0]) + ";"
        # print(query)
        cursor.execute(query)
        conn.commit()