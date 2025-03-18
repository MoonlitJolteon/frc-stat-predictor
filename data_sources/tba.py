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
        matches = None
        team_key = f"frc{team_number}"

        if event_code != None:
            matches = self.get_event_matches(event_code, team_number)
        else:
            url = f"{self.__base_url}/team/{team_key}/matches/{self.__observed_year}"
            response = requests.get(url, headers=self.__headers)
            if response.status_code == 200:
                matches = response.json()

        if matches == None:
            return None

        performance = {
            "team_number": team_number,
            "matches_played": 0,
            "wins": 0,
            "losses": 0,
            "auto_performance": {
                "auto_line_crosses": 0,
                "line_cross_success_rate": 0.0,
                "avg_auto_contribution": 0.0,
                "total_auto_points": 0,
                "auto_coral_count": 0,
            },
            "teleop_performance": {
                "avg_teleop_contribution": 0.0,
                "total_teleop_points": 0,
                "estimated_coral_per_match": 0.0,
                "total_coral_count": 0,
                "reef_placements": {
                    "top_row": 0,
                    "mid_row": 0,
                    "bot_row": 0,
                    "trough": 0,
                },
            },
            "endgame_performance": {
                "parked_count": 0,
                "parked_rate": 0.0,
                "deep_cage_count": 0,
                "deep_cage_rate": 0.0,
                "shallow_cage_count": 0,
                "shallow_cage_rate": 0.0,
                "none_count": 0,
                "none_rate": 0.0,
                "total_endgame_points": 0,
                "avg_endgame_points": 0.0,
            },
            "overall_metrics": {
                "total_estimated_points": 0,
                "avg_points_per_match": 0.0,
                "contribution_percentages": [],
                "avg_contribution_percentage": 0.0,
                "consistency_rating": 0.0,
            },
            "match_history": [],
        }

        contribution_percentages = []

        for match in matches:
            red_alliance = match["alliances"]["red"]["team_keys"]
            blue_alliance = match["alliances"]["blue"]["team_keys"]

            if team_key in red_alliance:
                alliance_color = "red"
                robot_position = red_alliance.index(team_key) + 1
            elif team_key in blue_alliance:
                alliance_color = "blue"
                robot_position = blue_alliance.index(team_key) + 1
            else:
                # Team not in this match
                continue

            performance["matches_played"] += 1
            if match["winning_alliance"] == alliance_color:
                performance["wins"] += 1
            else:
                performance["losses"] += 1

            alliance_data = match["score_breakdown"][alliance_color]
            match_points = {"auto": 0, "teleop": 0, "endgame": 0, "total": 0}
            alliance_total = alliance_data["totalPoints"]

            # Initialize match record to be added to match_history
            match_record = {
                "match_key": match["key"],
                "alliance": alliance_color,
                "result": (
                    "win" if match["winning_alliance"] == alliance_color else "loss"
                ),
                "robot_position": robot_position,
                "auto_line": alliance_data[f"autoLineRobot{robot_position}"],
                "endgame": alliance_data[f"endGameRobot{robot_position}"],
                "estimated_points": {"auto": 0, "teleop": 0, "endgame": 0, "total": 0},
                "alliance_total": alliance_total,
                "contribution_percentage": 0.0,
            }

            self.__calculate_auto_performance(
                performance, match_points, match_record, alliance_data, robot_position
            )
            self.__calculate_teleop_performance(
                performance, match_points, match_record, alliance_data, robot_position
            )
            self.__calculate_endgame_performance(
                performance, match_points, match_record, alliance_data, robot_position
            )

            # Calculate total contribution for this match
            match_points["total"] = (
                match_points["auto"] + match_points["teleop"] + match_points["endgame"]
            )
            match_record["estimated_points"]["total"] = match_points["total"]

            # Calculate contribution percentage
            contribution_percentage = (
                match_points["total"] / alliance_total if alliance_total > 0 else 0
            )
            match_record["contribution_percentage"] = contribution_percentage
            contribution_percentages.append(contribution_percentage)

            # Add match record to history
            performance["overall_metrics"]["total_estimated_points"] += match_points[
                "total"
            ]
            performance["match_history"].append(match_record)

        # After processing all matches:
        if performance["matches_played"] > 0:
            # Auto performance rates
            performance["auto_performance"]["line_cross_success_rate"] = (
                performance["auto_performance"]["auto_line_crosses"]
                / performance["matches_played"]
            )
            performance["auto_performance"]["avg_auto_contribution"] = (
                performance["auto_performance"]["total_auto_points"]
                / performance["matches_played"]
            )

            # Teleop performance rates
            performance["teleop_performance"]["avg_teleop_contribution"] = (
                performance["teleop_performance"]["total_teleop_points"]
                / performance["matches_played"]
            )
            performance["teleop_performance"]["estimated_coral_per_match"] = (
                performance["teleop_performance"]["total_coral_count"]
                / performance["matches_played"]
            )

            # Endgame performance rates
            total_endgame = (
                performance["endgame_performance"]["parked_count"]
                + performance["endgame_performance"]["deep_cage_count"]
                + performance["endgame_performance"]["shallow_cage_count"]
                + performance["endgame_performance"]["none_count"]
            )

            performance["endgame_performance"]["parked_rate"] = (
                performance["endgame_performance"]["parked_count"]
                / performance["matches_played"]
            )
            performance["endgame_performance"]["deep_cage_rate"] = (
                performance["endgame_performance"]["deep_cage_count"]
                / performance["matches_played"]
            )
            performance["endgame_performance"]["shallow_cage_rate"] = (
                performance["endgame_performance"]["shallow_cage_count"]
                / performance["matches_played"]
            )
            performance["endgame_performance"]["none_rate"] = (
                performance["endgame_performance"]["none_count"]
                / performance["matches_played"]
            )
            performance["endgame_performance"]["avg_endgame_points"] = (
                performance["endgame_performance"]["total_endgame_points"]
                / performance["matches_played"]
            )

            # Overall performance metrics
            performance["overall_metrics"]["avg_points_per_match"] = (
                performance["overall_metrics"]["total_estimated_points"]
                / performance["matches_played"]
            )

            # Calculate consistency metrics
            if contribution_percentages:
                performance["overall_metrics"][
                    "contribution_percentages"
                ] = contribution_percentages
                mean = sum(contribution_percentages) / len(contribution_percentages)
                performance["overall_metrics"]["avg_contribution_percentage"] = mean

                # Calculate standard deviation
                variance = sum((x - mean) ** 2 for x in contribution_percentages) / len(
                    contribution_percentages
                )
                std_dev = variance**0.5

                # Higher consistency means lower standard deviation relative to the mean
                performance["overall_metrics"]["consistency_rating"] = 1 - (
                    std_dev / mean if mean > 0 else 0
                )

        return performance

    def __calculate_auto_performance(
        self, performance, match_points, match_record, alliance_data, robot_position
    ):
        auto_line_status = alliance_data[f"autoLineRobot{robot_position}"]
        if auto_line_status == "Yes":
            performance["auto_performance"]["auto_line_crosses"] += 1
            estimated_auto_points = 3  # Mobility points

            # If auto bonus achieved, attribute partial credit for coral as the data doesn't track who scored it
            if alliance_data["autoBonusAchieved"]:
                robots_crossed = sum(
                    1
                    for i in range(1, 4)
                    if alliance_data[f"autoLineRobot{i}"] == "Yes"
                )
                if robots_crossed > 0:
                    auto_coral_points = alliance_data["autoCoralPoints"]
                    estimated_auto_points += auto_coral_points / robots_crossed

                    # Track auto coral count (approximately)
                    auto_coral_count = alliance_data["autoCoralCount"] / robots_crossed
                    performance["auto_performance"][
                        "auto_coral_count"
                    ] += auto_coral_count
        else:
            estimated_auto_points = 0

        performance["auto_performance"]["total_auto_points"] += estimated_auto_points
        match_points["auto"] = estimated_auto_points
        match_record["estimated_points"]["auto"] = estimated_auto_points

    def __calculate_endgame_performance(
        self, performance, match_points, match_record, alliance_data, robot_position
    ):
        endgame_status = alliance_data[f"endGameRobot{robot_position}"]
        if endgame_status == "Parked":
            performance["endgame_performance"]["parked_count"] += 1
            estimated_endgame_points = 2  # Points for parking
        elif endgame_status == "DeepCage":
            performance["endgame_performance"]["deep_cage_count"] += 1
            estimated_endgame_points = 12  # Points for deep cage
        elif endgame_status == "ShallowCage":
            performance["endgame_performance"]["shallow_cage_count"] += 1
            estimated_endgame_points = 6  # Points for shallow cage
        else:  # None
            performance["endgame_performance"]["none_count"] += 1
            estimated_endgame_points = 0

        performance["endgame_performance"][
            "total_endgame_points"
        ] += estimated_endgame_points
        match_points["endgame"] = estimated_endgame_points
        match_record["estimated_points"]["endgame"] = estimated_endgame_points

    def __calculate_teleop_performance(
        self, performance, match_points, match_record, alliance_data, robot_position
    ):
        # Teleop performance estimation
        robots_active = 3  # Assume all 3 robots contribute by default

        # Basic estimate: divide equally
        basic_teleop_estimate = alliance_data["teleopPoints"] / robots_active

        # Adjust based on activity levels (if a robot didn't cross auto line, might be less active)
        activity_adjustments = {1: 1.0, 2: 1.0, 3: 1.0}  # Full activity

        for i in range(1, 4):
            if alliance_data[f"autoLineRobot{i}"] == "No":
                activity_adjustments[i] = 0.7  # Reduced activity if didn't move in auto

        # Calculate adjusted teleop estimate
        total_activity = sum(activity_adjustments.values())
        adjusted_teleop_estimate = (
            alliance_data["teleopPoints"]
            * activity_adjustments[robot_position]
            / total_activity
        )

        # Track coral placements
        total_coral = alliance_data["teleopCoralCount"]
        estimated_coral = (
            total_coral * activity_adjustments[robot_position] / total_activity
        )
        performance["teleop_performance"]["total_coral_count"] += estimated_coral

        # Track reef placements
        reef_data = alliance_data["teleopReef"]
        top_row_count = reef_data["tba_topRowCount"]
        mid_row_count = reef_data["tba_midRowCount"]
        bot_row_count = reef_data["tba_botRowCount"]
        trough_count = reef_data.get("trough", 0)

        # Attribute reef placements based on activity adjustment
        performance["teleop_performance"]["reef_placements"]["top_row"] += (
            top_row_count * activity_adjustments[robot_position] / total_activity
        )
        performance["teleop_performance"]["reef_placements"]["mid_row"] += (
            mid_row_count * activity_adjustments[robot_position] / total_activity
        )
        performance["teleop_performance"]["reef_placements"]["bot_row"] += (
            bot_row_count * activity_adjustments[robot_position] / total_activity
        )
        performance["teleop_performance"]["reef_placements"]["trough"] += (
            trough_count * activity_adjustments[robot_position] / total_activity
        )

        performance["teleop_performance"][
            "total_teleop_points"
        ] += adjusted_teleop_estimate
        match_points["teleop"] = adjusted_teleop_estimate
        match_record["estimated_points"]["teleop"] = adjusted_teleop_estimate
