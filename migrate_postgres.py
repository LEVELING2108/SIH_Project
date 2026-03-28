"""
PostgreSQL Migration Script
Creates all tables and migrates data from SQLite to PostgreSQL
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from extensions import db
from models import User, Vendor, TrackItem, Inspection
from datetime import datetime

def create_tables():
    """Create all database tables"""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Tables created successfully!")

def create_default_admin():
    """Create default admin user"""
    with app.app_context():
        # Check if admin exists
        admin = User.query.filter_by(role='admin').first()
        if admin:
            print("✓ Admin user already exists")
            return
        
        # Create admin
        admin_user = User(
            username='admin',
            email='admin@railtrackpro.com',
            role='admin'
        )
        admin_user.set_password('Admin@123')
        
        db.session.add(admin_user)
        db.session.commit()
        
        print("✓ Default admin user created!")
        print("  Username: admin")
        print("  Password: Admin@123")
        print("  ⚠️  Change password after first login!")

def migrate_sqlite_data():
    """Migrate data from SQLite to PostgreSQL (optional)"""
    import sqlite3
    
    sqlite_db = os.path.join(os.path.dirname(__file__), 'backend', 'instance', 'vendors.db')
    
    if not os.path.exists(sqlite_db):
        print("ℹ️  No SQLite database found, skipping data migration")
        return
    
    print("Migrating data from SQLite...")
    
    try:
        # Connect to SQLite
        sqlite_conn = sqlite3.connect(sqlite_db)
        sqlite_conn.row_factory = sqlite3.Row
        sqlite_cursor = sqlite_conn.cursor()
        
        with app.app_context():
            # Migrate Users
            sqlite_cursor.execute("SELECT * FROM users")
            users = sqlite_cursor.fetchall()
            
            for user in users:
                # Check if user exists
                existing = User.query.filter_by(username=user['username']).first()
                if not existing:
                    new_user = User(
                        id=user['id'],
                        username=user['username'],
                        email=user['email'],
                        password_hash=user['password_hash'],
                        role=user['role'],
                        is_active=user['is_active'],
                        created_at=datetime.fromisoformat(user['created_at']) if user['created_at'] else None,
                        last_login=datetime.fromisoformat(user['last_login']) if user['last_login'] else None,
                        failed_login_attempts=user.get('failed_login_attempts', 0),
                        locked_until=datetime.fromisoformat(user['locked_until']) if user.get('locked_until') else None
                    )
                    db.session.add(new_user)
                    print(f"  ✓ Migrated user: {user['username']}")
            
            db.session.commit()
            
            # Migrate Vendors
            sqlite_cursor.execute("SELECT * FROM vendor_data")
            vendors = sqlite_cursor.fetchall()
            
            for vendor in vendors:
                existing = Vendor.query.get(vendor['id'])
                if not existing:
                    new_vendor = Vendor(
                        id=vendor['id'],
                        vendor_name=vendor['vendor_name'],
                        contact_person=vendor['contact_person'],
                        contact_email=vendor['contact_email'],
                        contact_phone=vendor['contact_phone'],
                        address_line1=vendor['address_line1'],
                        city=vendor['city'],
                        state=vendor['state'],
                        postal_code=vendor['postal_code'],
                        country=vendor['country'],
                        tax_id=vendor['tax_id'],
                        bank_account=vendor['bank_account'],
                        vendor_code=vendor['vendor_code'],
                        certification_status=vendor['certification_status'],
                        performance_rating=vendor['performance_rating'],
                        is_approved=vendor['is_approved'],
                        approval_date=datetime.fromisoformat(vendor['approval_date']).date() if vendor['approval_date'] else None,
                        created_by_id=vendor['created_by_id'],
                        created_at=datetime.fromisoformat(vendor['created_at']) if vendor['created_at'] else None,
                        updated_at=datetime.fromisoformat(vendor['updated_at']) if vendor['updated_at'] else None
                    )
                    db.session.add(new_vendor)
                    print(f"  ✓ Migrated vendor: {vendor['vendor_name']}")
            
            db.session.commit()
            
            # Migrate Track Items
            sqlite_cursor.execute("SELECT * FROM track_items")
            track_items = sqlite_cursor.fetchall()
            
            for item in track_items:
                existing = TrackItem.query.get(item['id'])
                if not existing:
                    new_item = TrackItem(
                        id=item['id'],
                        item_type=item['item_type'],
                        lot_number=item['lot_number'],
                        vendor_id=item['vendor_id'],
                        quantity=item['quantity'],
                        manufacture_date=datetime.fromisoformat(item['manufacture_date']).date() if item['manufacture_date'] else None,
                        supply_date=datetime.fromisoformat(item['supply_date']).date() if item['supply_date'] else None,
                        installation_date=datetime.fromisoformat(item['installation_date']).date() if item['installation_date'] else None,
                        warranty_period_years=item['warranty_period_years'],
                        warranty_start_date=datetime.fromisoformat(item['warranty_start_date']).date() if item['warranty_start_date'] else None,
                        warranty_expiry_date=datetime.fromisoformat(item['warranty_expiry_date']).date() if item['warranty_expiry_date'] else None,
                        installation_location=item['installation_location'],
                        kilometer_from=item['kilometer_from'],
                        kilometer_to=item['kilometer_to'],
                        section_name=item['section_name'],
                        division=item['division'],
                        zone=item['zone'],
                        status=item['status'],
                        performance_status=item['performance_status'],
                        defect_count=item['defect_count'],
                        replacement_count=item['replacement_count'],
                        specifications=item['specifications'],
                        details=item['details'],
                        notes=item['notes'],
                        created_by_id=item['created_by_id'],
                        created_at=datetime.fromisoformat(item['created_at']) if item['created_at'] else None,
                        updated_at=datetime.fromisoformat(item['updated_at']) if item['updated_at'] else None
                    )
                    db.session.add(new_item)
                    print(f"  ✓ Migrated track item: {item['lot_number']}")
            
            db.session.commit()
            
            # Migrate Inspections
            sqlite_cursor.execute("SELECT * FROM inspections")
            inspections = sqlite_cursor.fetchall()
            
            for insp in inspections:
                new_inspection = Inspection(
                    track_item_id=insp['track_item_id'],
                    inspection_type=insp['inspection_type'],
                    inspection_date=datetime.fromisoformat(insp['inspection_date']).date() if insp['inspection_date'] else None,
                    inspector_name=insp['inspector_name'],
                    inspector_designation=insp['inspector_designation'],
                    inspection_status=insp['inspection_status'],
                    quality_grade=insp['quality_grade'],
                    remarks=insp['remarks'],
                    defects_found=insp['defects_found'],
                    action_taken=insp['action_taken'],
                    next_inspection_due=datetime.fromisoformat(insp['next_inspection_due']).date() if insp['next_inspection_due'] else None,
                    document_references=insp['document_references'],
                    created_by_id=insp['created_by_id'],
                    created_at=datetime.fromisoformat(insp['created_at']) if insp['created_at'] else None
                )
                db.session.add(new_inspection)
                print(f"  ✓ Migrated inspection: {insp['inspection_type']} - {insp['track_item_id']}")
            
            db.session.commit()
            
            print("✓ Data migration completed successfully!")
            
        sqlite_conn.close()
        
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main migration function"""
    print("=" * 60)
    print("🗄️  PostgreSQL Migration Script")
    print("=" * 60)
    
    # Step 1: Create tables
    create_tables()
    
    # Step 2: Create default admin
    create_default_admin()
    
    # Step 3: Migrate data (optional)
    migrate_sqlite_data()
    
    print("=" * 60)
    print("✅ Migration completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Update .env with your PostgreSQL DATABASE_URL")
    print("2. Run: python app.py")
    print("3. Test at: http://localhost:5000")
    print("4. Login with: admin / Admin@123")

if __name__ == '__main__':
    main()
