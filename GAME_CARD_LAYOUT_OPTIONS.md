# 🏈 Game Card Header Layout Options

## Current State Analysis
**What's Working:**
- Watermark logos at z-index: 0 (subtle background)
- Orbitron font for team abbreviations
- Rank badges with silver gradient
- Sharp play indicators

**Issues to Fix:**
- Teams not clearly separated (away left, home right)
- Game time placement unclear
- Vertical stacking needs optimization
- VS divider needs better centering

---

## 🎨 OPTION A: Vertical Stack with Time at Bottom

### Visual Hierarchy
```
┌─────────────────────────────────────┐
│  [watermark logos in background]   │
│                                     │
│  RANK  🏈   HOME   (12-0)   RANK   │
│       BUCKEYES                      │
│                                     │
│            VS                       │
│                                     │
│  RANK  🏈  INDIANA  (12-0)   RANK   │
│        HOOSIERS                     │
│                                     │
│  ⏰ Saturday 8:00 PM  🔥 Sharp      │
└─────────────────────────────────────┘
```

### CSS Implementation
```css
.ev-game-header-optionA {
  position: relative;
  overflow: hidden;
  padding: 20px 16px 12px;
  display: flex;
  flex-direction: column;
  gap: 0;
}

/* Watermark Background Logos */
.ev-header-watermark-left {
  position: absolute;
  left: -30px;
  top: 50%;
  transform: translateY(-50%) rotate(-5deg);
  width: 140px;
  height: 140px;
  opacity: 0.06;
  filter: brightness(1.3) sepia(0.8) saturate(2);
  pointer-events: none;
  z-index: 0;
}

.ev-header-watermark-right {
  position: absolute;
  right: -30px;
  top: 50%;
  transform: translateY(-50%) rotate(5deg);
  width: 140px;
  height: 140px;
  opacity: 0.06;
  filter: brightness(1.3) sepia(0.8) saturate(2);
  pointer-events: none;
  z-index: 0;
}

/* Team Container - Vertical Stack */
.ev-teams-vertical-stack {
  display: flex;
  flex-direction: column;
  gap: 16px;
  position: relative;
  z-index: 2;
}

/* Individual Team Row */
.ev-team-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.ev-team-left {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
}

.ev-team-right {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  justify-content: flex-end;
}

/* Team Info Column */
.ev-team-info-stack {
  display: flex;
  flex-direction: column;
  gap: 2px;
  align-items: flex-start;
}

.ev-team-info-stack.right {
  align-items: flex-end;
}

/* Team Abbreviation */
.ev-team-abbr {
  font-family: 'Orbitron', monospace;
  font-size: 15px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.95);
  letter-spacing: 1.5px;
  text-transform: uppercase;
  line-height: 1;
}

/* Record */
.ev-team-record {
  font-size: 11px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.45);
  letter-spacing: 0.5px;
  line-height: 1;
}

/* Team Logo */
.ev-team-logo-main {
  width: 32px;
  height: 32px;
  object-fit: contain;
  filter: drop-shadow(0 3px 6px rgba(0, 0, 0, 0.4));
  flex-shrink: 0;
}

/* Rank Badge */
.ev-rank-badge {
  min-width: 28px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 800;
  font-family: 'Orbitron', monospace;
  background: linear-gradient(135deg, #C0C0C0 0%, #E5E5E5 25%, #A9A9A9 50%, #D3D3D3 75%, #808080 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 0.5px;
  padding: 0 4px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 4px;
  background-color: rgba(255, 255, 255, 0.05);
  flex-shrink: 0;
}

/* VS Divider - Centered */
.ev-vs-divider {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 2;
  margin: 4px 0;
}

.ev-vs-text {
  font-size: 12px;
  font-weight: 800;
  font-family: 'Orbitron', monospace;
  color: rgba(255, 255, 255, 0.25);
  letter-spacing: 3px;
  padding: 0 16px;
  position: relative;
}

.ev-vs-text::before,
.ev-vs-text::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 40px;
  height: 1px;
  background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.15), transparent);
}

.ev-vs-text::before {
  right: 100%;
  margin-right: 8px;
}

.ev-vs-text::after {
  left: 100%;
  margin-left: 8px;
}

/* Game Meta Footer */
.ev-game-meta-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 12px;
  padding-top: 10px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  position: relative;
  z-index: 2;
}

.ev-game-time-display {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.6);
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.ev-time-icon {
  width: 12px;
  height: 12px;
  opacity: 0.5;
}

.ev-sharp-badge {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 3px 10px;
  background: rgba(28, 221, 144, 0.08);
  border: 1px solid rgba(28, 221, 144, 0.25);
  border-radius: 12px;
  font-size: 9px;
  font-weight: 800;
  font-family: 'Orbitron', monospace;
  color: rgb(28, 221, 144);
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

.ev-sharp-icon {
  width: 10px;
  height: 10px;
}
```

