import requests
from data_sources.base import DataSource, DataSourceStatus
from datetime import datetime


class TheBlueAllianceConnector(DataSource):
    """Data source to handle pulling data from TheBlueAlliance.com"""

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
        self.__base_url = "https://www.thebluealliance.com/api/v3"
        self.__headers = {"X-TBA-Auth-Key": self.__api_token}

    def get_status(self) -> tuple[DataSourceStatus, dict]:
        url = f"{self.__base_url}/status"
        response = requests.get(url, headers=self.__headers)
        if response.status_code == 200:
            response_json = response.json()
            return (DataSourceStatus.CONNECTED, {"extra_info": response_json})
        if response.status_code == 401:
            return (DataSourceStatus.UNAUTHENTICATED, {})

    def get_team_info(self, team_number: int) -> dict | None:
        url = f"{self.__base_url}/team/frc{team_number}"
        response = requests.get(url, headers=self.__headers)
        if response.status_code == 200:
            return response.json()
        return None

    def get_event_matches(
        self, event_code: str, team_number: int | None = None
    ) -> dict | None:
        if team_number != None:
            url = f"{self.__base_url}/team/frc{team_number}/event/{event_code}/matches"
            response = requests.get(url, headers=self.__headers)
            if response.status_code == 200:
                return response.json()
        else:
            url = f"{self.__base_url}/event/{event_code}/matches"
            response = requests.get(url, headers=self.__headers)
            if response.status_code == 200:
                return response.json()
        return None

    def get_team_performance_metrics(self, team_number, event_code=None) -> dict | None:
        pass  # TODO: Decide what performance metrics I care about from TBA, how to calculate them, etc.
