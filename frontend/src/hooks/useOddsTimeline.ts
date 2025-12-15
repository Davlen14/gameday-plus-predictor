import { useState, useEffect, useCallback, useRef } from 'react';

/**
 * Historical odds data point structure
 */
export interface OddsDataPoint {
  bookId: number;
  spread: number;
  spreadOdds: number;
  total: number;
  totalOdds?: number;
  moneyline?: number;
  timestamp: string;
}

/**
 * Merged odds timeline with historical + live data
 */
export interface OddsTimeline {
  data: OddsDataPoint[];
  lastUpdated: string;
  isLoading: boolean;
  error: string | null;
}

/**
 * Hook configuration options
 */
interface UseOddsTimelineOptions {
  gameId: string | number;
  awayTeam: string;
  homeTeam: string;
  isModalOpen: boolean;
  pollInterval?: number; // milliseconds, default 180000 (3 minutes)
  enablePolling?: boolean; // default true
}

/**
 * Game identifier mapping for historical JSON files
 */
const GAME_FILE_MAP: Record<string, string> = {
  // Ohio State vs Indiana
  'osu_indiana': 'osu_indiana_historical_odds.json',
  'ohio_state_indiana': 'osu_indiana_historical_odds.json',
  'indiana_ohio_state': 'osu_indiana_historical_odds.json',
  'indiana_osu': 'osu_indiana_historical_odds.json',
  
  // Kennesaw State vs Jacksonville State
  'kennesaw_jacksonville': 'kennesaw_jacksonville_historical_odds.json',
  'kennesaw_state_jacksonville_state': 'kennesaw_jacksonville_historical_odds.json',
  'jacksonville_state_kennesaw_state': 'kennesaw_jacksonville_historical_odds.json',
  'jacksonville_kennesaw': 'kennesaw_jacksonville_historical_odds.json',
  
  // James Madison vs Troy
  'jmu_troy': 'jmu_troy_historical_odds.json',
  'james_madison_troy': 'jmu_troy_historical_odds.json',
  'troy_james_madison': 'jmu_troy_historical_odds.json',
  'troy_jmu': 'jmu_troy_historical_odds.json',
  
  // Duke vs Virginia
  'duke_virginia': 'duke_virginia_historical_odds.json',
  'virginia_duke': 'duke_virginia_historical_odds.json',
  
  // Georgia vs Alabama
  'georgia_alabama': 'georgia_alabama_historical_odds.json',
  'georgia_bulldogs_alabama_crimson_tide': 'georgia_alabama_historical_odds.json',
  'alabama_crimson_tide_georgia_bulldogs': 'georgia_alabama_historical_odds.json',
  'alabama_georgia': 'georgia_alabama_historical_odds.json',
  
  // Western Michigan vs Miami (OH)
  'wmu_miami_oh': 'wmu_miami_oh_historical_odds.json',
  'western_michigan_miami_oh': 'wmu_miami_oh_historical_odds.json',
  'miami_oh_western_michigan': 'wmu_miami_oh_historical_odds.json',
  'miami_oh_wmu': 'wmu_miami_oh_historical_odds.json',
  
  // BYU vs Texas Tech
  'byu_texas_tech': 'byu_texas_tech_historical_odds.json',
  'texas_tech_byu': 'byu_texas_tech_historical_odds.json',
  
  // North Texas vs Tulane
  'north_texas_tulane': 'north_texas_tulane_historical_odds.json',
  'tulane_north_texas': 'north_texas_tulane_historical_odds.json',
  
  // UNLV vs Boise State
  'unlv_bsu': 'unlv_bsu_historical_odds.json',
  'unlv_boise_state': 'unlv_bsu_historical_odds.json',
  'unlv_rebels_boise_state_broncos': 'unlv_bsu_historical_odds.json',
  'boise_state_unlv': 'unlv_bsu_historical_odds.json',
  'bsu_unlv': 'unlv_bsu_historical_odds.json',
};

/**
 * Generate game key from team names
 */
const getGameKey = (away: string, home: string): string => {
  const normalize = (team: string) => {
    // Remove common mascot/team suffixes to get school name
    const cleanName = team
      .replace(/\s+(Crimson Tide|Bulldogs|Buckeyes|Hoosiers|Owls|Rebels|Broncos|Red Raiders|Mean Green|Green Wave|Cavaliers|Blue Devils|Dukes|Trojans|Redhawks|Eagles|Mountaineers)$/i, '')
      .toLowerCase()
      .replace(/\s+/g, '_')
      .replace(/[()]/g, '');
    
    return cleanName;
  };

  return `${normalize(away)}_${normalize(home)}`;
};

/**
 * Find matching historical file for a game
 */
