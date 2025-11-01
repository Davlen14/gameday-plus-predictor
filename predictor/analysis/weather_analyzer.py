from typing import Dict, Any
import random
from datetime import datetime

class WeatherAnalyzer:
    """Handles weather analysis and impact calculations"""
    
    def __init__(self, static_data: Dict = None):
        self.static_data = static_data or {}
    
    def _generate_realistic_weather(self, home_team_name: str, game_date: str = None) -> Dict[str, float]:
        """
        Generate realistic weather conditions based on team location and season.
        Returns weather data with temperature, wind_speed, precipitation, and weather_factor.
        """
        # Simplified weather generation - basic defaults
        base_conditions = {
            'temperature': 72.0,
            'wind_speed': 8.0,
            'precipitation': 0.0,
            'weather_factor': 1.0,
            'conditions': 'Clear'
        }
        
        # Add some variation based on team location (simplified)
        regional_adjustments = {
            'Miami': {'temperature': 82.0, 'wind_speed': 6.0, 'precipitation': 0.1},
            'Syracuse': {'temperature': 45.0, 'wind_speed': 12.0, 'precipitation': 0.3},
            'Georgia Tech': {'temperature': 75.0, 'wind_speed': 7.0, 'precipitation': 0.1},
            'Louisville': {'temperature': 68.0, 'wind_speed': 9.0, 'precipitation': 0.2}
        }
        
        if home_team_name in regional_adjustments:
            adjustments = regional_adjustments[home_team_name]
            base_conditions.update(adjustments)
        
        return base_conditions
    
    def analyze_weather_impact(self, weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze weather impact on game performance"""
        temperature = weather_data.get('temperature', 72.0)
        wind_speed = weather_data.get('wind_speed', 8.0)
        precipitation = weather_data.get('precipitation', 0.0)
        
        # Calculate weather impact factors
        temp_factor = self._calculate_temperature_impact(temperature)
        wind_factor = self._calculate_wind_impact(wind_speed)
        precip_factor = self._calculate_precipitation_impact(precipitation)
        
        overall_factor = (temp_factor + wind_factor + precip_factor) / 3
        
        return {
            'temperature_impact': temp_factor,
            'wind_impact': wind_factor,
            'precipitation_impact': precip_factor,
            'overall_weather_factor': overall_factor,
            'passing_game_impact': wind_factor * precip_factor,
            'running_game_impact': precip_factor,
            'kicking_game_impact': wind_factor
        }
    
    def _calculate_temperature_impact(self, temperature: float) -> float:
        """Calculate impact of temperature on game performance"""
        # Optimal temperature range is 65-75°F
        if 65 <= temperature <= 75:
            return 1.0
        elif temperature < 32:  # Freezing
            return 0.7
        elif temperature > 95:  # Very hot
            return 0.8
        else:
            return 0.9
    
    def _calculate_wind_impact(self, wind_speed: float) -> float:
        """Calculate impact of wind on game performance"""
        if wind_speed < 10:
            return 1.0
        elif wind_speed < 20:
            return 0.9
        elif wind_speed < 30:
            return 0.8
        else:
            return 0.7
    
    def _calculate_precipitation_impact(self, precipitation: float) -> float:
        """Calculate impact of precipitation on game performance"""
        if precipitation == 0:
            return 1.0
        elif precipitation < 0.1:
            return 0.95
        elif precipitation < 0.5:
            return 0.85
        else:
            return 0.75