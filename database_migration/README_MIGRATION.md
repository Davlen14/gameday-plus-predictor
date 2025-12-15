# 🚀 COMPLETE DATABASE MIGRATION
## Week 16 Final Migration - CFP Ready System

**Timeline:** December 10-15, 2025  
**Goal:** Eliminate all 22 JSON files, migrate to single database source  
**Benefit:** 5-10x faster predictions, unlimited query flexibility

---

## 📋 MIGRATION CHECKLIST

### Phase 1: Schema Creation (30 minutes)
- [ ] Run `python database_migration/01_create_schema.py`
- [ ] Verify new tables created (10 new tables)
- [ ] Backup current database: `cp instance/coaches_master.db instance/coaches_master_backup_20251210.db`

### Phase 2: Data Migration (2-3 hours)
- [ ] Run `python database_migration/02_migrate_core_data.py` (coaches, teams, rankings)
- [ ] Run `python database_migration/03_migrate_stats.py` (EPA, offensive, defensive)
- [ ] Run `python database_migration/04_migrate_drives.py` (11,507 drives)
- [ ] Run `python database_migration/05_migrate_players.py` (player efficiency data)
- [ ] Run `python database_migration/06_migrate_metadata.py` (conferences, win probabilities)

### Phase 3: Validation (1 hour)
- [ ] Run `python database_migration/validate_migration.py`
- [ ] Compare DB vs JSON results (must be <0.1% difference)
- [ ] Test 5 sample predictions

### Phase 4: Predictor Refactor (2 hours)
- [ ] Update `graphqlpredictor.py` to use database queries
- [ ] Add database helper class `DatabaseLoader`
- [ ] Test predictions with new DB-backed system

### Phase 5: Archive JSONs (15 minutes)
- [ ] Move JSON files to `data/archived_json_backup/`
- [ ] Update `.gitignore` to exclude archived JSONs
- [ ] Document rollback procedure

---

## 🔄 ROLLBACK PROCEDURE

If anything goes wrong:
```bash
# Restore backup
cp instance/coaches_master_backup_20251210.db instance/coaches_master.db

# Revert predictor changes
git checkout main -- graphqlpredictor.py

# Restore JSON files
mv data/archived_json_backup/*.json data/
```

---

## 📊 EXPECTED RESULTS

| Metric | Before | After |
|--------|--------|-------|
| JSON Files | 22 | 0 |
| Database Size | 13 MB | ~100 MB |
| Predictor Load Time | 5-7 sec | 0.5-1 sec |
| Query Flexibility | None | Unlimited SQL |

---

## ⚠️ IMPORTANT NOTES

- **Keep `fbs.json`** in `static/` for frontend team picker
- **Backup before each phase** - SQLite is transactional but be safe
- **Test thoroughly** - CFP predictions are high-stakes
- **Monitor performance** - Add indexes if queries are slow

---

## 🎯 POST-MIGRATION

After successful migration:
1. Update weekly ETL scripts to populate DB directly
2. Create database maintenance cron jobs
3. Set up monitoring for data freshness
4. Document new query patterns for team

**Ready to start? Run Phase 1 first!**
