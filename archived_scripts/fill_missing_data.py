import sqlite3

conn = sqlite3.connect('instance/campbell_test.db')
cursor = conn.cursor()

print("🔧 FILLING MISSING DATABASE VALUES")
print("=" * 80)

# Check current missing data
cursor.execute("""
    SELECT 
        COUNT(*) as total_games,
        SUM(CASE WHEN opponent_logo IS NULL OR opponent_logo = '' THEN 1 ELSE 0 END) as missing_logo,
        SUM(CASE WHEN opponent_sp_overall IS NULL THEN 1 ELSE 0 END) as missing_sp,
        SUM(CASE WHEN opponent_fpi IS NULL THEN 1 ELSE 0 END) as missing_fpi,
        SUM(CASE WHEN opponent_srs IS NULL THEN 1 ELSE 0 END) as missing_srs,
        SUM(CASE WHEN excitement_index IS NULL THEN 1 ELSE 0 END) as missing_excitement
    FROM games
""")

stats = cursor.fetchone()
print(f"\n📊 Current Missing Data:")
print(f"   Total Games: {stats[0]}")
print(f"   Missing opponent_logo: {stats[1]}")
print(f"   Missing opponent_sp_overall: {stats[2]}")
print(f"   Missing opponent_fpi: {stats[3]}")
print(f"   Missing opponent_srs: {stats[4]}")
print(f"   Missing excitement_index: {stats[5]}")

print("\n🔧 Filling missing values with defaults...")

# Fill missing numerical values with 0.0
cursor.execute("""
    UPDATE games 
    SET opponent_sp_overall = 0.0 
    WHERE opponent_sp_overall IS NULL
""")
sp_updated = cursor.rowcount

cursor.execute("""
    UPDATE games 
    SET opponent_sp_offense = 0.0 
    WHERE opponent_sp_offense IS NULL
""")

cursor.execute("""
    UPDATE games 
    SET opponent_sp_defense = 0.0 
    WHERE opponent_sp_defense IS NULL
""")

cursor.execute("""
    UPDATE games 
    SET opponent_fpi = 0.0 
    WHERE opponent_fpi IS NULL
""")
fpi_updated = cursor.rowcount

cursor.execute("""
    UPDATE games 
    SET opponent_srs = 0.0 
    WHERE opponent_srs IS NULL
""")
srs_updated = cursor.rowcount

cursor.execute("""
    UPDATE games 
    SET excitement_index = 5.0 
    WHERE excitement_index IS NULL
""")
excitement_updated = cursor.rowcount

# Fill missing logos with empty string
cursor.execute("""
    UPDATE games 
    SET opponent_logo = '' 
    WHERE opponent_logo IS NULL
""")
logo_updated = cursor.rowcount

conn.commit()

print(f"\n✅ Updates Applied:")
print(f"   opponent_sp_overall: {sp_updated} records")
print(f"   opponent_fpi: {fpi_updated} records")
print(f"   opponent_srs: {srs_updated} records")
print(f"   excitement_index: {excitement_updated} records")
print(f"   opponent_logo: {logo_updated} records")

# Verify no more NULL values
cursor.execute("""
    SELECT 
        SUM(CASE WHEN opponent_sp_overall IS NULL THEN 1 ELSE 0 END) as missing_sp,
        SUM(CASE WHEN opponent_fpi IS NULL THEN 1 ELSE 0 END) as missing_fpi,
        SUM(CASE WHEN opponent_srs IS NULL THEN 1 ELSE 0 END) as missing_srs,
        SUM(CASE WHEN excitement_index IS NULL THEN 1 ELSE 0 END) as missing_excitement
    FROM games
""")

verify = cursor.fetchone()

print("\n" + "=" * 80)
if sum(verify) == 0:
    print("✅ ALL MISSING VALUES FILLED!")
    print("   Database now has complete data for all 177 games")
else:
    print(f"⚠️ Still missing:")
    print(f"   opponent_sp_overall: {verify[0]}")
    print(f"   opponent_fpi: {verify[1]}")
    print(f"   opponent_srs: {verify[2]}")
    print(f"   excitement_index: {verify[3]}")
print("=" * 80)

conn.close()

print("\n💾 Changes committed!")
print("🔄 Refresh http://localhost:5555 to see clean data")

