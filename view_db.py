import sqlite3

# Connect to database in instance folder
conn = sqlite3.connect('instance/urls.db')
cursor = conn.cursor()

# Check if table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='url'")
table_exists = cursor.fetchone()

if table_exists:
    # Get all data
    cursor.execute("SELECT * FROM url")
    rows = cursor.fetchall()
    
    if rows:
        print("\n" + "="*70)
        print("ID  |  SHORT CODE  |  LONG URL")
        print("="*70)
        for row in rows:
            print(f"{row[0]}    |  {row[2]}       |  {row[1]}")
        print("="*70)
        print(f"Total URLs: {len(rows)}")
    else:
        print("Table exists but no data found.")
        print("Shorten some URLs first!")
else:
    print("Table 'url' doesn't exist yet.")
    print("Run your app and shorten URLs first!")

conn.close()