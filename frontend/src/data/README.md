# 🚀 React Data Files - College Football Database

This folder contains all the recommended data files for your React college football app, optimized for performance and ease of use.

## 📁 File Overview

### **🏈 Core Team Data**
- **`fbs_teams_stats_only.json`** (0.7MB) - Complete FBS team season stats
  - 123 teams with 107+ stats each
  - Direct array access (no metadata wrapper)
  - Perfect for team comparisons and rankings

### **🎯 Specialized Analytics**  
- **`react_fbs_team_rankings.json`** - Pre-optimized team rankings
  - Key offensive and defensive stats extracted
  - Ready for leaderboards and comparisons

- **`react_fbs_conferences.json`** - Conference organization
  - Teams grouped by conference
  - Quick conference lookups

### **⚔️ Offense & Defense**
- **`fbs_offensive_stats.json`** (0.4MB) - Offensive stats only
  - Passing, rushing, scoring metrics
  - Use when you only need offensive data

- **`fbs_defensive_stats.json`** (0.4MB) - Defensive stats only  
  - Defensive yards, sacks, interceptions
  - Use when you only need defensive data

### **🚗 Drive Data (Power 5)**
- **`power5_drives_only.json`** (4.9MB) - All Power 5 drive data
  - 6,473 drives from major conferences
  - Drive-by-drive analysis ready

- **`react_power5_teams.json`** - Drives organized by team
  - Offensive/defensive drives separated
  - Easy team-specific drive analysis

- **`react_power5_efficiency.json`** - Drive efficiency stats
  - Scoring percentages and efficiency metrics
  - Ready for charts and comparisons

### **🎯 Win Probabilities & Rankings**
- **`complete_win_probabilities.json`** - Game win probabilities
  - Pregame and postgame win probabilities
  - Upset detection and game excitement

- **`team_season_summaries_clean.json`** - Season summaries & rankings
  - Win-loss records, scoring averages
  - Top 25 rankings and team performance

## 🔧 React Usage Examples

### Import Team Stats
```javascript
import teams from './data/fbs_teams_stats_only.json';

// Get top passing teams
const topPassing = teams
  .sort((a, b) => b.stats.passingYards - a.stats.passingYards)
  .slice(0, 10);
```

### Import Team Rankings
```javascript
import rankings from './data/react_fbs_team_rankings.json';

// Access pre-organized stats
Object.values(rankings).forEach(team => {
  console.log(team.team, team.offensive_stats, team.defensive_stats);
});
```

### Import Drive Data
```javascript
import drives from './data/power5_drives_only.json';

// Filter Ohio State offensive drives
const osuOffense = drives.filter(d => 
  d.offense === 'Ohio State' && d.driveResult === 'TD'
);
```

### Import Win Probabilities
```javascript
import winProbs from './data/complete_win_probabilities.json';

// Find biggest upsets
const upsets = winProbs.filter(game => 
  Math.abs(game.homePostgameWP - game.homePregameWP) > 0.7
);
```

## 📊 Performance Notes

- **Small files** (under 5MB each) - perfect for web apps
- **No metadata wrappers** on main files - clean array access
- **Pre-optimized structure** - ready for React components
- **Compressed efficiently** - 70%+ size reduction with GZIP

## 🎯 Recommended File Priority

1. **`fbs_teams_stats_only.json`** - Start here for team data
2. **`team_season_summaries_clean.json`** - For rankings and records  
3. **`react_fbs_team_rankings.json`** - For pre-built comparisons
4. **`power5_drives_only.json`** - For advanced drive analysis
5. **`complete_win_probabilities.json`** - For game excitement metrics

## 💡 Tips

- Files load instantly with modern web servers
- Use dynamic imports for large files: `const data = await import('./data/file.json')`
- Enable GZIP compression on your server for 70% smaller transfers
- Consider client-side caching for frequently accessed data

**Total API Cost: Only 16 calls (0.32% of monthly limit) for this entire database!** 🎉