### Pros
- ✅ Clear vertical separation of teams
- ✅ Time info doesn't interfere with team data
- ✅ Very readable in compact space
- ✅ Balanced weight distribution

### Cons
- ⚠️ Slightly taller card height
- ⚠️ May feel traditional

---

## 🎨 OPTION B: Horizontal with Time in Top-Right Corner

### Visual Hierarchy
```
┌─────────────────────────────────────┐
│  [watermark logos in background]   │
│                          ⏰ SAT 8PM │
│  #1  🏈   @   #2  🏈            🔥 │
│     OSU  VS  IND                    │
│    12-0     12-0                    │
└─────────────────────────────────────┘
```

### CSS Implementation
```css
.ev-game-header-optionB {
  position: relative;
  overflow: hidden;
  padding: 16px;
  display: grid;
  grid-template-areas:
    "time time"
    "teams teams";
  grid-template-rows: auto 1fr;
  gap: 12px;
  min-height: 100px;
}

/* Watermark Logos - Same as Option A */
.ev-header-watermark-left,
.ev-header-watermark-right {
  /* Same CSS as Option A */
}

/* Time Header Row */
.ev-time-header-row {
  grid-area: time;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  z-index: 2;
}

.ev-time-display-inline {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 10px;
  font-weight: 800;
  font-family: 'Orbitron', monospace;
  color: rgba(255, 255, 255, 0.5);
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-left: auto;
}

.ev-sharp-inline {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 2px 8px;
  background: rgba(28, 221, 144, 0.08);
  border: 1px solid rgba(28, 221, 144, 0.25);
  border-radius: 10px;
  font-size: 8px;
  font-weight: 800;
  font-family: 'Orbitron', monospace;
  color: rgb(28, 221, 144);
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

/* Teams Horizontal Layout */
.ev-teams-horizontal {
  grid-area: teams;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  position: relative;
  z-index: 2;
}

/* Away Team (Left) */
.ev-away-team-block {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
  flex: 1;
}

.ev-away-team-top {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Home Team (Right) */
.ev-home-team-block {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
  flex: 1;
}

.ev-home-team-top {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* VS Divider - Compact Centered */
.ev-vs-divider-compact {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  flex-shrink: 0;
  padding: 0 12px;
}

.ev-at-symbol {
  font-size: 10px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.3);
  letter-spacing: 1px;
}

.ev-vs-text-small {
  font-size: 11px;
  font-weight: 900;
  font-family: 'Orbitron', monospace;
  color: rgba(255, 255, 255, 0.3);
  letter-spacing: 2px;
}

/* Team Components - Same base as Option A but compact */
.ev-team-abbr-compact {
  font-family: 'Orbitron', monospace;
  font-size: 14px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.95);
  letter-spacing: 1.2px;
  text-transform: uppercase;
  line-height: 1;
}

.ev-team-record-compact {
  font-size: 10px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.4);
  letter-spacing: 0.3px;
}

.ev-team-logo-compact {
  width: 28px;
  height: 28px;
  object-fit: contain;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.4));
}

.ev-rank-badge-compact {
  min-width: 24px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 800;
  font-family: 'Orbitron', monospace;
  background: linear-gradient(135deg, #C0C0C0, #E5E5E5, #A9A9A9, #D3D3D3, #808080);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 0.5px;
  padding: 0 4px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 3px;
  background-color: rgba(255, 255, 255, 0.04);
}
```

