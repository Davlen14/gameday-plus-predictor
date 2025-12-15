-- Add missing box score stats to team_seasons table
-- These stats are available from College Football Data API but not in current schema

ALTER TABLE team_seasons ADD COLUMN possession_time INTEGER DEFAULT 0;
ALTER TABLE team_seasons ADD COLUMN possession_time_opponent INTEGER DEFAULT 0;
ALTER TABLE team_seasons ADD COLUMN turnovers INTEGER DEFAULT 0;
ALTER TABLE team_seasons ADD COLUMN turnovers_opponent INTEGER DEFAULT 0;
ALTER TABLE team_seasons ADD COLUMN turnover_margin INTEGER DEFAULT 0;
ALTER TABLE team_seasons ADD COLUMN penalty_yards INTEGER DEFAULT 0;
ALTER TABLE team_seasons ADD COLUMN sacks INTEGER DEFAULT 0;
ALTER TABLE team_seasons ADD COLUMN interceptions INTEGER DEFAULT 0;
ALTER TABLE team_seasons ADD COLUMN tackles_for_loss INTEGER DEFAULT 0;
ALTER TABLE team_seasons ADD COLUMN fumbles_recovered INTEGER DEFAULT 0;
ALTER TABLE team_seasons ADD COLUMN fumbles_lost INTEGER DEFAULT 0;
