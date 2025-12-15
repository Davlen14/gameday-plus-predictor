-- ESPN Players Table
-- Stores roster information for all FBS teams
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY,  -- ESPN player ID
    team_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    jersey TEXT,
    position TEXT,
    position_abbr TEXT,
    class_year TEXT,  -- FR, SO, JR, SR, GR
    height TEXT,
    weight INTEGER,
    hometown_city TEXT,
    hometown_state TEXT,
    headshot_url TEXT,
    status TEXT,  -- active, injured, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (team_id) REFERENCES teams(id)
);

-- ESPN Player Statistics Table
-- Season-level stats for each player
CREATE TABLE IF NOT EXISTS player_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    season INTEGER NOT NULL,
    games_played INTEGER,
    
    -- Passing stats
    passing_completions INTEGER,
    passing_attempts INTEGER,
    passing_yards INTEGER,
    passing_tds INTEGER,
    passing_interceptions INTEGER,
    passing_rating REAL,
    
    -- Rushing stats
    rushing_attempts INTEGER,
    rushing_yards INTEGER,
    rushing_tds INTEGER,
    rushing_avg REAL,
    rushing_long INTEGER,
    
    -- Receiving stats
    receiving_receptions INTEGER,
    receiving_yards INTEGER,
    receiving_tds INTEGER,
    receiving_avg REAL,
    receiving_long INTEGER,
    
    -- Defensive stats
    total_tackles INTEGER,
    solo_tackles INTEGER,
    tackles_for_loss REAL,
    sacks REAL,
    interceptions INTEGER,
    passes_defended INTEGER,
    forced_fumbles INTEGER,
    fumbles_recovered INTEGER,
    
    -- Other stats
    fumbles INTEGER,
    fumbles_lost INTEGER,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(id),
    UNIQUE(player_id, season)
);

-- ESPN Drives Table
-- Drive-level data for each game
CREATE TABLE IF NOT EXISTS drives (
    id TEXT PRIMARY KEY,  -- ESPN drive ID (string format like "401628546-1")
    game_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    sequence INTEGER NOT NULL,
    description TEXT,
    yards INTEGER,
    plays_count INTEGER,
    result TEXT,
    start_period INTEGER,
    start_clock TEXT,
    start_yardline INTEGER,
    start_yards_to_endzone INTEGER,
    end_period INTEGER,
    end_clock TEXT,
    end_yardline INTEGER,
    end_yards_to_endzone INTEGER,
    time_elapsed TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (game_id) REFERENCES games(id),
    FOREIGN KEY (team_id) REFERENCES teams(id)
);

-- ESPN Plays Table
-- Play-by-play data for each drive
CREATE TABLE IF NOT EXISTS plays (
    id TEXT PRIMARY KEY,  -- ESPN play ID
    drive_id TEXT NOT NULL,
    game_id INTEGER NOT NULL,
    sequence_number INTEGER NOT NULL,
    type_id INTEGER,
    type_text TEXT,
    play_text TEXT NOT NULL,
    away_score INTEGER,
    home_score INTEGER,
    period INTEGER,
    clock TEXT,
    down INTEGER,
    distance INTEGER,
    yard_line INTEGER,
    yards_to_endzone INTEGER,
    yards_gained INTEGER,
    scoring_play BOOLEAN DEFAULT 0,
    turnover BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (drive_id) REFERENCES drives(id),
    FOREIGN KEY (game_id) REFERENCES games(id)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_players_team ON players(team_id);
CREATE INDEX IF NOT EXISTS idx_players_position ON players(position_abbr);
CREATE INDEX IF NOT EXISTS idx_player_stats_player ON player_stats(player_id);
CREATE INDEX IF NOT EXISTS idx_player_stats_season ON player_stats(season);
CREATE INDEX IF NOT EXISTS idx_drives_game ON drives(game_id);
CREATE INDEX IF NOT EXISTS idx_drives_team ON drives(team_id);
CREATE INDEX IF NOT EXISTS idx_plays_drive ON plays(drive_id);
CREATE INDEX IF NOT EXISTS idx_plays_game ON plays(game_id);
CREATE INDEX IF NOT EXISTS idx_plays_scoring ON plays(scoring_play);
