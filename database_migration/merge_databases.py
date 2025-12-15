#!/usr/bin/env python3
"""
MERGE DATABASES: After validation, merge predictions.db into coaches_master.db
Only run this AFTER validation passes!
"""

import sqlite3
import os
import shutil
from datetime import datetime

PREDICTIONS_DB = 'instance/predictions.db'
MASTER_DB = 'instance/coaches_master.db'

def backup_master():
    """Create backup of master database before merge"""
    print("🔒 Creating backup of coaches_master.db...")
    
    if not os.path.exists(MASTER_DB):
        print("⚠️  Master database not found - nothing to backup")
        return True
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"{MASTER_DB}.pre_merge_backup_{timestamp}"
    
    try:
        shutil.copy(MASTER_DB, backup_path)
        size = os.path.getsize(backup_path) / (1024*1024)
        print(f"✅ Backup created: {backup_path} ({size:.1f} MB)")
        return backup_path
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return None

def attach_predictions_db():
    """Attach predictions.db to master and copy tables"""
    print("\n📊 Merging predictions.db → coaches_master.db...")
    
    if not os.path.exists(PREDICTIONS_DB):
        print(f"❌ Predictions database not found: {PREDICTIONS_DB}")
        return False
    
    conn = sqlite3.connect(MASTER_DB)
    cursor = conn.cursor()
    
    try:
        # Attach predictions database
        cursor.execute(f"ATTACH DATABASE '{PREDICTIONS_DB}' AS pred")
        
        # Get list of tables in predictions DB
        cursor.execute("SELECT name FROM pred.sqlite_master WHERE type='table' AND name NOT IN ('sqlite_sequence')")
        pred_tables = [row[0] for row in cursor.fetchall()]
        
        print(f"\n📋 Found {len(pred_tables)} tables to merge:")
        
        for table in pred_tables:
            print(f"\n  📦 Merging table: {table}")
            
            # Check if table exists in master
            cursor.execute(f"SELECT name FROM main.sqlite_master WHERE type='table' AND name='{table}'")
            exists_in_master = cursor.fetchone() is not None
            
            if not exists_in_master:
                # Table doesn't exist - copy entire table
                print(f"    ✅ New table - copying entire structure and data")
                
                # Get CREATE statement from predictions DB
                cursor.execute(f"SELECT sql FROM pred.sqlite_master WHERE type='table' AND name='{table}'")
                create_sql = cursor.fetchone()[0]
                
                # Create table in master
                cursor.execute(create_sql)
                
                # Copy all data
                cursor.execute(f"INSERT INTO main.{table} SELECT * FROM pred.{table}")
                
                cursor.execute(f"SELECT COUNT(*) FROM main.{table}")
                count = cursor.fetchone()[0]
                print(f"    ✅ Copied {count:,} records")
                
            else:
                # Table exists - merge data (INSERT OR REPLACE)
                print(f"    ⚠️  Table exists in master - merging data")
                
                # Get count before
                cursor.execute(f"SELECT COUNT(*) FROM main.{table}")
                before_count = cursor.fetchone()[0]
                
                # Get columns
                cursor.execute(f"PRAGMA pred.table_info({table})")
                columns = [row[1] for row in cursor.fetchall()]
                cols_str = ', '.join(columns)
                
                # Merge data
                cursor.execute(f"INSERT OR REPLACE INTO main.{table} SELECT {cols_str} FROM pred.{table}")
                
                # Get count after
                cursor.execute(f"SELECT COUNT(*) FROM main.{table}")
                after_count = cursor.fetchone()[0]
                
                added = after_count - before_count
                print(f"    ✅ Before: {before_count:,} | After: {after_count:,} | Added: {added:,}")
        
        conn.commit()
        cursor.execute("DETACH DATABASE pred")
        conn.close()
        
        print("\n✅ Merge complete!")
        return True
        
    except Exception as e:
        print(f"\n❌ Merge failed: {e}")
        conn.rollback()
        conn.close()
        return False

