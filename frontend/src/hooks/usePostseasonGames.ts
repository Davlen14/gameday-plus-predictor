import { useState, useEffect } from 'react';

export interface PostseasonGame {
  id: number;
  date: string;
  week: number;
  seasonType: string;
  home: {
    id: number;
    team: string;
    abbr: string;
    logo: string;
    color: string;
    altColor: string;
    record: string;
    rank: number | null;
    fpi: number | null;
    conference: string;
  };
  away: {
    id: number;
    team: string;
    abbr: string;
    logo: string;
    color: string;
    altColor: string;
    record: string;
    rank: number | null;
    fpi: number | null;
    conference: string;
  };
  betting: {
    spread: number | null;
    overUnder: number | null;
    homeMoneyline: number | null;
    awayMoneyline: number | null;
  };
  venue: string;
  neutralSite: boolean;
}

interface UsePostseasonGamesReturn {
  games: PostseasonGame[];
  isLoading: boolean;
  error: string | null;
  refetch: () => void;
}

export function usePostseasonGames(): UsePostseasonGamesReturn {
  const [games, setGames] = useState<PostseasonGame[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchGames = async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      const API_URL = (import.meta.env?.VITE_API_URL as string | undefined) || 'http://localhost:5002';
      const response = await fetch(`${API_URL}/api/upcoming-games?season_type=postseason`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setGames(data.games || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch postseason games');
      console.error('Error fetching postseason games:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchGames();
  }, []);

  return {
    games,
    isLoading,
    error,
    refetch: fetchGames
  };
}
