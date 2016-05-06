import requests
import sys

def requestSummonerData(region, summonerName, APIKey):
    URL = "https://" + region + ".api.pvp.net/api/lol/na/v1.4/summoner/by-name/" + summonerName + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json() if response.status_code == requests.codes.ok else None

def requestRankedData(region, ID, APIKey):
    URL = "https://" + region + ".api.pvp.net/api/lol/na/v2.5/league/by-summoner/" + ID + "/entry?api_key=" + APIKey
    response = requests.get(URL)
    return response.json() if response.status_code == requests.codes.ok else None

def requestRecentMatches(region, ID, APIKey):
    URL = "https://" + region + ".api.pvp.net/api/lol/na/v1.3/game/by-summoner/" + ID + "/recent?api_key=" + APIKey
    response = requests.get(URL)
    return response.json() if response.status_code == requests.codes.ok else None

def requestChampionData(region, champID, APIKey):
    URL = "https://global.api.pvp.net/api/lol/static-data/" + region + "/v1.2/champion/" + champID + "?api_key=" + APIKey
    return requests.get(URL).json()

def main():
    print "Type in one of the following regions:\n"
    print "NA EUW EUNE LAN BR KR LAS OCE TR RU PBE\n"

    regionList = ["na","euw","eune", "lan", "br", "kr", "las", "oce", "tr", "ru" , "pbe"]

    region = (str)(raw_input('Type in one of the regions above: ')).lower()

    if region in regionList:
        summonerName = (str)(raw_input('Type your Summoner Name here and DO NOT INCLUDE ANY SPACES: '))
    else:
        print "Invalid Region. Please Try again."
        print "----------------------------------------------------------\n\n"
        while True:
            execfile("APIGrabber.py")

    APIKey = (str) ('7ac4f906-c21a-476f-a50a-b0862026dcb8')

    summonerDataJSON  = requestSummonerData(region, summonerName, APIKey)

    if summonerDataJSON is None:
        print 'This summoner does not Exist'
        sys.exit()
    else:
        ID = (str) (summonerDataJSON[summonerName]['id'])
        Name = (str)(summonerDataJSON[summonerName]['name'])
        rankedDataJSON = requestRankedData(region, ID, APIKey)
        recentMatchJSON = requestRecentMatches(region, ID, APIKey)
        print '\nName: ' + Name


    if rankedDataJSON is None:
        print 'The Summoner is not ranked'
    else:
        LP = (str) (rankedDataJSON[ID][0]['entries'][0]['leaguePoints'])
        Tier = (str) (rankedDataJSON[ID][0]['tier'])
        Division = (str) (rankedDataJSON[ID][0]['entries'][0]['division'])
        print 'Tier: ' + Tier + " " + Division + " @ " + LP + " LP"

        print '\nMost Recent Game Stats'
        print '-------------------------------------------------------------'

    for i in range(0, 5):
        DamageToChamps = (str) (recentMatchJSON['games'][i]['stats']['totalDamageDealtToChampions'])
        GameResult = 'Win' if (recentMatchJSON['games'][i]['stats']['win']) else 'Loss'
        kills = (str) (recentMatchJSON['games'][i]['stats']['championsKilled']) if ('championsKilled' in recentMatchJSON['games'][i]['stats']) else (str(0))
        deaths = (str) (recentMatchJSON['games'][i]['stats']['numDeaths']) if 'numDeaths' in recentMatchJSON['games'][i]['stats'] else (str(0))
        assists = (str) (recentMatchJSON['games'][i]['stats']['assists']) if 'assists' in recentMatchJSON['games'][i]['stats'] else (str(0))

        Ratio = str(round((int(assists) + int(kills)) / int(deaths), 2)) if deaths > 0 else 'Perfect'
        championNameJSON = requestChampionData(region, (str)(recentMatchJSON['games'][i]['championId']), APIKey)
        m, s = divmod((recentMatchJSON['games'][i]['stats']['timePlayed']), 60)
        h, m = divmod(m, 60)

        print 'Game Result: ' + GameResult
        print 'Champion Played: ' + championNameJSON['name']
        print 'KDA: ' + kills + "-" + deaths + "-" + assists + " ; Ratio: " + Ratio
        print 'Creep Score: ' + (str)(recentMatchJSON['games'][i]['stats']['minionsKilled'])
        print 'Game Time: ' + "%d:%02d:%02d" % (h, m, s) + "\n\n"


if __name__ == "__main__":
    main()
