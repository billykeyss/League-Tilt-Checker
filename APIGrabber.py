import requests
import sys

def requestSummonerData(region, summonerName, APIKey):
    URL = "https://" + region + ".api.pvp.net/api/lol/na/v1.4/summoner/by-name/" + summonerName + "?api_key=" + APIKey
    response = requests.get(URL)
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        return None

def requestRankedData(region, ID, APIKey):
    URL = "https://" + region + ".api.pvp.net/api/lol/na/v2.5/league/by-summoner/" + ID + "/entry?api_key=" + APIKey
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

    responseJSON  = requestSummonerData(region, summonerName, APIKey)
    
    if responseJSON is None:
        print 'This summoner does not Exist'
        sys.exit()
    else:
        ID = (str) (responseJSON[summonerName]['id'])
        Name = (str)(responseJSON[summonerName]['name'])
        responseJSON2 = requestRankedData(region, ID, APIKey)
        responseJSON3 = requestRecentMatches(region, ID, APIKey)
        print '\nName: ' + Name


    if responseJSON2 is None:
        print 'The Summoner is not ranked'
    else:
        LP = (str) (responseJSON2[ID][0]['entries'][0]['leaguePoints'])
        Tier = (str) (responseJSON2[ID][0]['tier'])
        Division = (str) (responseJSON2[ID][0]['entries'][0]['division'])
        print 'Tier: ' + Tier + " " + Division + " @ " + LP + " LP"

        print '\nMost Recent Game Stats'
        print '-------------------------------------------------------------'

    for i in range(0, 5):
        DamageToChamps = (str) (responseJSON3['games'][i]['stats']['totalDamageDealtToChampions'])
        GameResult = (responseJSON3['games'][i]['stats']['win'])
        
        if GameResult:
            GameResult = 'Win'
        else:
            GameResult = 'Loss'
            
        KDA = (str) (responseJSON3['games'][i]['stats']['championsKilled']) + "-" + (str) (responseJSON3['games'][i]['stats']['numDeaths']) + "-" + (str) (responseJSON3['games'][i]['stats']['assists'])
        Ratio = (responseJSON3['games'][i]['stats']['assists'] + responseJSON3['games'][i]['stats']['championsKilled']) / (responseJSON3['games'][i]['stats']['numDeaths'])
        Ratio = str(round(Ratio, 2))
        responseJSON4 = requestChampionData(region, (str)(responseJSON3['games'][i]['championId']), APIKey)
        m, s = divmod((responseJSON3['games'][i]['stats']['timePlayed']), 60)
        h, m = divmod(m, 60)
        
        print 'Game Result: ' + GameResult
        print 'Champion Played: ' + responseJSON4['name']
        print 'KDA: ' + KDA + " ; Ratio: " + Ratio
        print 'Creep Score: ' + (str)(responseJSON3['games'][i]['stats']['minionsKilled'])
        print 'Game Time: ' + "%d:%02d:%02d" % (h, m, s) + "\n\n"


if __name__ == "__main__":
    main()

