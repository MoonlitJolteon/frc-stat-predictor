from abc import ABC, abstractmethod
from enum import Enum


class DataSourceStatus(Enum):
    CONNECTED = 1
    UNAUTHENTICATED = 2
    NOT_FOUND = 3


class DataSource(ABC):
    """Abstract base class for all data sources"""

    @abstractmethod
    def get_status(self) -> tuple[DataSourceStatus, dict]:
        """
        Retrieves the status of the data source along with any additional information.

        Returns:
        -------
        tuple[DataSourceStatus, dict]
            A tuple containing the data source status and a dictionary.
            The dictionary may include extra information under the keys "errors" and "extra_info".

        Notes:
        -----
        The errors and extra_info may be missing if there is nothing to be sent in them.
        """

    @abstractmethod
    def get_team_info(self, team_number: int):
        """Retrieve information about a specific team
        team_number: int
            The team you want to retrieve data for
        """

    @abstractmethod
    def get_event_matches(self, event_code: str, team_number: int | None = None):
        """Retrieve matches for a specific event
        event_code: str
            The eventcode for the event you want to retrieve match data from
        team_number: int | None
            The team you want to retrieve data for, if not provided will get all matches reguardless of teams
        """

    @abstractmethod
    def get_team_performance_metrics(self, team_number, event_code=None):
        """Get performance metrics for a team, optionally at a specific event

        team_number: int
            The team you want to retrieve data for

        (Optional) event_code: str | None
            The eventcode for the event you want to retrieve match data from"""
