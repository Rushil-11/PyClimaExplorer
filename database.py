import sqlite3
import bcrypt

DB_NAME = "prometheus.db"

def create_tables():
    """Creates the user and uploads tables if they don't exist yet."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Existing Users Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            institution TEXT,
            password TEXT NOT NULL
        )
    ''')
    
    # NEW: Uploads Table to track files
    c.execute('''
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            filename TEXT NOT NULL,
            file_type TEXT,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def add_user(name, email, institution, password):
    """Hashes the password and securely saves the user."""
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO users (name, email, institution, password) VALUES (?, ?, ?, ?)",
                  (name, email, institution, hashed.decode('utf-8')))
        conn.commit()
        conn.close()
        return True 
    except sqlite3.IntegrityError:
        conn.close()
        return False

def verify_user(email, password):
    """Checks if the email exists and the password matches the hash."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE email = ?", (email,))
    result = c.fetchone()
    conn.close()
    
    if result:
        stored_hashed_password = result[0]
        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
            return True
    return False

# --- NEW PROFILE FUNCTIONS ---

def get_user_details(email):
    """Fetches user info for the profile page."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT name, email, institution FROM users WHERE email = ?", (email,))
    result = c.fetchone()
    conn.close()
    
    if result:
        return {"name": result[0], "email": result[1], "institution": result[2]}
    return None

def change_password(email, new_password):
    """Updates a user's password."""
    hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE users SET password = ? WHERE email = ?", (hashed.decode('utf-8'), email))
    conn.commit()
    conn.close()
    return True

def log_file_upload(email, filename, file_type):
    """Records a newly uploaded file into the database."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO uploads (email, filename, file_type) VALUES (?, ?, ?)", 
              (email, filename, file_type))
    conn.commit()
    conn.close()

def get_user_files(email):
    """Retrieves all files uploaded by a specific user."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT filename, file_type, upload_date FROM uploads WHERE email = ? ORDER BY upload_date DESC", (email,))
    results = c.fetchall()
    conn.close()
    return results