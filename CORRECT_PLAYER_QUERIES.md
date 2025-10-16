# 🏈 College Football Data GraphQL API - CORRECT Query Patterns for Active Players

## ✅ SCHEMA DISCOVERY RESULTS

### Athlete Table Fields:
- `athleteTeams` - Links to team rosters by season (THIS IS THE KEY!)
- `teamId` - Current/most recent team
- `position` - Relationship object (not a string)
- `positionId` - Position ID number

### GamePlayerStat Table Fields:
- `gameTeam` - Links to the game/team combination (not `game`)
- `athlete` - Links to athlete
- `playerStatCategory` - The category (passing, rushing, receiving, etc.)
- `playerStatType` - Specific stat type
- `stat` - The numeric value

## 🎯 CORRECT APPROACH - Get Active 2024 Players

### Method 1: Using athleteTeams relationship (RECOMMENDED)

```graphql
query GetActivePlayers($teamId: Int!, $season: Int!) {
  athlete(
    where: {
      athleteTeams: {
        teamId: {_eq: $teamId}
        year: {_eq: $season}
      }
    }
  ) {
    id
    name
    firstName
    lastName
    jersey
    position {
      abbreviation
    }
  }
}
```

**Variables:**
```json
{
  "teamId": 356,
  "season": 2024
}
```

This filters athletes to only those who have an `athleteTeams` entry for the specified team and season!

### Method 2: Get team roster then stats

**Step 1: Get Active Roster for 2024**
```graphql
query GetTeamRoster($teamId: Int!, $season: Int!) {
  athleteTeam(
    where: {
      teamId: {_eq: $teamId}
      year: {_eq: $season}
    }
  ) {
    athleteId
    year
    teamId
    athlete {
      id
      name
      firstName
      lastName
      jersey
      position {
        abbreviation
      }
    }
  }
}
```

**Step 2: Get Stats for Those Players**
```graphql
query GetPlayerStats($playerIds: [bigint!], $season: Int!) {
  gamePlayerStat(
    where: {
      athleteId: {_in: $playerIds}
      gameTeam: {
        game: {
          season: {_eq: $season}
        }
      }
      playerStatCategory: {
        name: {_eq: "receiving"}
      }
    }
  ) {
    athleteId
    stat
    playerStatType {
      name
    }
    playerStatCategory {
      name
    }
    gameTeam {
      game {
        season
        week
      }
    }
  }
}
```

## 🔑 KEY CORRECTIONS

### ❌ WRONG (from your original query):
```graphql
gamePlayerStats: {  # This field doesn't exist!
  _exists: {
    _where: { 
      year: {_eq: $year}
    }
  }
}
```

### ✅ CORRECT:
```graphql
athleteTeams: {  # This is the correct field!
  teamId: {_eq: $teamId}
  year: {_eq: $season}
}
```

## 📋 COMPLETE WORKING EXAMPLE

### Get Illinois WRs for 2024 with Receiving Stats

```graphql
query GetIllinoisWRsWithStats {
  # Step 1: Get 2024 roster
  athleteTeam(
    where: {
      teamId: {_eq: 356}
      year: {_eq: 2024}
    }
  ) {
    athlete {
      id
      name
      jersey
      position {
        abbreviation
      }
    }
  }
}
```

Then for each WR found, query their stats:

```graphql
query GetWRStats($athleteIds: [bigint!]) {
  gamePlayerStat(
    where: {
      athleteId: {_in: $athleteIds}
      playerStatCategory: {
        name: {_eq: "receiving"}
      }
      gameTeam: {
        game: {
          season: {_eq: 2024}
        }
      }
    }
  ) {
    athleteId
    stat
    playerStatType {
      name
    }
    gameTeam {
      game {
        week
      }
    }
  }
}
```

## 💡 IMPLEMENTATION TIPS

1. **Use `athleteTeam` table as the roster source** - It has year field for filtering
2. **Use `athleteId` not `playerId`** in gamePlayerStat
3. **Position is an object** - use `position { abbreviation }` not `position` as string
4. **Categories are objects** - use `playerStatCategory { name }` with filters
5. **Always specify season** - filter through `gameTeam { game { season } }`

## 🎯 PRODUCTION QUERY PATTERN

```python
# 1. Get active roster
roster_query = """
query GetActiveRoster($teamId: Int!, $season: Int!) {
  athleteTeam(
    where: {
      teamId: {_eq: $teamId}
      year: {_eq: $season}
    }
  ) {
    athleteId
    athlete {
      name
      firstName
      lastName
      jersey
      position { abbreviation }
    }
  }
}
"""

# 2. Get stats for those athletes
stats_query = """
query GetPlayerStats($athleteIds: [bigint!], $season: Int!, $category: String!) {
  gamePlayerStat(
    where: {
      athleteId: {_in: $athleteIds}
      gameTeam: {
        game: { season: {_eq: $season} }
      }
      playerStatCategory: {
        name: {_eq: $category}
      }
    }
  ) {
    athleteId
    stat
    playerStatType { name }
    gameTeam {
      game { week }
    }
  }
}
"""

# 3. Aggregate stats in Python
# Group by athleteId, sum stats by type
```

## ✅ THIS WILL GET YOU ACTIVE 2024 PLAYERS ONLY!

The key is using `athleteTeam` with `year` filter, not trying to use `gamePlayerStats` which doesn't exist as a relationship field on `athlete`.
