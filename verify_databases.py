#!/usr/bin/env python3
"""
Quick script to verify all SQL databases are accessible and show sample data
"""
import sqlite3
import os

def verify_database(db_path, db_name):
    """Verify database is accessible and show basic info"""
    if not os.path.exists(db_path):
        print(f"❌ {db_name}: File not found at {db_path}")
        return
    
    size = os.path.getsize(db_path)
    if size == 0:
        print(f"⚠️  {db_name}: Empty file (0 bytes)")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get table count
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        table_count = len(tables)
        
        print(f"✅ {db_name}:")
        print(f"   Size: {size:,} bytes ({size/1024/1024:.2f} MB)")
        print(f"   Tables: {table_count}")
        
        # Show first 3 tables with row counts
        if tables:
            print(f"   Sample tables:")
            for table in tables[:3]:
                table_name = table[0]
                # Use parameterized query with identifier quoting to prevent SQL injection
                cursor.execute(f'SELECT COUNT(*) FROM "{table_name}"')
                count = cursor.fetchone()[0]
                print(f"      - {table_name}: {count:,} rows")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ {db_name}: Error - {e}")

def main():
    print("=" * 70)
    print("SQL DATABASE VERIFICATION - Gameday+ Predictor")
    print("=" * 70)
    print()
    
    databases = [
        ("instance/coaches_master.db", "coaches_master.db (Primary Coach DB)"),
        ("instance/predictions.db", "predictions.db (Prediction Engine)"),
        ("gameday_analytics.db", "gameday_analytics.db (Live Analytics)"),
        ("instance/campbell_test.db", "campbell_test.db (Test DB)"),
        ("instance/cfb_database.db", "cfb_database.db (Placeholder)"),
        ("instance/gameday_analytics.db", "gameday_analytics.db (Placeholder)"),
        ("coaches_master.db", "coaches_master.db (Root - Placeholder)"),
    ]
    
    for db_path, db_name in databases:
        verify_database(db_path, db_name)
        print()
    
    print("=" * 70)
    print("SCHEMA FILES:")
    print("=" * 70)
    
    schema_files = [
        "create_espn_tables.sql",
        "add_missing_columns.sql"
    ]
    
    for schema_file in schema_files:
        if os.path.exists(schema_file):
            size = os.path.getsize(schema_file)
            with open(schema_file, 'r') as f:
                lines = len(f.readlines())
            print(f"✅ {schema_file}: {size:,} bytes, {lines} lines")
        else:
            print(f"❌ {schema_file}: Not found")
    
    print()
    print("=" * 70)

if __name__ == "__main__":
    main()
