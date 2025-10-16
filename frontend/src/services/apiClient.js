// Simple API client to connect to your existing Flask backend
import { CONFIG } from '../config';
const API_BASE_URL = CONFIG.API.BASE_URL;

export class ApiClient {
  // Call your existing /predict endpoint
  static async getPrediction(homeTeam, awayTeam) {
    try {
      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          home_team: homeTeam,
          away_team: awayTeam
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to get prediction');
      }

      const data = await response.json();
      
      // Your Flask API already returns all the data your UI needs
      return {
        success: true,
        data: data
      };
      
    } catch (error) {
      console.error('API Error:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  // Health check your existing API
  static async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL}/`);
      return await response.json();
    } catch (error) {
      console.error('Health check failed:', error);
      return { status: 'error', message: error.message };
    }
  }

  // Get teams list (if you want to fetch from API instead of local JSON)
  static async getTeams() {
    try {
      const response = await fetch(`${API_BASE_URL}/teams`);
      if (!response.ok) throw new Error('Failed to fetch teams');
      return await response.json();
    } catch (error) {
      console.error('Failed to fetch teams:', error);
      // Fallback to local data
      return null;
    }
  }
}