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
    global responseJSON
    responseJSON = requestSummonerData(region, summonerName, APIKey)
    
    if responseJSON is None:
        print 'This summoner does not Exist'
        sys.exit()
        execfile("TiltChecker.py")
    else:
        ID = (str) (responseJSON[summonerName]['id'])
        responseJSON2 = requestCurrentMatch(region, ID, APIKey)
        if responseJSON2 is None:
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
        print responseJSON2['participants'][i]["summonerName"]
        opponentID = (str)(responseJSON2['participants'][i]["summonerId"])

        responseJSON3 = requestRecentMatches(region, opponentID, APIKey)
        
        for j in range(0, 5):
            
            GameResult = (responseJSON3['games'][j]['stats']['win'])
        
            if GameResult:
                GameResult = 'W'
            else:
                GameResult = 'L'
            responseJSON4 = requestChampionData(region, (str)(responseJSON3['games'][j]['championId']), APIKey)
            m, s = divmod((responseJSON3['games'][j]['stats']['timePlayed']), 60)
            h, m = divmod(m, 60)

            if 'championsKilled' in responseJSON3['games'][j]['stats']:
                kills = (str) (responseJSON3['games'][j]['stats']['championsKilled'])
            else:
                kills = (str(0));

            if 'numDeaths' in responseJSON3['games'][j]['stats']:
                deaths = (str) (responseJSON3['games'][j]['stats']['numDeaths'])
            else:
                deaths = (str(0));

            if 'assists' in responseJSON3['games'][j]['stats']:
                assists = (str) (responseJSON3['games'][j]['stats']['assists'])
            else:
                assists = (str(0));

            KDA = kills + "-" + deaths + "-" + assists
        
            print 'Game ' + str(j+1) + ": " + GameResult + '   Game Time: ' + "%d:%02d:%02d" % (h, m, s) + '   Champ: ' + responseJSON4['name'] + '   KDA: ' + KDA


        print "----------------------------------------------------------\n\n"


if __name__ == "__main__":
    main()

