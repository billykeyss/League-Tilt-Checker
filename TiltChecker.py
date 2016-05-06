import requests
import sys

def requestSummonerData(region, summonerName, APIKey):
    URL = "https://" + region + ".api.pvp.net/api/lol/na/v1.4/summoner/by-name/" + summonerName + "?api_key=" + APIKey
    response = requests.get(URL)
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        return None

def requestCurrentMatch(region, ID, APIKey):
    URL = "https://" + region + ".api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/NA1/" + ID + "?api_key=" + APIKey
    response = requests.get(URL)
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        return None

def requestRecentMatches(region, ID, APIKey):
    URL = "https://" + region + ".api.pvp.net/api/lol/na/v1.3/game/by-summoner/" + ID + "/recent?api_key=" + APIKey
    response = requests.get(URL)
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        return None

def requestChampionData(region, champID, APIKey):
    URL = "https://global.api.pvp.net/api/lol/static-data/" + region + "/v1.2/champion/" + champID + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def main():
    print "Type in one of the following regions:\n"
    print "NA EUW EUNE LAN BR KR LAS OCE TR RU PBE\n"

    regionList = ["na","euw","eune", "lan", "br", "kr", "las", "oce", "tr", "ru" , "pbe"]

    region = (str)(raw_input('Type in one of the regions above: '))
    region = region.lower()

    if region in regionList:
        summonerName = (str)(raw_input('Type your Summoner Name here and DO NOT INCLUDE ANY SPACES: '))
    else:
        print "Invalid Region. Please Try again."
        print "----------------------------------------------------------\n\n"
        while True:
            execfile("APIGrabber.py")

    APIKey = (str) ('7ac4f906-c21a-476f-a50a-b0862026dcb8')
    global summonerDataJSON
    summonerDataJSON = requestSummonerData(region, summonerName, APIKey)

    if summonerDataJSON is None:
        print 'This summoner does not Exist'
        sys.exit()
        execfile("TiltChecker.py")
    else:
        ID = (str) (summonerDataJSON[summonerName]['id'])
        currentMatchJSON = requestCurrentMatch(region, ID, APIKey)
        if currentMatchJSON is None:
            print 'This summoner is not in game'
            print "----------------------------------------------------------\n\n"
            while True:
                execfile("TiltChecker.py")
        else:
            print '\nMost Recent Game Stats'
            print '-------------------------------------------------------------'

    for i in range(0,10):
        if i is 5:
            print "\n----------------------------------------------------------\n----------------------------------------------------------\n"
        print currentMatchJSON['participants'][i]["summonerName"]
        opponentID = (str)(currentMatchJSON['participants'][i]["summonerId"])

        recentMatchJSON = requestRecentMatches(region, opponentID, APIKey)

        for j in range(0, 5):

            GameResult = (recentMatchJSON['games'][j]['stats']['win'])

            if GameResult:
                GameResult = 'W'
            else:
                GameResult = 'L'
            championDataJSON = requestChampionData(region, (str)(recentMatchJSON['games'][j]['championId']), APIKey)
            m, s = divmod((recentMatchJSON['games'][j]['stats']['timePlayed']), 60)
            h, m = divmod(m, 60)

            kills = (str) (recentMatchJSON['games'][j]['stats']['championsKilled']) if ('championsKilled' in recentMatchJSON['games'][j]['stats']) else (str(0))
            deaths = (str) (recentMatchJSON['games'][j]['stats']['numDeaths']) if 'numDeaths' in recentMatchJSON['games'][j]['stats'] else (str(0))
            assists = (str) (recentMatchJSON['games'][j]['stats']['assists']) if 'assists' in recentMatchJSON['games'][j]['stats'] else (str(0))

            KDA = kills + "-" + deaths + "-" + assists

            print 'Game ' + str(j+1) + ": " + GameResult + '   Game Time: ' + "%d:%02d:%02d" % (h, m, s) + '   Champ: ' + championDataJSON['name'] + '   KDA: ' + KDA


        print "----------------------------------------------------------\n\n"


if __name__ == "__main__":
    main()
