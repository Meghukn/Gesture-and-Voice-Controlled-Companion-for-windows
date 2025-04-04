import sqlite3

# Connect to the database
con = sqlite3.connect("mitra.db")
cursor = con.cursor()

# Drop existing tables if necessary (optional, use only if resetting the DB)
# cursor.execute('DROP TABLE IF EXISTS web_command')
# cursor.execute('DROP TABLE IF EXISTS sys_command')
# cursor.execute('DROP TABLE IF EXISTS contacts')

# # Create Web Command Table with multilingual support
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS web_command (
#         id INTEGER PRIMARY KEY, 
#         name VARCHAR(100), 
#         name_kn VARCHAR(100), 
#         url VARCHAR(1000)
#     );
# ''')

# # Create System Command Table with multilingual support
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS sys_command (
#         id INTEGER PRIMARY KEY, 
#         name VARCHAR(100), 
#         name_kn VARCHAR(100), 
#         path VARCHAR(1000)
#     );
# ''')

# # Commit changes and close the connection
# con.commit()
# print("Database setup complete with multilingual support!")

# con.close()


# import sqlite3

# Connect to the database
con = sqlite3.connect("mitra.db")
cursor = con.cursor()

# Insert Web Commands (English + Kannada)
web_commands = [
    ("google", "ಗೂಗಲ್", "https://www.google.com"),
    ("spotify", "ಸ್ಪೋಟಿಫೈ", "https://open.spotify.com"),
    ("youtube", "ಯೂಟ್ಯೂಬ್", "https://www.youtube.com")
]

cursor.executemany("INSERT INTO web_command (name, name_kn, url) VALUES (?, ?, ?);", web_commands)

# Insert System Commands (English + Kannada)
sys_commands = [
    ("notepad", "ಟೆಕ್ಸ್ ಪ್ಯಾಡ್", "C:\\Windows\\System32\\notepad.exe"),
    ("calculator", "ಗಣಕಯಂತ್ರ", "C:\\Windows\\System32\\calc.exe"),
    ("command_prompt", "ಆಜ್ಞಾ ಪ್ರಾಂಪ್ಟ್", "C:\\Windows\\System32\\cmd.exe")
]

cursor.executemany("INSERT INTO sys_command (name, name_kn, path) VALUES (?, ?, ?);", sys_commands)

# Commit changes and close the connection
con.commit()
print("Data inserted successfully!")

con.close()