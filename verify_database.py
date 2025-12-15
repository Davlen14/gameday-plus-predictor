import sqlite3

conn = sqlite3.connect('gameday_analytics.db')
cursor = conn.cursor()

print('📊 DATABASE STATS:')
print('='*50)
print(f"✅ Teams: {cursor.execute('SELECT COUNT(*) FROM teams').fetchone()[0]}")
print(f"✅ Games: {cursor.execute('SELECT COUNT(*) FROM games').fetchone()[0]}")
print(f"✅ Drives: {cursor.execute('SELECT COUNT(*) FROM drives').fetchone()[0]}")
print(f"✅ Plays: {cursor.execute('SELECT COUNT(*) FROM plays').fetchone()[0]}")

print('\n🏈 Sample Indiana Drives:')
print('='*50)
for row in cursor.execute('''
    SELECT d.drive_number, d.yards, d.plays, d.drive_result 
    FROM drives d 
    JOIN teams t ON d.offense_team_id = t.id 
    WHERE t.team_name = "Indiana" 
    LIMIT 10
'''):
    print(f"  Drive #{row[0]}: {row[1]} yards, {row[2]} plays → {row[3]}")

print('\n📈 Top 10 Teams by Total Offensive Yards:')
print('='*50)
for row in cursor.execute('''
    SELECT t.team_name, SUM(d.yards) as total_yards, COUNT(d.id) as num_drives
    FROM drives d
    JOIN teams t ON d.offense_team_id = t.id
    GROUP BY t.team_name
    ORDER BY total_yards DESC
    LIMIT 10
'''):
    print(f"  {row[0]}: {row[1]:,} yards ({row[2]} drives)")

conn.close()