const findHistoricalFile = (away: string, home: string): string | null => {
  const gameKey = getGameKey(away, home);

  // Try exact match first
  if (GAME_FILE_MAP[gameKey]) {
    return GAME_FILE_MAP[gameKey];
  }

  // Try reversed (home_away)
  const reversedKey = getGameKey(home, away);
  if (GAME_FILE_MAP[reversedKey]) {
    return GAME_FILE_MAP[reversedKey];
  }

  // Try partial matches
  for (const [key, file] of Object.entries(GAME_FILE_MAP)) {
    const awayNorm = away.toLowerCase().replace(/\s+/g, '_');
    const homeNorm = home.toLowerCase().replace(/\s+/g, '_');

    if (key.includes(awayNorm) && key.includes(homeNorm)) {
      return file;
    }
  }

  return null;
};

/**
 * Load historical odds from JSON file
 */
const loadHistoricalOdds = async (
  away: string,
  home: string
): Promise<OddsDataPoint[]> => {
  const filename = findHistoricalFile(away, home);

  if (!filename) {
    console.warn(`[OddsTimeline] No historical file found for "${away}" vs "${home}"`);
    console.warn(`[OddsTimeline] Generated game key: ${getGameKey(away, home)}`);
    return [];
  }

  try {
    console.log(`[OddsTimeline] Loading historical data from: ${filename}`);
    const response = await fetch(`/${filename}`);

    if (!response.ok) {
      throw new Error(`Failed to load ${filename}: ${response.statusText}`);
    }

    const data = await response.json();

    if (!Array.isArray(data)) {
      throw new Error(`Invalid data format in ${filename}`);
    }

    console.log(`[OddsTimeline] Loaded ${data.length} historical data points from ${filename}`);
    return data;
  } catch (error) {
    console.error(`[OddsTimeline] Error loading historical odds for ${away} vs ${home}:`, error);
    return [];
  }
};

/**
 * Fetch live odds from Action Network API
 */
const fetchLiveOdds = async (
  gameId: string | number
): Promise<OddsDataPoint[]> => {
  try {
    // Replace with your actual Action Network API endpoint
    const response = await fetch(`/api/action-network/odds/${gameId}`);

    if (!response.ok) {
      throw new Error(`API request failed: ${response.statusText}`);
    }

    const data = await response.json();

    // Transform Action Network response to our format
    // Adjust this based on your actual API response structure
    if (data.odds && Array.isArray(data.odds)) {
      return data.odds.map((odd: any) => ({
        bookId: odd.bookId || odd.book_id,
        spread: odd.spread,
        spreadOdds: odd.spreadOdds || odd.spread_odds,
        total: odd.total,
        totalOdds: odd.totalOdds || odd.total_odds,
        moneyline: odd.moneyline,
        timestamp: odd.timestamp || new Date().toISOString(),
      }));
    }

    return [];
  } catch (error) {
    console.error(`Error fetching live odds for game ${gameId}:`, error);
    return [];
  }
};

/**
 * Merge historical and live odds, removing duplicates
 */
const mergeOdds = (
  historical: OddsDataPoint[],
  live: OddsDataPoint[]
): OddsDataPoint[] => {
  const merged = [...historical];
  const existingKeys = new Set(
    historical.map(item => `${item.timestamp}_${item.bookId}`)
  );

  // Add live data that doesn't exist in historical
  for (const liveItem of live) {
    const key = `${liveItem.timestamp}_${liveItem.bookId}`;
    if (!existingKeys.has(key)) {
      merged.push(liveItem);
      existingKeys.add(key);
    }
  }

  // Sort by timestamp (oldest to newest)
  return merged.sort((a, b) =>
    new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
  );
};

/**
 * Save to localStorage
 */
const saveToLocalStorage = (
  gameId: string | number,
  data: OddsDataPoint[]
): void => {
  try {
    const key = `odds_timeline_${gameId}`;
    localStorage.setItem(key, JSON.stringify({
      data,
      lastUpdated: new Date().toISOString(),
    }));
  } catch (error) {
    console.error('Error saving to localStorage:', error);
  }
};

/**
 * Load from localStorage
 */
const loadFromLocalStorage = (
  gameId: string | number
): { data: OddsDataPoint[]; lastUpdated: string } | null => {
  try {
    const key = `odds_timeline_${gameId}`;
    const stored = localStorage.getItem(key);

    if (!stored) return null;

    const parsed = JSON.parse(stored);
    return {
      data: parsed.data || [],
      lastUpdated: parsed.lastUpdated || new Date().toISOString(),
    };
  } catch (error) {
    console.error('Error loading from localStorage:', error);
    return null;
  }
};

/**
 * Custom hook for managing odds timeline data
 *
 * Features:
 * - Loads historical baseline from JSON file
 * - Polls Action Network API every 3 minutes
 * - Merges live + historical without duplicates
 * - Persists to localStorage
 * - Automatic cleanup on modal close
 *
 * @example
 * ```tsx
 * const { timeline, refresh, clearCache } = useOddsTimeline({
 *   gameId: 'osu_indiana',
 *   awayTeam: 'Indiana',
 *   homeTeam: 'Ohio State',
 *   isModalOpen: true,
 * });
 *
 * // timeline.data contains merged historical + live odds
 * // timeline.isLoading indicates loading state
 * // timeline.error contains error message if any
 * ```
 */
