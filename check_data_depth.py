import sqlite3

conn = sqlite3.connect('instance/coaches_master.db')
cursor = conn.cursor()

# Get a Power 5 coach example (Kirby Smart)
print("="*60)
print("EXISTING POWER 5 COACH (Kirby Smart)")
print("="*60)

cursor.execute("SELECT id FROM coaches WHERE name = 'Kirby Smart'")
kirby_id = cursor.fetchone()[0]

tables_to_check = [
    'stints', 'games', 'rankings', 'season_analytics', 
    'situational_stats', 'vs_coaches', 'draft_picks', 
    'recruiting_classes', 'talent_composite', 'transfer_portal'
]

kirby_data = {}
for table in tables_to_check:
    cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE coach_id = ?", (kirby_id,))
    count = cursor.fetchone()[0]
    kirby_data[table] = count
    print(f"  {table}: {count} records")

# Get a new G5 coach example (Spencer Danielson - Boise State)
print("\n" + "="*60)
print("NEW G5 COACH (Spencer Danielson)")
print("="*60)

cursor.execute("SELECT id FROM coaches WHERE name = 'Spencer Danielson'")
spencer_result = cursor.fetchone()
if spencer_result:
    spencer_id = spencer_result[0]
    
    spencer_data = {}
    for table in tables_to_check:
        cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE coach_id = ?", (spencer_id,))
        count = cursor.fetchone()[0]
        spencer_data[table] = count
        print(f"  {table}: {count} records")
else:
    print("  Coach not found")

# Check all new coaches
print("\n" + "="*60)
print("ALL NEW COACHES DATA DEPTH")
print("="*60)

cursor.execute("""
    SELECT id, name FROM coaches 
    WHERE id IN (
        SELECT id FROM coaches 
        ORDER BY id DESC 
        LIMIT 63
    )
""")

new_coaches = cursor.fetchall()
print(f"Checking {len(new_coaches)} most recent coaches...\n")

summary = {table: 0 for table in tables_to_check}

for coach_id, coach_name in new_coaches:
    for table in tables_to_check:
        cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE coach_id = ?", (coach_id,))
        count = cursor.fetchone()[0]
        summary[table] += count

print("Total records across all new coaches:")
for table, count in summary.items():
    print(f"  {table}: {count} records")

conn.close()
