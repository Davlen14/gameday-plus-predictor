import sqlite3

conn = sqlite3.connect('instance/campbell_test.db')
cursor = conn.cursor()

print("🔧 RESTORING POP-TARTS BOWL")
print("=" * 80)

print("\n📍 Clarification: The 2024 Iowa State vs Miami game (W 42-41)")
print("   was actually the POP-TARTS BOWL, not Big 12 Championship")
print("   Official record shows 2024: 11-3 (14 games total)")
print("   Database currently shows: 10-3 (13 games)")

# Add back the Pop-Tarts Bowl
cursor.execute("""
    INSERT INTO games (season, week, school, opponent, result, coach_score, opponent_score, season_type)
    VALUES (2024, 1, 'Iowa State', 'Miami', 'W', 42, 41, 'postseason')
""")

print("\n✅ Added: 2024 Pop-Tarts Bowl - Iowa State vs Miami (W 42-41)")

# Recalculate all totals
cursor.execute("""
    SELECT 
        COUNT(*) as games,
        SUM(CASE WHEN result='W' THEN 1 ELSE 0 END) as wins,
        SUM(CASE WHEN result='L' THEN 1 ELSE 0 END) as losses
    FROM games 
    WHERE school = 'Toledo'
""")
toledo_stats = cursor.fetchone()

cursor.execute("""
    SELECT 
        COUNT(*) as games,
        SUM(CASE WHEN result='W' THEN 1 ELSE 0 END) as wins,
        SUM(CASE WHEN result='L' THEN 1 ELSE 0 END) as losses
    FROM games 
    WHERE school = 'Iowa State'
""")
iowa_state_stats = cursor.fetchone()

cursor.execute("""
    SELECT 
        COUNT(*) as games,
        SUM(CASE WHEN result='W' THEN 1 ELSE 0 END) as wins,
        SUM(CASE WHEN result='L' THEN 1 ELSE 0 END) as losses
    FROM games
""")
career_stats = cursor.fetchone()

print("\n" + "=" * 80)
print("📊 FINAL TOTALS")
print("=" * 80)

print(f"\nToledo (2012-2015): {toledo_stats[1]}-{toledo_stats[2]} ({toledo_stats[0]} games)")
print(f"  Official: 35-15 (50 games) {'✅' if toledo_stats[0] == 50 else '❌'}")

print(f"\nIowa State (2016-2025): {iowa_state_stats[1]}-{iowa_state_stats[2]} ({iowa_state_stats[0]} games)")
print(f"  Official: 72-55 (127 games) {'✅' if iowa_state_stats[0] == 127 else '❌'}")

print(f"\nCareer Total: {career_stats[1]}-{career_stats[2]} ({career_stats[0]} games)")
print(f"  Official: 107-70 (177 games) {'✅' if career_stats[0] == 177 else '❌'}")

# Update all summary tables
cursor.execute("""
    UPDATE stints 
    SET record = ?,
        games_coached = ?
    WHERE school = 'Toledo'
""", (f"{toledo_stats[1]}-{toledo_stats[2]}", toledo_stats[0]))

cursor.execute("""
    UPDATE stints 
    SET record = ?,
        games_coached = ?
    WHERE school = 'Iowa State'
""", (f"{iowa_state_stats[1]}-{iowa_state_stats[2]}", iowa_state_stats[0]))

cursor.execute("""
    UPDATE coaches 
    SET career_record = ?,
        total_games = ?
    WHERE name = 'Matt Campbell'
""", (f"{career_stats[1]}-{career_stats[2]}", career_stats[0]))

conn.commit()
conn.close()

print("\n✅ Summary tables updated")

print("\n" + "=" * 80)
if career_stats[0] == 177 and career_stats[1] == 107 and career_stats[2] == 70:
    print("✅ DATABASE NOW MATCHES OFFICIAL RECORDS PERFECTLY!")
    print("   177 games, 107-70 record")
else:
    print(f"Status: {career_stats[1]}-{career_stats[2]} ({career_stats[0]} games)")
    print(f"Target: 107-70 (177 games)")
    print(f"Difference: {career_stats[0] - 177} games, {career_stats[1] - 107} wins, {career_stats[2] - 70} losses")
print("=" * 80)

print("\n💾 Changes committed!")
print("🔄 Refresh http://localhost:5555")

