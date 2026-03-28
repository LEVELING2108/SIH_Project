"""
Simple migration script to add account lockout fields to users table
"""
import sqlite3
import os

def migrate():
    """Add account lockout columns to users table"""
    # Get database path
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'vendors.db')
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'failed_login_attempts' in columns and 'locked_until' in columns:
            print("✓ Migration already applied - columns exist")
            return
        
        # Add columns
        if 'failed_login_attempts' not in columns:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN failed_login_attempts INTEGER DEFAULT 0 NOT NULL"
            )
            print("✓ Added failed_login_attempts column")
        
        if 'locked_until' not in columns:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN locked_until DATETIME"
            )
            print("✓ Added locked_until column")
        
        conn.commit()
        print("✓ Migration completed successfully!")
        
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == '__main__':
    print("Running database migration for account lockout...")
    migrate()