### Pros
- ✅ Most compact height (fits more in viewport)
- ✅ Modern horizontal layout
- ✅ Time clearly separated
- ✅ Sharp indicator immediately visible

### Cons
- ⚠️ Slightly wider requirement
- ⚠️ Teams less visually separated

---

## 🎨 OPTION C: RECOMMENDED - Modern Sports Betting UI (Hybrid Approach)

### Visual Hierarchy
```
┌─────────────────────────────────────┐
│  [watermark logos in background]   │
│                                     │
│  #1 🏈 OHIO STATE    VS    #2 🏈    │
│      (12-0)                 (12-0)  │
│                 INDIANA             │
│  ────────────────────────────────   │
│  ⏰ SAT 8:00 PM  │  🔥 SHARP PLAY  │
└─────────────────────────────────────┘
```

### CSS Implementation
```css
.ev-game-header-optionC {
  position: relative;
  overflow: hidden;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: rgba(0, 0, 0, 0.15);
  border-radius: 8px 8px 0 0;
}

/* Watermark Logos - Enhanced with blur */
.ev-header-watermark-left-enhanced {
  position: absolute;
  left: -40px;
  top: 50%;
  transform: translateY(-50%) scale(1.1);
  width: 150px;
  height: 150px;
  opacity: 0.08;
  filter: brightness(1.4) blur(1px) sepia(0.5) saturate(2);
  pointer-events: none;
  z-index: 0;
  transition: transform 0.5s ease, opacity 0.5s ease;
}

.ev-header-watermark-right-enhanced {
  position: absolute;
  right: -40px;
  top: 50%;
  transform: translateY(-50%) scale(1.1);
  width: 150px;
  height: 150px;
  opacity: 0.08;
  filter: brightness(1.4) blur(1px) sepia(0.5) saturate(2);
  pointer-events: none;
  z-index: 0;
  transition: transform 0.5s ease, opacity 0.5s ease;
}

.ev-game-card:hover .ev-header-watermark-left-enhanced {
  transform: translateY(-50%) scale(1.15);
  opacity: 0.12;
}

.ev-game-card:hover .ev-header-watermark-right-enhanced {
  transform: translateY(-50%) scale(1.15);
  opacity: 0.12;
}

/* Main Matchup Row */
.ev-matchup-main {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  position: relative;
  z-index: 2;
}

/* Team Block - Away (Left) */
.ev-team-block-away {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  position: relative;
}

/* Rank Badge - Enhanced */
.ev-rank-pro {
  position: relative;
  min-width: 26px;
  height: 26px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 900;
  font-family: 'Orbitron', monospace;
  letter-spacing: 0.3px;
  background: linear-gradient(135deg, 
    #F5F5F5 0%, 
    #E8E8E8 20%, 
    #D3D3D3 40%, 
    #C0C0C0 60%, 
    #A8A8A8 80%, 
    #909090 100%
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  border: 1.5px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  background-color: rgba(255, 255, 255, 0.06);
  box-shadow: 
    0 2px 8px rgba(0, 0, 0, 0.3),
    inset 0 1px 2px rgba(255, 255, 255, 0.1);
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.ev-rank-pro:hover {
  transform: translateY(-1px);
  box-shadow: 
    0 4px 12px rgba(0, 0, 0, 0.4),
    inset 0 1px 2px rgba(255, 255, 255, 0.15);
}

/* Team Logo - Enhanced */
.ev-team-logo-pro {
  width: 36px;
  height: 36px;
  object-fit: contain;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.5));
  flex-shrink: 0;
  transition: transform 0.3s ease;
}

.ev-game-card:hover .ev-team-logo-pro {
  transform: scale(1.05);
}

/* Team Info Column */
.ev-team-info-pro {
  display: flex;
  flex-direction: column;
  gap: 3px;
  align-items: flex-start;
}

.ev-team-info-pro.home {
  align-items: flex-end;
}

/* Team Name - Enhanced Orbitron */
.ev-team-name-pro {
  font-family: 'Orbitron', monospace;
  font-size: 16px;
  font-weight: 800;
  color: rgba(255, 255, 255, 0.98);
  letter-spacing: 2px;
  text-transform: uppercase;
  line-height: 1;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.6);
  transition: color 0.3s ease;
}

.ev-game-card:hover .ev-team-name-pro {
  color: rgba(255, 255, 255, 1);
  text-shadow: 0 2px 12px rgba(204, 0, 28, 0.3);
}

/* Record - Enhanced */
.ev-team-record-pro {
  font-size: 11px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.5);
  letter-spacing: 0.8px;
  line-height: 1;
  font-family: 'Orbitron', monospace;
}

/* Team Block - Home (Right) */
.ev-team-block-home {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  justify-content: flex-end;
  position: relative;
}

/* VS Divider - Enhanced with Pulse */
.ev-vs-divider-pro {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  padding: 0 20px;
  flex-shrink: 0;
}

.ev-vs-text-pro {
  font-size: 13px;
  font-weight: 900;
  font-family: 'Orbitron', monospace;
  color: rgba(255, 255, 255, 0.35);
  letter-spacing: 4px;
  position: relative;
  z-index: 1;
  transition: all 0.3s ease;
}

.ev-game-card:hover .ev-vs-text-pro {
  color: rgba(204, 0, 28, 0.6);
  letter-spacing: 5px;
  text-shadow: 0 0 10px rgba(204, 0, 28, 0.3);
}

.ev-vs-text-pro::before,
.ev-vs-text-pro::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 30px;
  height: 1px;
  background: linear-gradient(
    to right, 
    transparent, 
    rgba(255, 255, 255, 0.2), 
    transparent
  );
  transition: all 0.3s ease;
}

.ev-vs-text-pro::before {
  right: calc(100% + 6px);
}

.ev-vs-text-pro::after {
  left: calc(100% + 6px);
}

.ev-game-card:hover .ev-vs-text-pro::before,
.ev-game-card:hover .ev-vs-text-pro::after {
  background: linear-gradient(
    to right, 
    transparent, 
    rgba(204, 0, 28, 0.4), 
    transparent
  );
  width: 35px;
}

/* Game Meta Bar - Split Layout */
.ev-game-meta-bar {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 12px;
  align-items: center;
  padding-top: 10px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  position: relative;
  z-index: 2;
}

/* Time Display - Enhanced */
.ev-time-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 800;
  font-family: 'Orbitron', monospace;
  color: rgba(255, 255, 255, 0.55);
  letter-spacing: 0.8px;
  text-transform: uppercase;
  padding: 4px 10px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.06);
  transition: all 0.3s ease;
}

.ev-game-card:hover .ev-time-meta {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.1);
}

.ev-time-icon-pro {
  width: 13px;
  height: 13px;
  opacity: 0.6;
}

/* Sharp Badge - Enhanced with Glow */
.ev-sharp-pro {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 5px 12px;
  background: linear-gradient(135deg, 
    rgba(28, 221, 144, 0.08) 0%, 
    rgba(28, 221, 144, 0.12) 100%
  );
  border: 1.5px solid rgba(28, 221, 144, 0.35);
  border-radius: 8px;
  font-size: 9px;
  font-weight: 900;
  font-family: 'Orbitron', monospace;
  color: rgb(28, 221, 144);
  text-transform: uppercase;
  letter-spacing: 1.2px;
  box-shadow: 
    0 2px 8px rgba(28, 221, 144, 0.2),
    inset 0 1px 2px rgba(28, 221, 144, 0.1);
  transition: all 0.3s ease;
  animation: sharpPulse 2s ease-in-out infinite;
}

@keyframes sharpPulse {
  0%, 100% { 
    box-shadow: 
      0 2px 8px rgba(28, 221, 144, 0.2),
      inset 0 1px 2px rgba(28, 221, 144, 0.1);
  }
  50% { 
    box-shadow: 
      0 4px 16px rgba(28, 221, 144, 0.4),
      inset 0 1px 2px rgba(28, 221, 144, 0.15);
  }
}

.ev-game-card:hover .ev-sharp-pro {
  background: linear-gradient(135deg, 
    rgba(28, 221, 144, 0.12) 0%, 
    rgba(28, 221, 144, 0.16) 100%
  );
  border-color: rgba(28, 221, 144, 0.5);
  transform: translateY(-1px);
}

.ev-sharp-icon-pro {
  width: 11px;
  height: 11px;
  filter: drop-shadow(0 0 4px rgba(28, 221, 144, 0.6));
}

/* Z-Index Layering */
.ev-game-header-optionC {
  /* Layer 0: Background watermarks (z-index: 0) */
  /* Layer 1: Dark overlay (implicit) */
  /* Layer 2: Content (z-index: 2) */
}
```

