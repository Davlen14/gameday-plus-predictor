# 🏈 Matchup Cards Implementation - Detailed Prompt for AI

## Overview
Implement 4 sophisticated matchup visualization cards in the PlayerPropsPanel component to show key offensive vs defensive battles.

---

## 🎯 Implementation Requirements

### **Location**: 
`/Users/davlenswain/Desktop/Gameday_Graphql_Model/frontend/src/components/figma/PlayerPropsPanel.tsx`

### **Current State**:
- Component already has WR vs DB matchup cards implemented
- All player data available with efficiency scores
- Players categorized by position: QB, RB, WR, TE, DB, LB, DL
- Each player has: name, position, team, efficiency score, stats, headshot_url

---

## 🎨 4 Matchup Card Types to Implement

### **1. WR vs DB Matchup** ✅ (Already Implemented)
- Keep existing implementation
- Side-by-side split cards showing WR on left, DB on right
- Shows efficiency advantage calculation

### **2. RB vs LB Matchup** 🏃‍♂️⚔️🛡️
**Design**: Side-by-side split card (similar to WR vs DB)

**Left Side** - Running Back:
- Player headshot (transparent)
- Name, position badge (RB)
- Team name
- Efficiency score badge (top right)
- Primary stat: Rush Yards (large display)
- Key metrics grid: Attempts, TDs, Receptions, YPC

**Right Side** - Linebacker:
- Player headshot (transparent)  
- Name, position badge (LB)
- Team name
- Efficiency score badge (top right)
- Primary stat: Tackles (large display)
- Key metrics grid: Tackles, Sacks, TFLs, Type

**Center Divider**:
- Vertical gradient line
- "RUN DEFENSE BATTLE" label
- Efficiency advantage: "RB +XXX" or "LB +XXX"
- Use green for RB advantage, red for LB advantage

**Matchup Logic**:
- Match highest efficiency RB from Team A vs highest efficiency LB from Team B
- If multiple RBs/LBs, create multiple matchup cards
- Show top 2 RB vs LB matchups per game

---

### **3. TE vs LB Matchup** 🎯⚔️🛡️
**Design**: Side-by-side split card (similar to WR vs DB)

**Left Side** - Tight End:
- Player headshot (transparent)
- Name, position badge (TE)
- Team name
- Efficiency score badge (top right)
- Primary stat: Receiving Yards (large display)
- Key metrics grid: Receptions, Targets, TDs, YPR

**Right Side** - Linebacker:
- Player headshot (transparent)
- Name, position badge (LB)
- Team name
- Efficiency score badge (top right)
- Primary stat: Tackles (large display)
- Key metrics grid: Tackles, Sacks, Coverage, Type

**Center Divider**:
- Vertical gradient line
- "MIDDLE FIELD BATTLE" label
- Efficiency advantage: "TE +XXX" or "LB +XXX"
- Use green for TE advantage, red for LB advantage

**Matchup Logic**:
- Match highest efficiency TE from Team A vs highest efficiency LB from Team B
- Show top 1-2 TE vs LB matchups per game

---

### **4. QB vs Defensive Front (SPECIAL POLAR CHART)** 🎯💥⚡
**Design**: Unique circular/polar visualization - **This is the coolest one!**

**Center Circle** - Quarterback:
- Large circular container (150-200px diameter)
- QB headshot in center
- Efficiency score as large number overlaid
- QB name below headshot
- Team logo watermark (very subtle)
- Passing yards stat below name
- Glowing effect around circle (team color gradient)

**Surrounding Defense** - Polar/Radial Layout:
- 4-6 defensive players arranged in circle around QB
- Mix of DL (defensive linemen) and LB (linebackers)
- Each defender positioned at angles: 0°, 60°, 120°, 180°, 240°, 300°
- **Each defender card contains**:
  - Small circular headshot (60-80px)
  - Position badge (DL or LB)
  - Efficiency score
  - Primary stat (Sacks for DL, Tackles for LB)
  - Connected to center with subtle line/beam

