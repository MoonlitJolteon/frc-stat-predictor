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
        self._headers = {"X-TBA-Auth-Key": self.__api_token}

    def get_status(self) -> tuple[DataSourceStatus, dict]:
        pass

    def get_team_data(self, team_number: int):
        pass

    def get_event_matches(self, event_code: str):
        pass

    def get_team_performance_metrics(self, team_number, event_code=None):
        pass