export const useOddsTimeline = ({
  gameId,
  awayTeam,
  homeTeam,
  isModalOpen,
  pollInterval = 180000, // 3 minutes
  enablePolling = true,
}: UseOddsTimelineOptions) => {
  const [timeline, setTimeline] = useState<OddsTimeline>({
    data: [],
    lastUpdated: new Date().toISOString(),
    isLoading: true,
    error: null,
  });

  const pollTimerRef = useRef<NodeJS.Timeout | null>(null);
  const isMountedRef = useRef(true);
  const hasLoadedHistoricalRef = useRef(false);
  const lastGameIdRef = useRef<string>('');

  // Reset historical loaded flag when game changes
  useEffect(() => {
    const currentGameKey = `${gameId}_${awayTeam}_${homeTeam}`;
    if (currentGameKey !== lastGameIdRef.current) {
      hasLoadedHistoricalRef.current = false;
      lastGameIdRef.current = currentGameKey;
    }
  }, [gameId, awayTeam, homeTeam]);

  /**
   * Load and merge all odds data
   */
  const loadOddsData = useCallback(async (skipCache = false) => {
    if (!isModalOpen) return;

    setTimeline(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      // 1. Try localStorage first (unless skipCache)
      let cachedData: OddsDataPoint[] = [];
      if (!skipCache) {
        const cached = loadFromLocalStorage(gameId);
        if (cached && cached.data.length > 0) {
          cachedData = cached.data;
          setTimeline({
            data: cachedData,
            lastUpdated: cached.lastUpdated,
            isLoading: true, // Still loading live data
            error: null,
          });
        }
      }

      // 2. Load historical baseline (only once per mount)
      let historicalData: OddsDataPoint[] = [];
      if (!hasLoadedHistoricalRef.current || skipCache) {
        historicalData = await loadHistoricalOdds(awayTeam, homeTeam);
        hasLoadedHistoricalRef.current = true;
      } else {
        // Use cached data as historical if we've already loaded
        historicalData = cachedData;
      }

      // 3. Fetch live data from API
      let liveData: OddsDataPoint[] = [];
      if (enablePolling) {
        liveData = await fetchLiveOdds(gameId);
      }

      // 4. Merge historical + live
      const merged = mergeOdds(historicalData, liveData);

      if (!isMountedRef.current) return;

      // 5. Update state
      const newTimeline = {
        data: merged,
        lastUpdated: new Date().toISOString(),
        isLoading: false,
        error: null,
      };

      setTimeline(newTimeline);

      // 6. Persist to localStorage
      saveToLocalStorage(gameId, merged);

    } catch (error) {
      if (!isMountedRef.current) return;

      const errorMessage = error instanceof Error ? error.message : 'Failed to load odds data';
      console.error('Error loading odds timeline:', error);

      setTimeline(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }));
    }
  }, [gameId, awayTeam, homeTeam, isModalOpen, enablePolling]);

  /**
   * Start polling
   */
  const startPolling = useCallback(() => {
    if (!enablePolling || !isModalOpen) return;

    // Clear existing timer
    if (pollTimerRef.current) {
      clearInterval(pollTimerRef.current);
    }

    // Set new polling interval
    pollTimerRef.current = setInterval(() => {
      loadOddsData(false); // Don't skip cache on polls
    }, pollInterval);
  }, [enablePolling, isModalOpen, loadOddsData, pollInterval]);

  /**
   * Stop polling
   */
  const stopPolling = useCallback(() => {
    if (pollTimerRef.current) {
      clearInterval(pollTimerRef.current);
      pollTimerRef.current = null;
    }
  }, []);

  /**
   * Manual refresh
   */
  const refresh = useCallback(async () => {
    await loadOddsData(true); // Skip cache on manual refresh
  }, [loadOddsData]);

  /**
   * Clear cached data
   */
  const clearCache = useCallback(() => {
    try {
      const key = `odds_timeline_${gameId}`;
      localStorage.removeItem(key);
      hasLoadedHistoricalRef.current = false;
    } catch (error) {
      console.error('Error clearing cache:', error);
    }
  }, [gameId]);

  // Initial load when modal opens
  useEffect(() => {
    if (isModalOpen) {
      loadOddsData(false);
      startPolling();
    }

    return () => {
      stopPolling();
    };
  }, [isModalOpen, loadOddsData, startPolling, stopPolling]);

  // Cleanup on unmount
  useEffect(() => {
    isMountedRef.current = true;

    return () => {
      isMountedRef.current = false;
      stopPolling();
    };
  }, [stopPolling]);

  return {
    timeline,
    refresh,
    clearCache,
    isPolling: pollTimerRef.current !== null,
  };
};
