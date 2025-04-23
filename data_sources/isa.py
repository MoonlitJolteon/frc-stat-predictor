import requests
from data_sources.base import DataSource, DataSourceStatus
from datetime import datetime


class IndianaScoutingAllianceConnector(DataSource):
    def __init__(self, api_token: str, year=datetime.now().year):
        """
        Initializes the class instance with an API token and a specific year.

        Args
        -----
        api_token : str
            The authentication token required for API access.
        year : int, optional
            The year for which data will be retrieved. Defaults to the current year.
        """
        self.__api_token = api_token
        self.__observed_year = year
        self.__base_url = (
            "https://isa2025-api.liujip2020.workers.dev/public/REPLACEME/json?"
        )
        self.__headers = {"Authorization": f"Bearer {self.__api_token}"}

    def __build_ISA_robot_url(
        self, include_flags: str, teams: list = [], event_key: str = ""
    ):
        url = f"{self.__base_url}&include={include_flags}"
        if not teams == None:
            url += f"&team={','.join(teams)}"
        if not event_key == None:
            url += f"&event={event_key}"
        url = url.replace("REPLACEME", "robots")
        return url

    def __build_ISA_human_url(
        self, include_flags: str, teams: list = [], event_key: str = ""
    ):
        url = f"{self.__base_url}&include={include_flags}"
        if len(teams):
            url += f"&team={','.join(teams)}"
        if len(event_key):
            url += f"&event={event_key}"
        url = url.replace("REPLACEME", "humans")
        return url

    def get_status(self):
        url = self.__build_ISA_human_url("100000000000000")
        response = requests.get(url, headers=self.__headers)
        if response.status_code == 200:
            return (DataSourceStatus.CONNECTED, {"extra_info": {}})
        if response.status_code == 401:
            return (DataSourceStatus.UNAUTHENTICATED, {})

    def get_event_matches(self, event_code, team_number=None):
        human_url = self.__build_ISA_robot_url(
            "111110000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
            [str(team_number)] if not team_number == None else None,
            event_code,
        )
        response = requests.get(human_url, headers=self.__headers)
        if response.status_code == 200:
            return response.json()

    def get_robot_notes(self, team_number, event_code=None):
        notes_url = self.__build_ISA_robot_url(
            "0011000000000000000000000000010000000000000000000000000000000000000000000000000000000000000",
            [str(team_number)],
            event_code,
        )
        response = requests.get(notes_url, headers=self.__headers)
        if response.status_code == 200:
            return response.json()

    def get_team_info(self, team_number):
        pass

    def get_team_performance_metrics(self, team_number, event_code=None):
        pass