def verify_merge():
    """Verify merge was successful"""
    print("\n🔍 Verifying merged database...")
    
    conn = sqlite3.connect(MASTER_DB)
    cursor = conn.cursor()
    
    checks = [
        ("drives_complete", "SELECT COUNT(*) FROM drives_complete"),
        ("team_epa_metrics", "SELECT COUNT(*) FROM team_epa_metrics"),
        ("team_offensive_stats", "SELECT COUNT(*) FROM team_offensive_stats"),
        ("team_defensive_stats", "SELECT COUNT(*) FROM team_defensive_stats"),
    ]
    
    all_passed = True
    for table, query in checks:
        try:
            cursor.execute(query)
            count = cursor.fetchone()[0]
            status = "✅" if count > 0 else "⚠️"
            print(f"  {status} {table}: {count:,} records")
        except Exception as e:
            print(f"  ❌ {table}: Error - {e}")
            all_passed = False
    
    # Check final database size
    conn.close()
    size = os.path.getsize(MASTER_DB) / (1024*1024)
    print(f"\n📊 Final database size: {size:.1f} MB")
    
    return all_passed

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║           🔀 MERGE PREDICTIONS.DB → MASTER.DB 🔀            ║
    ║                                                               ║
    ║     ⚠️  WARNING: This will modify coaches_master.db ⚠️      ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Verify predictions DB exists
    if not os.path.exists(PREDICTIONS_DB):
        print(f"❌ Predictions database not found: {PREDICTIONS_DB}")
        print("Run migration first: ./migrate.sh")
        return
    
    pred_size = os.path.getsize(PREDICTIONS_DB) / (1024*1024)
    print(f"📊 Predictions DB: {pred_size:.1f} MB")
    
    if os.path.exists(MASTER_DB):
        master_size = os.path.getsize(MASTER_DB) / (1024*1024)
        print(f"📊 Master DB: {master_size:.1f} MB")
    else:
        print("📊 Master DB: Not found (will be created)")
    
    # Confirm
    print("\n⚠️  This operation will:")
    print("  1. Backup coaches_master.db")
    print("  2. Merge all predictions.db tables into master")
    print("  3. Keep predictions.db unchanged (can delete manually later)")
    
    response = input("\n🚀 Proceed with merge? (yes/no): ").strip().lower()
    if response != 'yes':
        print("❌ Merge cancelled")
        return
    
    # Backup
    backup_path = backup_master()
    if not backup_path and os.path.exists(MASTER_DB):
        print("❌ Cannot proceed without backup")
        return
    
    # Merge
    if not attach_predictions_db():
        print("\n❌ Merge failed!")
        if backup_path:
            print(f"Restore backup: cp {backup_path} {MASTER_DB}")
        return
    
    # Verify
    if not verify_merge():
        print("\n⚠️  Verification issues - check above")
        if backup_path:
            print(f"If needed, restore backup: cp {backup_path} {MASTER_DB}")
        return
    
    print("\n" + "=" * 70)
    print("🎉 MERGE SUCCESSFUL!")
    print("=" * 70)
    print(f"""
    ✅ All predictor data merged into coaches_master.db
    
    📦 Backup saved: {backup_path if backup_path else 'N/A'}
    
    🎯 NEXT STEPS:
    
    1. Test predictor with master DB:
       python run.py "Ohio State" "Michigan"
    
    2. Update graphqlpredictor.py:
       - Change DB_PATH to 'instance/coaches_master.db'
       - Remove JSON loading code
    
    3. Archive JSON files:
       mkdir -p data/archived_json_backup
       mv data/*.json data/archived_json_backup/
    
    4. (Optional) Delete predictions.db:
       rm instance/predictions.db
    
    🏆 Your system now runs on a unified database! 🏆
    """)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Merge interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
