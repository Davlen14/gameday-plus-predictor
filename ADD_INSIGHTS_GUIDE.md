# Component Insights Addition Guide

## Components Already Updated ✅
- EPAComparison.tsx
- MarketComparison.tsx  
- ConfidenceSection.tsx

## Pattern to Follow for Remaining Components

### 1. Add Import
```typescript
import { InsightBox } from './InsightBox';
```

### 2. Add InsightBox Before Closing </GlassCard>

## SituationalPerformance.tsx
Add before final `</GlassCard>`:
```tsx
<InsightBox
  whatItMeans="Situational performance shows how teams perform in critical moments: 3rd downs (sustaining drives), red zone (scoring TDs vs FGs), and goal-to-go (punch-it-in ability). These situations determine game outcomes more than total yardage."
  whyItMatters="Teams that convert 3rd downs control the clock and wear down defenses. Red zone efficiency (50%+ TD rate) is the difference between 28-point and 21-point performances. Goal-to-go success rate predicts short-yardage dominance."
  whoHasEdge={{
    team: "[Calculate from data - team with higher 3rd down%]",
    reason: "[Dynamic based on biggest gaps: '3rd down edge of X%, red zone TD rate Y% higher, dominates short yardage Z% better']",
    magnitude: "[Calculate: >15% gap = major, >10% = significant, >5% = moderate, else small]"
  }}
  keyDifferences={[
    "3rd down conversion: [X%] vs [Y%] ([Z]% advantage)",
    "Red zone TD rate: [X%] vs [Y%] ([Z] more TDs per 10 red zone trips)",
    "Goal-to-go success: [X%] vs [Y%] (short yardage domination)"
  ]}
/>
```

## FieldPositionMetrics.tsx
```tsx
<InsightBox
  whatItMeans="Starting field position is 'free yards' - teams starting at their 35 vs their 25 gain 10 extra yards per drive without running a play. This compounds over 12+ drives per game into significant scoring advantages."
  whyItMatters="Every 5 yards of field position advantage equals roughly 0.5 points per game. A 10-yard edge (starting at 32 vs 22) translates to 1+ point per game, or 7-10 points over a season. Elite field position teams (avg 30+ yard line) score 3-5 more PPG."
  whoHasEdge={{
    team: "[Team with better avg starting position]",
    reason: "[X] averages [Y] yards better starting field position ([Z] yard line vs [A] yard line). Over [B] drives, that's [C] extra yards before running a play - equivalent to [D] extra first downs.",
    magnitude: "[>10 yards = major, >7 = significant, >4 = moderate, else small]"
  }}
  keyDifferences={[
    "Avg start position: [X yard line] vs [Y yard line] ([Z] yard advantage)",
    "Explosive play rate: [X%] vs [Y%] (determines field flip ability)",
    "Punt/kick return avg: [X] vs [Y] yards (hidden yards edge)"
  ]}
/>
```

## KeyPlayerImpact.tsx
```tsx
<InsightBox
  whatItMeans="Individual player efficiency scores quantify how much better/worse a team performs with that player. QB efficiency combines completion %, yards/attempt, TD rate, and INT avoidance. WR efficiency measures targets converted to yards and TDs relative to team average."
  whyItMatters="Elite QB play (efficiency >75) wins 65%+ of games regardless of team talent. A 20-point QB efficiency gap typically translates to 2-3 point spread advantage. Top WRs (efficiency >70) create mismatches that force defenses into predictable schemes."
  whoHasEdge={{
    team: "[Team with higher combined QB+WR efficiency]",
    reason: "[Team]'s QB efficiency of [X] vs [Y] creates a [Z]-point advantage. Their top WR trio ([A], [B], [C]) averages [D] efficiency vs opponents' [E], forcing [F] coverage adjustments per drive.",
    magnitude: "[>20 QB gap = major, >15 = significant, >10 = moderate, else small]"
  }}
  keyDifferences={[
    "QB efficiency: [X] vs [Y] ([Z]-point spread impact)",
    "WR1 efficiency: [A] vs [B] ([C] receiving yards advantage per game)",
    "Depth advantage: [X] has [Y] WRs >65 efficiency, opponent has [Z]"
  ]}
/>
```

