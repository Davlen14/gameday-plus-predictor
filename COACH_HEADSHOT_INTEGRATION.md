# 🏈 Coach Headshot Integration

## Overview
Professional coach headshot integration for the Gameday+ coaching comparison section, featuring real coach photos from Power 5 conferences with premier chrome styling.

## 📊 Data Source
**File**: `power5_coaches_headshots.json`
- **Conferences**: Big 12, Big Ten, SEC, ACC
- **Total Coaches**: 60+ Power 5 head coaches
- **Format**: Structured JSON with school names, coach names, and headshot URLs

## 🎨 Visual Features

### Coach Headshots Display
1. **Main Header Cards** (80x80px)
   - Rounded corners with team-color borders
   - Shadow effects using team primary colors
   - Gradient overlay for depth
   - Elite badge for top-performing coaches
   - Team logo displayed alongside headshot

2. **Career Stats Sections** (48x48px)
   - Smaller headshots with team logos
   - Chrome-style borders matching team colors
   - Subtle gradient overlays

3. **Conference Breakdown** (40x40px)
   - Compact headshots for conference performance
   - Team logos displayed next to headshots
   - Color-coordinated shadows

## 🔧 Technical Implementation

### Service Layer
**File**: `frontend/src/services/coachService.ts`

```typescript
import { getCoachHeadshot } from '../../services/coachService';

// Get headshot URL by school name
const headshotUrl = getCoachHeadshot('Ohio State');

// Get full coach data
const coachData = getCoachData('Alabama');

// Get all coaches from a conference
const bigTenCoaches = getCoachesByConference('big10');
```

### Features
- **Fuzzy Matching**: Handles variations in school names (e.g., "Ohio State" vs "Ohio State University")
- **Conference Aliases**: Supports "Big Ten" and "BigTen" variations
- **Fallback Handling**: Uses team logos if headshot not available
- **Type Safety**: Full TypeScript interfaces for coach data

### Component Integration
**File**: `frontend/src/components/figma/CoachingComparison.tsx`

Headshots integrated into:
- ✅ Team Header cards (main coach comparison)
- ✅ Career Achievements sections
- ✅ Conference vs Ranked breakdown
- ✅ Elite Performance Analysis headers

## 🎯 Styling Patterns

### Modern Chrome Effects
```typescript
// Border with team color
borderColor: `${coach.color}40`

// Shadow with team color glow
boxShadow: `0 8px 24px ${coach.color}30, 0 0 0 1px ${coach.color}20`

// Gradient overlay for depth
<div className="absolute inset-0 bg-gradient-to-t from-slate-900/60 via-transparent to-transparent" />
```

### Image Enhancement
```typescript
style={{
  filter: 'brightness(1.05) contrast(1.1)'
}}
```

## 📋 Data Structure

### JSON Format
```json
{
  "big10": [
    {
      "coach": "Ryan Day",
      "school": "Ohio State",
      "headshot_url": "https://example.com/ryan-day.jpg"
    }
  ],
  "sec": [...],
  "acc": [...],
  "big12": [...]
}
```

## 🚀 Usage Example

```tsx
import { getCoachHeadshot } from '../../services/coachService';

// In component
<ImageWithFallback 
  src={getCoachHeadshot(coach.team) || coach.logo}
  alt={coach.name}
  className="w-full h-full object-cover"
/>
```

## 📦 File Locations
- **Data**: `/power5_coaches_headshots.json`
- **Service**: `/frontend/src/services/coachService.ts`
- **Component**: `/frontend/src/components/figma/CoachingComparison.tsx`
- **Types**: Defined in service file

## 🎨 Design Philosophy
1. **Professional Presentation**: Real coach photos elevate credibility
2. **Team Identity**: Color-coordinated borders and shadows match team branding
3. **Visual Hierarchy**: Headshot sizes match importance (80px → 48px → 40px)
4. **Fallback Strategy**: Always show team logo if headshot unavailable
5. **Chrome Styling**: Premium metallic effects with multi-layer shadows

## 🔄 Future Enhancements
- [ ] Add assistant coach headshots
- [ ] Historical coach comparisons
- [ ] Coach career timeline visualization
- [ ] Animated hover effects on headshots
- [ ] Coach vs coach head-to-head records

## ✅ Testing
1. **Visual Test**: Check all coach headshots render correctly
2. **Fallback Test**: Verify team logos appear when headshot missing
3. **Fuzzy Match Test**: Confirm school name variations work
4. **Responsive Test**: Ensure headshots look good on mobile

## 📊 Coverage
- **Big 12**: 16 coaches
- **Big Ten**: 18 coaches  
- **SEC**: 16 coaches
- **ACC**: 16 coaches
- **Total**: 66 Power 5 head coaches

---

**Status**: ✅ Production Ready  
**Last Updated**: December 3, 2025  
**Integration**: Complete - All coaching sections enhanced with headshots