**Visual Elements**:
- Gradient beams connecting defenders to QB (opacity based on efficiency)
- Background: dark with subtle grid/radar pattern
- Title at top: "POCKET PRESSURE ANALYSIS"
- Subtitle: "QB vs Defensive Front"
- Overall pressure score: Average of all defender efficiency scores
- Color coding:
  - Red beams: Elite defenders (250+ efficiency)
  - Yellow beams: High defenders (200-249 efficiency)
  - Green beams: Medium defenders (150-199 efficiency)

**Layout Structure**:
```
         [Top Defender DL]
              |
    [Left DL] --- [QB Center] --- [Right DL]
              |
       [Bottom LB] [Bottom LB]
```

**Matchup Logic**:
- Show QB from Team A
- Surround with top 4-6 defensive players from Team B (mix of DL and LB)
- Sort defenders by efficiency score
- Create 2 of these cards (one for each team's QB)

**Animation Ideas** (optional):
- Pulse effect on high-threat defenders
- Subtle rotation of defender positions
- Glow intensity based on defender efficiency

---

## 📊 Data Structure Reference

### Available Player Data:
```typescript
interface Player {
  name: string;
  player_name?: string;
  position: 'QB' | 'RB' | 'WR' | 'TE' | 'DB' | 'LB' | 'DL';
  position_type?: string; // For defense: 'DB', 'LB', 'DL'
  team: string;
  headshot_url?: string;
  comprehensive_efficiency_score: number;
  
  // QB Stats
  passing_stats?: {
    passing_yards: number;
    completions: number;
    attempts: number;
    passing_touchdowns: number;
    interceptions: number;
  };
  
  // RB Stats
  rushing_yards?: number;
  rushing_attempts?: number;
  rushing_touchdowns?: number;
  receptions?: number;
  yards_per_carry?: number;
  
  // WR/TE Stats
  receiving_yards?: number;
  receptions?: number;
  targets?: number;
  receiving_touchdowns?: number;
  yards_per_reception?: number;
  
  // Defense Stats
  tackles?: number;
  sacks?: number;
  tackles_for_loss?: number;
  interceptions?: number;
}
```

### Accessing Player Data:
```typescript
const homePlayers = predictionData?.enhanced_player_analysis?.home_players;
const awayPlayers = predictionData?.enhanced_player_analysis?.away_players;

// Available arrays:
homePlayers.qbs // Array of QBs
homePlayers.rbs // Array of RBs
homePlayers.wrs // Array of WRs
homePlayers.tes // Array of TEs
homePlayers.defense // Array of DBs, LBs, DLs (check position_type)

// Filter by position_type
const lbs = homePlayers.defense.filter(d => d.position_type === 'LB');
const dls = homePlayers.defense.filter(d => d.position_type === 'DL');
```

---

## 🎨 Styling Guidelines

### Use Existing Design System:
- **Glassmorphism**: `bg-white/5`, `backdrop-blur-sm`, `border border-white/10`
- **Compact spacing**: `p-3`, `gap-2`, `text-xs/text-sm`
- **Analytical colors**: Gray-based with accent colors for metrics
- **Icons**: Use lucide-react (Activity, TrendingUp, Shield, Target, Zap, AlertTriangle)
- **Gradients**: 
  - Green advantage: `from-green-500/20 to-green-600/20`
  - Red advantage: `from-red-500/20 to-red-600/20`
  - Team colors: Use team watermarks

### Card Dimensions:
- **Side-by-side cards**: Width auto (flex), Height ~250-300px
- **QB Polar chart**: Width 400-500px, Height 400-500px (square)
- **Responsive**: Use `grid grid-cols-1 md:grid-cols-2` for layout

---

## 📍 Component Structure

### Section Layout:
```tsx
// In PlayerPropsPanel component:

1. Threat Level Summary (existing)
2. Key Matchups Section (NEW):
   - WR vs DB cards (existing)
   - RB vs LB cards (NEW)
   - TE vs LB cards (NEW)  
   - QB vs Defense polar charts (NEW)
3. All Players Grid (existing)
```

### New Components to Create:

```tsx
// RB vs LB Matchup Card
const RBvsLBMatchup = ({ rb, lb, homeTeam, awayTeam }) => { ... }

// TE vs LB Matchup Card
const TEvsLBMatchup = ({ te, lb, homeTeam, awayTeam }) => { ... }

// QB vs Defense Polar Chart
const QBPressureChart = ({ qb, defenders, opposingTeam }) => { ... }
```

---

## 🔧 Implementation Steps

1. **Create RBvsLBMatchup component** (similar to existing MatchupCard)
2. **Create TEvsLBMatchup component** (similar to existing MatchupCard)
3. **Create QBPressureChart component** (unique polar/radial design)
4. **Add matchup generation logic**:
   - Find best RB vs LB pairs
   - Find best TE vs LB pairs
   - Find QBs and their opposing defensive fronts
5. **Update main component render** to display all 4 matchup types
6. **Style with glassmorphism** and analytical design
7. **Test with real game data** (Ohio State vs Indiana, Texas Tech vs BYU, etc.)

---

## 🎯 Success Criteria

✅ All 4 matchup types display correctly  
✅ QB polar chart shows defenders in circular layout around QB  
✅ Efficiency advantages calculate correctly  
✅ Responsive design works on all screen sizes  
✅ Compact, analytical styling matches existing components  
✅ All player data displays (headshots, stats, efficiency scores)  
✅ Proper color coding for advantages (green/yellow/red)  
✅ Smooth integration with existing PlayerPropsPanel

---

## 💡 Visual References

### QB Polar Chart Layout ASCII:
```
┌─────────────────────────────────────┐
│   POCKET PRESSURE ANALYSIS          │
│   QB vs Defensive Front             │
├─────────────────────────────────────┤
│                                     │
│        [DL #90]                     │
│          Eff: 90                    │
│            ╲                        │
│   [LB #86]  ╲  [DL #84]            │
│   Eff: 86    ╲ Eff: 84             │
│       ╲       ╲ ╱                   │
│        ╲   [🏈QB]   ╱               │
│         ╲  Morton  ╱                │
│          ╲ 241   ╱                  │
│           ╲    ╱                    │
│   [LB #84]  ╲ ╱  [LB #76]          │
│   Eff: 84    ╳   Eff: 76           │
│             ╱                       │
│        [DL #70]                     │
│        Eff: 70                      │
│                                     │
│   Overall Pressure: 81.7            │
└─────────────────────────────────────┘
```

### Side-by-Side Matchup Layout:
```
┌──────────────────┬─────────────────┐
│  [RB Headshot]   │  [LB Headshot]  │
│  Cameron Dickey  │  Jack Kelly     │
│  RB · Texas Tech │  LB · BYU       │
│  Eff: 437        │  Eff: 84        │
│                  │                 │
│  Rush Yards      │  Tackles        │
│     958          │     77          │
│                  │                 │
│  Att: 170        │  Sacks: 7       │
│  TDs: 13         │  TFLs: 12       │
│  Rec: 16    ────►├◄──── RUN BATTLE │
│  YPC: 5.6        │  Type: LB       │
│                  │                 │
│   RB ADVANTAGE: +353               │
└──────────────────┴─────────────────┘
```

---

## 🚀 Additional Enhancements (Optional)

- Add tooltips on hover showing full player stats
- Add click to expand full player profile
- Add animation when matchup cards appear
- Add "Impact Score" calculation (efficiency differential × position weight)
- Add historical matchup data if available
- Add injury/status indicators
- Add recent performance trends (last 3 games)

---

## 📝 Notes

- Maintain consistent spacing with existing PlayerCard components (p-3, gap-2)
- Ensure all headshots use ImageWithFallback component
- All efficiency scores should display as integers (`.toFixed(0)`)
- Keep QB polar chart as the centerpiece - make it visually striking
- Test with games that have incomplete data (missing TEs, etc.)
- Gracefully handle cases where position matchups don't exist

---

**File to modify**: `/Users/davlenswain/Desktop/Gameday_Graphql_Model/frontend/src/components/figma/PlayerPropsPanel.tsx`

**Framework**: React + TypeScript + Tailwind CSS  
**Icons**: lucide-react  
**Existing pattern**: Follow compact analytical style from recent PlayerCard updates