### Pros
- ✅ **Perfect balance** of horizontal and vertical space
- ✅ **Clear team separation** with away left, home right
- ✅ **Prominent rank badges** with enhanced silver gradient
- ✅ **VS divider** perfectly centered with decorative lines
- ✅ **Split footer** keeps time and sharp indicator organized
- ✅ **Enhanced hover states** for interactivity
- ✅ **Subtle animations** (sharp pulse, hover effects)
- ✅ **Professional sports betting aesthetic**
- ✅ **Optimized for 3-column grid** (compact but readable)
- ✅ **Watermark logos** properly layered with blur
- ✅ **Orbitron font** featured prominently

### Cons
- None significant - best all-around option

---

## 📐 Z-Index Layering System (All Options)

```css
/* Layer 0: Background Effects */
.ev-header-watermark-left,
.ev-header-watermark-right {
  z-index: 0;
}

/* Layer 1: Card Background Gradient (implicit) */
.ev-game-header-optionC {
  /* background color/gradient at base level */
}

/* Layer 2: Content Layer */
.ev-matchup-main,
.ev-game-meta-bar,
.ev-vs-divider-pro {
  position: relative;
  z-index: 2;
}

/* Layer 3: Hover Overlays (if needed) */
.ev-game-card::after {
  z-index: 3;
}
```

---

## 🎯 Recommendation Summary

### **OPTION C (Hybrid) is the Winner** because:

1. **Visual Hierarchy**: Perfectly balanced - teams clearly separated, VS centered, time/sharp at bottom
2. **Compact**: Fits 3-column grid while remaining highly readable
3. **Modern**: Matches sports betting UI standards (similar to DraftKings, FanDuel, Outlier.bet)
4. **Brand Alignment**: Showcases Orbitron font, rank badges, and watermark logos optimally
5. **Interactivity**: Enhanced hover states feel premium
6. **Scalability**: Works across responsive breakpoints

### Quick Implementation Priority:
1. ✅ **Option C** - Main production version
2. ⭐ **Option A** - Alternative for mobile/tablet breakpoints
3. 📦 **Option B** - Consider for ultra-compact "list view" mode

---

## 🚀 Next Steps

1. **Implement Option C** in `EVBettingDashboard.tsx`
2. **Update CSS** in `EVBettingDashboard.css`
3. **Test responsiveness** at 1400px, 1024px, 768px breakpoints
4. **Add optional dark/light theme variants**
5. **Performance test** watermark logo loading and rendering

---

*Last updated: December 5, 2025*
*Design system: Gameday+ Premium Sports Betting UI*
