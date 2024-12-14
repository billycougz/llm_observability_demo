import requests

def get_team_id(team_abbreviation: str):
    """
    Retrieve the team ID based on the team abbreviation.

    Args:
        team_abbreviation: The abbreviation of the NFL team (e.g., "ARI" for Arizona Cardinals).

    Returns:
        int: The team ID associated with the given abbreviation, or None if the abbreviation is not found.
    """
    TEAM_IDS = {
        "ARI": 22,  # Arizona Cardinals
        "ATL": 1,   # Atlanta Falcons
        "BAL": 33,  # Baltimore Ravens
        "BUF": 2,   # Buffalo Bills
        "CAR": 29,  # Carolina Panthers
        "CHI": 3,   # Chicago Bears
        "CIN": 4,   # Cincinnati Bengals
        "CLE": 5,   # Cleveland Browns
        "DAL": 6,   # Dallas Cowboys
        "DEN": 7,   # Denver Broncos
        "DET": 8,   # Detroit Lions
        "GB": 9,    # Green Bay Packers
        "HOU": 34,  # Houston Texans
        "IND": 11,  # Indianapolis Colts
        "JAX": 30,  # Jacksonville Jaguars
        "KC": 12,   # Kansas City Chiefs
        "LV": 13,   # Las Vegas Raiders
        "LAC": 24,  # Los Angeles Chargers
        "LAR": 14,  # Los Angeles Rams
        "MIA": 15,  # Miami Dolphins
        "MIN": 16,  # Minnesota Vikings
        "NE": 17,   # New England Patriots
        "NO": 18,   # New Orleans Saints
        "NYG": 19,  # New York Giants
        "NYJ": 20,  # New York Jets
        "PHI": 21,  # Philadelphia Eagles
        "PIT": 23,  # Pittsburgh Steelers
        "SF": 25,   # San Francisco 49ers
        "SEA": 26,  # Seattle Seahawks
        "TB": 27,   # Tampa Bay Buccaneers
        "TEN": 10,  # Tennessee Titans
        "WAS": 28   # Washington Commanders
    }
    return TEAM_IDS.get(team_abbreviation)

def get_team_players(team_id: str):
    """
    Retrieve the list of players for a given NFL team.

    Args:
        team_id: The ID of the NFL team.

    Returns:
        list: A list of dictionaries containing player details such as name, ID, and position.
    """
    roster_url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/roster"
    response = requests.get(roster_url)
    position_categories = response.json().get('athletes', [])
    players = [item for category in position_categories for item in category.get('items', [])]
    return players
  
def get_player_id(player_name: str, team_players: list):
    """
    Retrieve the player ID for a given player name from the team's roster.

    Args:
        player_name: The name of the player to search for.
        team_players: A list of players from the team's roster.

    Returns:
        str: The player's ID if the player is found, otherwise None.
    """
    for player in team_players:
        if player['displayName'].lower() == player_name.lower():
            return player['id']

def get_player_stats(player_id: str):
    """
    Retrieve the statistics for a player by their ID.

    Args:
        player_id: The ID of the player whose statistics need to be fetched.

    Returns:
        dict: A dictionary containing the player's statistics, or None if the request fails.
    """
    stats_url = f"https://site.api.espn.com/apis/common/v3/sports/football/nfl/athletes/{player_id}/stats"
    stats_response = requests.get(stats_url)
    
    if stats_response.status_code != 200:
        print(f"Failed to fetch player stats. Status code: {stats_response.status_code}")
        return None
    
    stats = stats_response.json()
    return stats

def get_nfl_team_stats(team_id: str):
    """
    Retrieve the statistics for a team's players by the team's ID.

    Args:
        team_id: ID of the NFL team.
    
    Returns:
        dict: Dictionary containing the team's stats.
    """
    url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/statistics"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        
        # Check if data contains team stats
        if 'team' in data:
            return data['team']
        else:
            return {"error": "Team stats not found"}
    
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

import requests
from datetime import datetime

def get_recent_game_stats(team_id: str, num_games: int):
    """
    Retrieve the statistics for the most recent games for a team.

    Args:
        team_id: ID of the NFL team.
        num_games: Number of recent games to fetch stats for.
    
    Returns:
        list: List of dictionaries containing stats for the most recent games.
    """
    # Step 1: Fetch the team's schedule
    schedule_url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/schedule"
   
    try:
        schedule_response = requests.get(schedule_url)
        schedule_response.raise_for_status()
        schedule_data = schedule_response.json()
        
        # Step 2: Find the most recent completed games
        recent_games = []
        if 'events' in schedule_data:
            for event in schedule_data['events']:
                game = event['competitions'][0]
                # Check for completed games
                if 'status' in game and game['status']['type']['name'] == 'STATUS_FINAL':
                    game_date = datetime.strptime(game['date'], "%Y-%m-%dT%H:%MZ")
                    recent_games.append({
                        'game_id': game['id'],
                        'date': game_date
                    })
        # Sort games by date (most recent first)
        recent_games = sorted(recent_games, key=lambda x: x['date'], reverse=True)
        
        # Step 3: Fetch stats for the specified number of games
        game_stats_list = []
        for game in recent_games[:num_games]:
            game_id = game['game_id']
            game_stats_url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={game_id}"
            game_stats_response = requests.get(game_stats_url)
            game_stats_response.raise_for_status()
            game_stats_data = game_stats_response.json()
            
            game_stats_list.append(game_stats_data['boxscore'])

        return game_stats_list

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
