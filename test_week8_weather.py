#!/usr/bin/env python3
"""
Week 8 2025 All Weather Data - GraphQL Query
Get all Week 8 games with weather data using GraphQL
"""

import requests
import json
from datetime import datetime

# API Configuration
GRAPHQL_ENDPOINT = "https://graphql.collegefootballdata.com/v1/graphql"
API_KEY = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"

# GraphQL Query for Week 8 2025 FBS games with weather data
WEEK8_ALL_WEATHER_QUERY = """
query Week8FBSWeatherData($season: smallint!, $week: smallint!) {
  game(
    where: {
      season: { _eq: $season }
      week: { _eq: $week }
      _or: [
        { homeClassification: { _eq: "fbs" } }
        { awayClassification: { _eq: "fbs" } }
      ]
    }
    orderBy: { id: ASC }
  ) {
    id
    season
    week
    seasonType
    homeTeam
    awayTeam
    homeClassification
    awayClassification
    homeConference
    awayConference
    startDate
    venueId
    neutralSite
    conferenceGame
    status
    weather {
      gameId
      temperature
      dewpoint
      humidity
      precipitation
      pressure
      snowfall
      windDirection
      windSpeed
      windGust
      weatherConditionCode
    }
  }
}
"""

def fetch_week8_all_weather_graphql():
    """
    Fetch all Week 8 games with weather data using GraphQL.
    
    Returns:
        dict: The query results containing games and weather data
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    variables = {
        "season": 2025,
        "week": 8
    }
    
    payload = {
        "query": WEEK8_ALL_WEATHER_QUERY,
        "variables": variables
    }
    
    try:
        print(f"Fetching FBS Week 8 2025 weather data using GraphQL...")
        print("This will show FBS games with weather forecasts available...")
        print()
        
        response = requests.post(
            GRAPHQL_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        
        data = response.json()
        
        if "errors" in data:
            print(f"GraphQL Errors: {json.dumps(data['errors'], indent=2)}")
            return None
        
        return data.get("data", {})
    
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return None

def display_weather_summary(data):
    """Display summary of weather data"""
    if not data:
        print("No data received.")
        return
    
    games = data.get("game", [])
    
    print("=" * 100)
    print("WEEK 8 2025 - FBS GAMES WITH WEATHER DATA (GRAPHQL)")
    print("=" * 100)
    
    print(f"\n📊 SUMMARY:")
    print(f"   Total FBS games with weather data: {len(games)}")
    
    if games:
        print(f"\n🏈 FBS GAMES WITH WEATHER FORECASTS:")
        print("-" * 100)
        
        for i, game in enumerate(games, 1):
            home_team = game.get("homeTeam", "Unknown")
            away_team = game.get("awayTeam", "Unknown")
            venue_id = game.get("venueId", "Unknown")
            start_date = game.get("startDate", "Unknown")
            game_id = game.get("id", "Unknown")
            home_conf = game.get("homeConference", "N/A")
            away_conf = game.get("awayConference", "N/A")
            
            weather = game.get("weather", {})
            
            print(f"{i:2d}. {away_team} @ {home_team}")
            print(f"    Game ID: {game_id}")
            print(f"    Conferences: {away_conf} vs {home_conf}")
            print(f"    Venue ID: {venue_id}")
            print(f"    Date: {start_date}")
            
            if weather:
                temp = weather.get("temperature", "N/A")
                humidity = weather.get("humidity", "N/A")
                wind = weather.get("windSpeed", "N/A")
                precip = weather.get("precipitation", "N/A")
                condition_code = weather.get("weatherConditionCode", "N/A")
                
                print(f"    🌤️  Weather: {temp}°F, {humidity}% humidity, {wind} mph wind")
                print(f"         Precipitation: {precip}\", Condition Code: {condition_code}")
            else:
                print(f"    ⚠️  No weather data available")
            
            print()
    
    print("=" * 100)

def save_results(data):
    """Save results to JSON file"""
    if not data:
        print("No data to save.")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"week8_fbs_weather_graphql_{timestamp}.json"
    filepath = f"/Users/davlenswain/Desktop/Gameday_Graphql_Model/{filename}"
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✓ Results saved to: {filename}")
    return filepath

def main():
    """Main execution function"""
    print("=" * 100)
    print("WEEK 8 2025 - FBS WEATHER DATA GRAPHQL QUERY")
    print("=" * 100)
    print()
    
    # Fetch the data
    result = fetch_week8_all_weather_graphql()
    
    if result:
        # Display weather summary
        display_weather_summary(result)
        
        # Save to file
        filepath = save_results(result)
        
        print(f"\n✓ GraphQL query completed successfully!")
        
        # Check results
        games = result.get("game", [])
        
        if games:
            print(f"✓ Found {len(games)} FBS games with weather data!")
        else:
            print("⚠️  No FBS weather data found for Week 8.")
    else:
        print("\n✗ Query failed. Please check the errors above.")

if __name__ == "__main__":
    main()