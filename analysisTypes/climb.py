import statistics

def climb(analysis, rsRobotMatches):
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 7
    numberOfMatchesPlayed = 0
    totalClimbPointsList = []

    for matchResults in rsRobotMatches:
        rsCEA['Team'] = matchResults[analysis.columns.index('Team')]
        rsCEA['EventID'] = matchResults[analysis.columns.index('EventID')]
        autoDidNotShow = matchResults[analysis.columns.index('AutoDidNotShow')]
        scoutingStatus = matchResults[analysis.columns.index('ScoutingStatus')]
        # Skip if DNS or UR
        if autoDidNotShow == 1:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = ''
        elif scoutingStatus == 2:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = ''
        else:
            ClimbMoveOnBar = matchResults[analysis.columns.index('ClimbMoveOnBar')]
            if ClimbMoveOnBar == 1:
                ClimbMoveOnBarString = "*"
            else:
                ClimbMoveOnBarString = ""

            # Status values: 1=no attempt, 2=success, 3=fail, 4=busy, 5=parked
            ClimbStatus = matchResults[analysis.columns.index('ClimbStatus')]
            if (ClimbStatus is None) or (ClimbStatus == 3 or 4 or 5):
                ClimbPoints = 0
            elif ClimbStatus == 2:
                ClimbPoints = 25
            else:
                ClimbPoints = 999

            ClimbLevelStatus = matchResults[analysis.columns.index('ClimbLevelStatus')]
            if ClimbLevelStatus == 1 and ClimbStatus == 2:
                ClimbLevelPoints = 15
            else:
                ClimbLevelPoints = 0

            RobotWeight = matchResults[analysis.columns.index('RobotWeight')]
            if RobotWeight is None:
                RobotWeight = 999

            # Perform some calculations
            numberOfMatchesPlayed += 1
            totalClimbPoints = ClimbPoints + ClimbLevelPoints
            totalClimbPointsList.append(totalClimbPoints)

            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = \
                str(totalClimbPoints) + str(ClimbMoveOnBarString)
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = totalClimbPoints
            if totalClimbPoints == 40 and ClimbMoveOnBar == 1:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 5
            elif totalClimbPoints == 40 and ClimbMoveOnBar != 1:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 4
            elif totalClimbPoints == 25:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 3
            elif totalClimbPoints == 5:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 2
            else:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 1

    if numberOfMatchesPlayed > 0:
        rsCEA['Summary1Display'] = round(statistics.mean(totalClimbPointsList), 1)
        rsCEA['Summary1Value'] = round(statistics.mean(totalClimbPointsList), 1)
        rsCEA['Summary2Display'] = statistics.median(totalClimbPointsList)
        rsCEA['Summary2Value'] = statistics.median(totalClimbPointsList)
        # 3 is rank
        rsCEA['Summary4Display'] = RobotWeight
        rsCEA['Summary4Value'] = RobotWeight

    return rsCEA