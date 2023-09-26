from requests import Response
import requests


class mentimeter:
    def __init__(self, menti_id: str):
        self.host: str = "https://www.menti.com/"
        self.menti_id = menti_id

        self.headers: dict = {
            "Referer": f"{self.host}/{menti_id}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
            "Alt-Used": "www.menti.com"
        }

    def getCookies(self):
        r: Response = requests.get(
            f"{self.host}{self.menti_id}", headers=self.headers)

        self.cookies = r.cookies

    def getIdentifier(self):
        self.getCookies()

        r: Response = requests.post(
            f"{self.host}/core/identifiers", headers=self.headers, cookies=self.cookies)
        if r.status_code == 200:
            data: dict = r.json()
            identifier_key: str = "identifier"
            if identifier_key in data:
                self.headers["X-Identifier"] = data.get(identifier_key, "")

    def getVoteId(self):
        self.getIdentifier()

        r: Response = requests.get(
            f"{self.host}/core/vote-keys/{self.menti_id}/series", headers=self.headers, cookies=self.cookies)
        if r.status_code == 200:
            data: dict = r.json()
            pace_key: str = "pace"
            if pace_key in data:
                pace: dict = data["pace"]
                vote_id_key: str = "active"
                if vote_id_key in pace:
                    self.vote_id = pace.get(vote_id_key, "")

    def vote(self, word: str):
        self.getVoteId()

        body: dict = {"vote": word, "type": "wordcloud"}

        r: Response = requests.post(
            f"{self.host}/core/votes/{self.vote_id}", data=body, headers=self.headers, cookies=self.cookies)

        if r.status_code != 200:
            print(r.content)
            raise EisException(
                f"Dein Eiswunsch konnte nicht erfüllt werden: {r.status_code}")


class EisException(Exception):
    pass
