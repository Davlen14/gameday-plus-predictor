# 📋 Missing Features - GraphQL Ingestor vs Reference DB

## ✅ **COMPLETE (Already Working)**
| Feature | Reference | New DB | Status |
|---------|-----------|--------|--------|
| **Games** | 177 | **190** | ✅ BETTER (includes 2025!) |
| **Draft Picks** | 15 | 15 | ✅ COMPLETE |
| **Stints** | 2 | 2 | ✅ COMPLETE |
| **Coaches** | 1 | 1 | ✅ COMPLETE |

---

## ⚠️ **PARTIAL (Need More Data)**

### **1. Rankings** (5 / 78 rows - **93% missing**)
**Current:** Only preseason/postseason rankings (5 total)  
**Reference:** Weekly AP/Coaches poll rankings throughout season (78 total)

**What's Missing:**
- Week-by-week rankings during season
- Currently only getting: Preseason, Final (from GraphQL)
- Reference has: Weekly rankings for weeks 1-14+ across multiple seasons

**Fix Needed:**
```python
# Add REST API call for weekly rankings
GET /rankings?year={year}&team={school}&seasonType=regular
```

**Schema Already Exists:** ✅ Rankings table supports week column

---

### **2. Recruiting Classes** (15 / 30 rows - **50% missing**)
**Current:** 2011-2025 (15 years)  
**Reference:** 2000-2026 (30 years - includes future class)

**What's Missing:**
- Classes from 2000-2010 (before Campbell started at Toledo)
- 2026 recruiting class

**Fix Needed:**
- REST API already being used as fallback ✅
- Need to extend year range in REST calls to include all available data
- Currently filtering by stint years - should get ALL available data for the school

**Current Code:**
```python
for year in range(stint['start_year'], effective_end_year + 1):
```

**Should Be:**
```python
# Get ALL recruiting data available, not just during stint
for year in range(2000, effective_end_year + 2):  # +2 for future class
```

---

### **3. Talent Composite** (11 / 22 rows - **50% missing**)
**Current:** 2015-2025 (11 years)  
**Reference:** 2015-2025 (22 years - but this is across TWO schools)

**What's Missing:**
- Talent ratings are school-specific, not coach-specific
- Reference has Toledo 2015 + Iowa State 2015-2025 = 22 total
- New DB only has Iowa State 2015-2025 = 11 total (missing Toledo 2015)

**Fix Needed:**
- Current code already fetches per-stint ✅
- Check if Toledo 2015 talent rating exists in API
- Should be working correctly - investigate why Toledo 2015 missing

---

## ❌ **NOT IMPLEMENTED (Need to Add)**

### **4. Season Analytics** (0 / 15 rows - **100% missing**)
**Schema Exists:** ✅ Table created in setup_master_db.py  
**Data Source:** Calculate from `games` table (no API needed)

**Required Columns:**
```sql
- season (year)
- school
- total_wins
- total_losses  
- conf_wins
- conf_losses
- win_percentage
- conf_win_percentage
```

**Implementation Needed:**
```python
def _calculate_season_analytics(self, coach_id: int, cursor) -> int:
    # Query games table grouped by season/school
    # Calculate wins/losses overall and by conference
    # Insert into season_analytics table
```

**Priority:** 🔥 HIGH (core feature for coach evaluation)

---

### **5. Transfer Portal** (0 / 16 rows - **100% missing**)
**Schema Exists:** ✅ Table created in setup_master_db.py  
**Data Source:** GraphQL `portal` table (if exists) or REST API

**Required Columns:**
```sql
- season
- school
- transfers_in (count)
- transfers_out (count)
- net_transfers
- avg_rating_in
- avg_rating_out
```

**Reference Data:** 2018-2025 (8 seasons × 2 schools = 16 rows)

**Implementation Needed:**
- Check if GraphQL has `transferPortal` query
- Otherwise use REST: `GET /player/portal?year={year}`
- Aggregate by school/season

**Priority:** 🟡 MEDIUM (modern recruiting metric)

---

### **6. VS Coaches** (0 / 6 rows - **100% missing**)
**Schema Exists:** ✅ Table created in setup_master_db.py  
**Data Source:** Calculate from `games` table + coach metadata

**Required Columns:**
```sql
- opponent_coach (name)
- opponent_school
- wins
- losses
- record (e.g., "3-2")
- avg_point_differential
- biggest_win_margin
- biggest_loss_margin
- first_meeting_year
- last_meeting_year
```

**Implementation Needed:**
```python
def _calculate_vs_coaches(self, coach_id: int, cursor) -> int:
    # Get all games for this coach
    # Query GraphQL for opponent coaches (by school + year)
    # Aggregate head-to-head records
    # Calculate point differentials
```

**Complexity:** 🔴 HIGH (requires coach lookups for every opponent game)  
**Priority:** 🟡 MEDIUM (interesting but not critical)

---

## 📊 **Summary of Work Needed**

### **Quick Wins (1-2 hours)**
1. ✅ **Recruiting**: Extend year range to get 2000-2026 instead of stint years only
2. ✅ **Season Analytics**: Calculate from games table (simple GROUP BY query)
3. ⚠️ **Rankings**: Add REST API call for weekly rankings

### **Medium Complexity (3-5 hours)**
4. **Talent**: Debug why Toledo 2015 missing (should work already)
5. **Transfer Portal**: Add GraphQL/REST query for portal data

### **Complex (6+ hours)**
6. **VS Coaches**: Requires coach lookup for every opponent in every game

---

## 🎯 **Recommended Priority Order**

### **Phase 1: Core Data Completeness (Tonight/Tomorrow)**
1. **Season Analytics** - Calculate from existing games ✅
2. **Recruiting Extension** - Change year range to 2000-2026 ✅
3. **Talent Debug** - Fix missing Toledo 2015 ⚠️

### **Phase 2: Enhanced Metrics (This Week)**
4. **Weekly Rankings** - Add REST API calls for week-by-week data
5. **Transfer Portal** - Add portal data ingestion

### **Phase 3: Advanced Features (Next Week)**
6. **VS Coaches** - Complex head-to-head analysis

---

## 💡 **Current System Status**

**Working Perfectly:**
- ✅ Games (190/177 - includes 2025!)
- ✅ Draft Picks (15/15)
- ✅ Stints (2/2)
- ✅ Basic coach metadata

**Ready for 134 Coaches:**
- Current implementation will work for all coaches
- Missing features won't block batch ingestion
- Can add missing features incrementally

**API Usage:**
- Currently: ~9 calls per coach
- With all features: ~15-20 calls per coach
- 134 coaches × 20 = 2,680 calls (still well under 75k limit)

---

## 🚀 **Next Steps**

1. **Review this document** - Confirm what features you want
2. **Phase 1 implementation** - Add season_analytics and recruiting extension
3. **Test Matt Campbell** - Verify all Phase 1 features work
4. **Batch ingestion** - Run all 134 coaches
5. **Phase 2+ as needed** - Add remaining features based on priority
