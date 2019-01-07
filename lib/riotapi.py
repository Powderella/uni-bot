import requests
from pprint import pformat

params = {"api_key": "RGAPI-f99ed19f-f92c-4df7-ba62-fc187c7d8063"}


class RiotAPI:
    def __init__(self, region="jp1"):
        self.baseurl = "https://{0}.api.riotgames.com/lol/".format(region)

    def _get_summoner_info(self, summoner_name):
        """
        サモナーの情報を返す
        """
        url = self.baseurl + "summoner/v4/summoners/by-name/{name}"
        formatted_url = url.format(name=summoner_name)
        with requests.get(formatted_url, params) as res:
            res.raise_for_status()
            return res.json()
            

    def _get_summoner_rank_info(self, summoner_id):
        """
        ランク戦の情報を返す
        """
        url = self.baseurl + "league/v4/positions/by-summoner/{id}"

        formatted_url = url.format(id=summoner_id)

        with requests.get(formatted_url, params) as res:
            res.raise_for_status()
            return res.json()[0] # RANKED_SOLO_5x5のみ返す
    
    def _get_player_icon_url(self, icon_id):
        """
        icon_idをもらってURLを返すだけ
        """
        url = "https://ddragon.leagueoflegends.com/cdn/8.24.1/" \
            + "img/profileicon/{0}.png".format(icon_id)
        
        return url
    
    def get_summoner(self, summoner_name):
        summonerinfo = self._get_summoner_info(summoner_name)
        rankinfo = self._get_summoner_rank_info(summonerinfo["id"])

        summonerinfo.update(rankinfo)
        summonerinfo["icon_url"] = self._get_player_icon_url(
                                    summonerinfo["profileIconId"])
        return summonerinfo

    def _get_spectate(self, summoner_name):
        """
        return yield
        """
        url = self.baseurl + "spectator/v4/active-games/by-summoner/{id}"

        summoner = self._get_summoner_info(summoner_name)

        formatted_url = url.format(id=summoner["id"])

        with requests.get(formatted_url, params) as res:
            res.raise_for_status()
            return res.json()

    def _get_spectate_summoner_info(self, summoner_name):
        contents = self._get_spectate(summoner_name)
        for content in contents["participants"]:
            summoner_name = content["summonerName"]
            team_id = content["teamId"]
            rank = self._get_summoner_rank_info(content["summonerId"])
            yield summoner_name, team_id, rank["tier"], rank["rank"], rank["leaguePoints"]

if __name__ == "__main__":
    r = RiotAPI()
    for s in r._get_spectate_summoner_info("とうやまなお"):
        print(s)