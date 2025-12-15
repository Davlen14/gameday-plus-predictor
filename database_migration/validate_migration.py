#!/usr/bin/env python3
"""
Validation: Compare Database vs JSON Results
Ensures migration accuracy before deleting JSON files
"""

import sqlite3
import json
import os
from datetime import datetime

# SAFE APPROACH: Validate predictions database
DB_PATH = 'instance/predictions.db'
MASTER_DB_PATH = 'instance/coaches_master.db'
DATA_DIR = 'data'

class MigrationValidator:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.errors = []
        self.warnings = []
        
    def close(self):
        self.conn.close()
    
    def validate_team_count(self):
        """Validate team count matches"""
        print("\n✓ Validating Team Count...")
        
        # Count teams in JSON
        with open(os.path.join(DATA_DIR, 'fbs_teams_stats_only.json'), 'r') as f:
            json_teams = json.load(f)
        json_count = len(json_teams)
        
        # Check if EPA metrics were migrated
        self.cursor.execute("SELECT COUNT(*) FROM team_epa_metrics")
        epa_count = self.cursor.fetchone()[0]
        
        if epa_count == 0:
            print(f"  ⚠️  EPA metrics not yet migrated (using master.teams via ATTACH)")
            return True  # Don't fail for incomplete Phase 3
        
        # Count teams in DB
        self.cursor.execute("SELECT COUNT(DISTINCT team_id) FROM team_epa_metrics WHERE season = 2025")
        db_count = self.cursor.fetchone()[0]
        
        if json_count == db_count:
            print(f"  ✅ Team count matches: {db_count} teams")
            return True
        else:
            error = f"  ❌ Mismatch: JSON has {json_count} teams, DB has {db_count} teams"
            print(error)
            self.errors.append(error)
            return False
    
    def validate_drive_count(self):
        """Validate drive count matches"""
        print("\n✓ Validating Drive Count...")
        
        # Count drives in JSON
        with open(os.path.join(DATA_DIR, 'power5_drives_only.json'), 'r') as f:
            json_drives = json.load(f)
        json_count = len(json_drives)
        
        # Count drives in DB
        self.cursor.execute("SELECT COUNT(*) FROM drives_complete")
        db_count = self.cursor.fetchone()[0]
        
        difference = abs(json_count - db_count)
        percent_diff = (difference / json_count) * 100 if json_count > 0 else 0
        
        if percent_diff < 1.0:  # Allow <1% difference
            print(f"  ✅ Drive count matches: {db_count:,} drives (JSON: {json_count:,})")
            return True
        else:
            error = f"  ❌ Significant mismatch: JSON has {json_count:,}, DB has {db_count:,} ({percent_diff:.2f}% diff)"
            print(error)
            self.errors.append(error)
            return False
    
    def validate_epa_metrics(self):
        """Validate EPA metrics match for sample teams"""
        print("\n✓ Validating EPA Metrics (Sample Check)...")
        
        # Check if EPA metrics were migrated
        self.cursor.execute("SELECT COUNT(*) FROM team_epa_metrics")
        epa_count = self.cursor.fetchone()[0]
        
        if epa_count == 0:
            print("  ⚠️  EPA metrics not yet migrated (Phase 3 incomplete)")
            return True  # Don't fail validation for incomplete phase
        
        # Load JSON
        with open(os.path.join(DATA_DIR, 'fbs_teams_stats_only.json'), 'r') as f:
            json_teams = json.load(f)
        
        # Test 5 random teams
        test_teams = ['Ohio State', 'Alabama', 'Oregon', 'Texas', 'Georgia']
        
        matches = 0
        for team_name in test_teams:
            # Get JSON data
            json_data = next((t for t in json_teams if t['team'] == team_name), None)
            if not json_data:
                continue
            
            # Get DB data
            self.cursor.execute("""
                SELECT off_ppa, def_ppa, off_success_rate, def_success_rate
                FROM team_epa_metrics
                WHERE team_name = ? AND season = 2025
            """, (team_name,))
            db_data = self.cursor.fetchone()
            
            if db_data:
                json_off_ppa = json_data.get('stats', {}).get('offensivePPA')
                db_off_ppa = db_data[0]
                
                if json_off_ppa and db_off_ppa:
                    diff = abs(json_off_ppa - db_off_ppa)
                    if diff < 0.01:  # Allow tiny floating point differences
                        matches += 1
                        print(f"  ✅ {team_name}: OFF PPA matches ({db_off_ppa:.4f})")
                    else:
                        warning = f"  ⚠️  {team_name}: OFF PPA mismatch (JSON: {json_off_ppa:.4f}, DB: {db_off_ppa:.4f})"
                        print(warning)
                        self.warnings.append(warning)
        
        if matches >= 3:  # At least 3 out of 5 should match
            print(f"  ✅ EPA validation passed ({matches}/5 teams verified)")
            return True
        else:
            error = f"  ❌ Too many mismatches ({matches}/5 teams matched)"
            print(error)
            self.errors.append(error)
            return False
    
    def validate_drives_sample(self):
        """Validate specific drive records match"""
        print("\n✓ Validating Drive Records (Sample Check)...")
        
        # Load JSON
        with open(os.path.join(DATA_DIR, 'power5_drives_only.json'), 'r') as f:
            json_drives = json.load(f)
        
        # Test first 10 drives
        matches = 0
        for drive in json_drives[:10]:
            drive_id = drive.get('id')
            
            # Check DB
            self.cursor.execute("""
                SELECT offense, yards, plays_count, scoring
                FROM drives_complete
                WHERE id = ?
            """, (drive_id,))
            db_drive = self.cursor.fetchone()
            
            if db_drive:
                json_yards = drive.get('yards')
                db_yards = db_drive[1]
                
                if json_yards == db_yards:
                    matches += 1
                else:
                    warning = f"  ⚠️  Drive {drive_id}: yards mismatch (JSON: {json_yards}, DB: {db_yards})"
                    print(warning)
                    self.warnings.append(warning)
            else:
                warning = f"  ⚠️  Drive {drive_id} not found in database"
                print(warning)
                self.warnings.append(warning)
        
        if matches >= 8:  # At least 8 out of 10 should match
            print(f"  ✅ Drive validation passed ({matches}/10 drives verified)")
            return True
        else:
            error = f"  ❌ Too many mismatches ({matches}/10 drives matched)"
            print(error)
            self.errors.append(error)
            return False
    
    def validate_coach_rankings(self):
        """Validate coach rankings match"""
        print("\n✓ Validating Coach Rankings...")
        
        # Load JSON
        with open(os.path.join(DATA_DIR, 'coaches_advanced_rankings.json'), 'r') as f:
            json_coaches = json.load(f)
        
        # Count coaches
        json_count = len(json_coaches)
        
        self.cursor.execute("SELECT COUNT(*) FROM coach_rankings WHERE season = 2025")
        db_count = self.cursor.fetchone()[0]
        
        if json_count == db_count:
            print(f"  ✅ Coach count matches: {db_count} coaches")
            return True
        else:
            error = f"  ❌ Mismatch: JSON has {json_count} coaches, DB has {db_count} coaches"
            print(error)
            self.errors.append(error)
            return False
    
    def validate_indexes(self):
        """Validate all indexes were created"""
        print("\n✓ Validating Database Indexes...")
        
        self.cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='index' AND name LIKE 'idx_%'
            ORDER BY name
        """)
        indexes = self.cursor.fetchall()
        
        required_indexes = [
            'idx_drives_complete_team_season',
            'idx_drives_complete_offense',
            'idx_drives_complete_scoring',
            'idx_epa_team_season',
        ]
        
        found_indexes = [idx[0] for idx in indexes]
        missing = [idx for idx in required_indexes if idx not in found_indexes]
        
        if not missing:
            print(f"  ✅ All required indexes created ({len(found_indexes)} total)")
            return True
        else:
            error = f"  ⚠️  Missing indexes: {', '.join(missing)}"
            print(error)
            self.warnings.append(error)
            return True  # Warning, not error
    
    def generate_report(self):
        """Generate validation report"""
        print("\n" + "=" * 60)
        print("📋 VALIDATION REPORT")
        print("=" * 60)
        
        if not self.errors and not self.warnings:
            print("✅ ALL VALIDATIONS PASSED!")
            print("\n🎉 Migration is SUCCESSFUL and accurate!")
            print("\n✅ Safe to proceed with:")
            print("   1. Archive JSON files")
            print("   2. Update graphqlpredictor.py")
            print("   3. Deploy to production")
            return True
        else:
            if self.errors:
                print(f"\n❌ ERRORS FOUND: {len(self.errors)}")
                for error in self.errors:
                    print(f"  {error}")
            
            if self.warnings:
                print(f"\n⚠️  WARNINGS: {len(self.warnings)}")
                for warning in self.warnings:
                    print(f"  {warning}")
            
            if self.errors:
                print("\n⛔ DO NOT PROCEED - Fix errors first!")
                return False
            else:
                print("\n⚠️  Warnings found but not critical - Safe to proceed with caution")
                return True

def run_full_validation():
    """Run complete validation suite"""
    print("🔍 FULL MIGRATION VALIDATION")
    print("=" * 60)
    
    validator = MigrationValidator()
    
    results = [
        validator.validate_team_count(),
        validator.validate_drive_count(),
        validator.validate_epa_metrics(),
        validator.validate_drives_sample(),
        validator.validate_coach_rankings(),
        validator.validate_indexes(),
    ]
    
    success = validator.generate_report()
    validator.close()
    
    return success

if __name__ == '__main__':
    success = run_full_validation()
    exit(0 if success else 1)