## DifferentialAnalysis.tsx
```tsx
<InsightBox
  whatItMeans="Differentials compare teams head-to-head across all categories. Positive differentials show where one team has statistical advantages. The magnitude of gaps determines whether advantages are noise (<5%) or meaningful (>10%)."
  whyItMatters="Teams with 3+ major differentials (>15% gaps) in their favor win 75%+ of matchups. Offensive + defensive differentials compounding (both >10%) create overwhelming advantages. Single massive differential (>25%) can override multiple small edges."
  whoHasEdge={{
    team: "[Team with more positive differentials >10%]",
    reason: "[Team] holds [X] major advantages (>15% gaps) vs [Y] for opponent. Combined differential strength: [Z] points across offense ([A]), defense ([B]), and special teams ([C]). Largest gap: [D] in [category] ([E]% difference).",
    magnitude: "[>3 major diffs = major, 2-3 = significant, 1-2 = moderate, 0-1 = small]"
  }}
  keyDifferences={[
    "Biggest offensive gap: [X] in [category] ([Y]% / [Z] points per game)",
    "Biggest defensive gap: [A] in [category] ([B]% / [C] points allowed)",
    "Net advantage: [X] holds [Y] of top 5 differentials, [Z]-point edge"
  ]}
/>
```

## AdvancedMetrics.tsx
```tsx
<InsightBox
  whatItMeans="Success rate (gaining 50%+ of yards needed on 1st/2nd down, 100% on 3rd/4th) measures consistency. Explosiveness tracks plays gaining 10+ yards (passing) or 8+ yards (rushing). Power success = short yardage conversion (3rd/4th & 1-2)."
  whyItMatters="Success rate >45% = efficient offense that sustains drives. Explosiveness >15% = big-play ability that scores quickly. Teams with BOTH (45%+ success, 15%+ explosive) average 35+ PPG. Power success >70% wins 4th quarter tight games."
  whoHasEdge={{
    team: "[Team with higher combined metric score]",
    reason: "[Team] combines [X]% success rate with [Y]% explosiveness, creating a balanced attack. Their [Z]% power success dominates short yardage, while opponent's [A]% ranks [B]. Total offensive efficiency edge: [C] points per game.",
    magnitude: "[>8% success + >5% explosive = major, >5% + >3% = significant, else moderate/small]"
  }}
  keyDifferences={[
    "Success rate: [X]% vs [Y]% ([Z]% more consistent drives)",
    "Explosiveness: [A]% vs [B]% ([C] more big plays per game)",
    "Power success: [D]% vs [E]% ([F]% edge in short yardage)"
  ]}
/>
```

## DriveEfficiency.tsx
```tsx
<InsightBox
  whatItMeans="Drive efficiency combines scoring %, explosive plays, methodical drives, 3&outs, and red zone success. Scoring drives % = % of possessions ending in points. Explosive drives have 3+ plays of 15+ yards. Methodical drives = 10+ plays grinding defenses."
  whyItMatters="Teams scoring on 40%+ of drives average 30+ PPG. Explosive drives (fast scores) preserve defense energy. Methodical drives (8+ minutes) dominate time of possession and wear down opponents. Limiting opponent 3&outs to <20% controls the game."
  whoHasEdge={{
    team: "[Team with higher scoring drive %]",
    reason: "[Team] scores on [X]% of drives vs opponent's [Y]%, a [Z]-point per game advantage. Their [A] explosive drives per game vs [B] creates quick-strike ability, while [C] methodical drives per game controls clock [D] minutes more.",
    magnitude: "[>15% scoring gap = major, >10% = significant, >5% = moderate, else small]"
  }}
  keyDifferences={[
    "Scoring drive %: [X]% vs [Y]% ([Z] more scoring possessions per game)",
    "Explosive drives: [A] vs [B] per game ([C] more quick-strike TDs)",
    "3 & out rate: [X]% vs [Y]% ([Z]% better at sustaining drives)"
  ]}
/>
```

## Implementation Priority
1. **Situational Performance** (3rd down/red zone = game winners)
2. **Key Player Impact** (QBs/WRs drive outcomes)
3. **Differential Analysis** (shows who's actually better)
4. **Advanced Metrics** (success rate = NFL's #1 predictor)
5. **Field Position** (hidden yards matter)
6. **Drive Efficiency** (tells full offensive story)

## Notes
- Replace placeholders `[X]`, `[Y]`, `[Team]` with actual data extraction from `predictionData`
- Magnitude thresholds are based on historical win rate correlations
- Key differences should highlight the 2-3 biggest gaps users should care about
