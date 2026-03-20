"""
Database models for Vendor Verification System
"""
from datetime import datetime, date as dt_date
import bcrypt
from extensions import db
from sqlalchemy.types import TypeDecorator, Date as SQLDate


class AcceptsDateString(TypeDecorator):
    """
    Accept both Python `date` objects and ISO date strings (YYYY-MM-DD)
    for SQLAlchemy Date columns (useful for tests/JSON payloads).
    """

    impl = SQLDate
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None

        if isinstance(value, dt_date) and not isinstance(value, datetime):
            return value

        if isinstance(value, datetime):
            return value.date()

        if isinstance(value, str):
            # Expected ISO format: 'YYYY-MM-DD'
            return datetime.fromisoformat(value).date()

        return value


class User(db.Model):
    """User model for authentication and authorization"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)  # admin, user, viewer
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        """Hash and set password"""
        salt = bcrypt.gensalt(rounds=12)
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
        db.session.commit()

    def to_dict(self):
        """Convert user to dictionary (excluding sensitive data)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

    def __repr__(self):
        return f'<User {self.username}>'


class Vendor(db.Model):
    """Vendor model representing vendor/manufacturer data"""
    __tablename__ = 'vendor_data'

    id = db.Column(db.String(50), primary_key=True)
    vendor_name = db.Column(db.String(255), nullable=False)
    contact_person = db.Column(db.String(100))
    contact_email = db.Column(db.String(255))
    contact_phone = db.Column(db.String(20))
    address_line1 = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100), default='India')
    tax_id = db.Column(db.String(50))
    bank_account = db.Column(db.String(50))

    # Railway-specific fields
    vendor_code = db.Column(db.String(50), unique=True)  # UDM portal vendor code
    certification_status = db.Column(db.String(50), default='pending')  # approved, pending, blacklisted
    performance_rating = db.Column(db.Float, default=0.0)  # 0-5 rating
    is_approved = db.Column(db.Boolean, default=False)
    approval_date = db.Column(AcceptsDateString)

    # Relationships
    track_items = db.relationship('TrackItem', backref='vendor', lazy='dynamic')

    # Audit fields
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Indexes
    __table_args__ = (
        db.Index('idx_vendor_name', 'vendor_name'),
        db.Index('idx_vendor_code', 'vendor_code'),
        db.Index('idx_certification_status', 'certification_status'),
    )

    def to_dict(self):
        """Convert vendor to dictionary"""
        return {
            'id': self.id,
            'vendor_name': self.vendor_name,
            'vendor_code': self.vendor_code,
            'contact_person': self.contact_person,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'address_line1': self.address_line1,
            'city': self.city,
            'state': self.state,
            'postal_code': self.postal_code,
            'country': self.country,
            'tax_id': self.tax_id,
            'bank_account': self.bank_account,
            'certification_status': self.certification_status,
            'performance_rating': self.performance_rating,
            'is_approved': self.is_approved,
            'approval_date': self.approval_date.isoformat() if self.approval_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Vendor {self.vendor_name}>'


class TrackItem(db.Model):
    """Track fitting items - Elastic Rail Clips, Rail Pads, Liners, Sleepers"""
    __tablename__ = 'track_items'

    id = db.Column(db.String(50), primary_key=True)  # Unique item/lot ID
    item_type = db.Column(db.String(50), nullable=False)  # elastic_rail_clip, rail_pad, liner, sleeper
    lot_number = db.Column(db.String(100), nullable=False, unique=True)

    # Vendor information
    vendor_id = db.Column(db.String(50), db.ForeignKey('vendor_data.id'), nullable=False)

    # Quantity and dates
    quantity = db.Column(db.Integer, nullable=False)
    manufacture_date = db.Column(AcceptsDateString, nullable=False)
    supply_date = db.Column(AcceptsDateString)
    installation_date = db.Column(AcceptsDateString)

    # Warranty information
    warranty_period_years = db.Column(db.Integer, default=5)
    warranty_start_date = db.Column(AcceptsDateString)
    warranty_expiry_date = db.Column(AcceptsDateString)

    # Location information
    installation_location = db.Column(db.String(255))  # Track section
    kilometer_from = db.Column(db.Float)
    kilometer_to = db.Column(db.Float)
    section_name = db.Column(db.String(100))
    division = db.Column(db.String(100))
    zone = db.Column(db.String(100))

    # Status and performance
    status = db.Column(db.String(50), default='in_stock')  # in_stock, installed, in_service, defective, replaced
    performance_status = db.Column(db.String(50), default='good')  # good, average, poor, failed
    defect_count = db.Column(db.Integer, default=0)
    replacement_count = db.Column(db.Integer, default=0)

    # Technical specifications (JSON field for flexibility)
    specifications = db.Column(db.Text)  # JSON string with technical specs

    # Additional details
    details = db.Column(db.Text)
    notes = db.Column(db.Text)

    # Relationships
    inspections = db.relationship('Inspection', backref='track_item', lazy='dynamic', cascade='all, delete-orphan')

    # Audit fields
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Indexes
    __table_args__ = (
        db.Index('idx_item_type', 'item_type'),
        db.Index('idx_lot_number', 'lot_number'),
        db.Index('idx_vendor_id', 'vendor_id'),
        db.Index('idx_status', 'status'),
        db.Index('idx_warranty_expiry', 'warranty_expiry_date'),
        db.Index('idx_section', 'section_name'),
    )

    def to_dict(self):
        """Convert track item to dictionary"""
        return {
            'id': self.id,
            'item_type': self.item_type,
            'lot_number': self.lot_number,
            'vendor_id': self.vendor_id,
            'vendor_name': self.vendor.vendor_name if self.vendor else None,
            'quantity': self.quantity,
            'manufacture_date': self.manufacture_date.isoformat() if self.manufacture_date else None,
            'supply_date': self.supply_date.isoformat() if self.supply_date else None,
            'installation_date': self.installation_date.isoformat() if self.installation_date else None,
            'warranty_period_years': self.warranty_period_years,
            'warranty_start_date': self.warranty_start_date.isoformat() if self.warranty_start_date else None,
            'warranty_expiry_date': self.warranty_expiry_date.isoformat() if self.warranty_expiry_date else None,
            'installation_location': self.installation_location,
            'kilometer_from': self.kilometer_from,
            'kilometer_to': self.kilometer_to,
            'section_name': self.section_name,
            'division': self.division,
            'zone': self.zone,
            'status': self.status,
            'performance_status': self.performance_status,
            'defect_count': self.defect_count,
            'replacement_count': self.replacement_count,
            'specifications': self.specifications,
            'details': self.details,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<TrackItem {self.lot_number} - {self.item_type}>'


class Inspection(db.Model):
    """Multi-stage inspection records for track items"""
    __tablename__ = 'inspections'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    track_item_id = db.Column(db.String(50), db.ForeignKey('track_items.id'), nullable=False)

    # Inspection details
    inspection_type = db.Column(db.String(50), nullable=False)  # manufacturing, supply, installation, periodic, defect
    inspection_date = db.Column(AcceptsDateString, nullable=False)
    inspector_name = db.Column(db.String(100))
    inspector_designation = db.Column(db.String(100))

    # Results
    inspection_status = db.Column(db.String(50), nullable=False)  # passed, failed, conditional, pending
    quality_grade = db.Column(db.String(20))  # A, B, C, D, F
    remarks = db.Column(db.Text)
    defects_found = db.Column(db.Text)  # JSON array of defects

    # Actions taken
    action_taken = db.Column(db.String(255))
    next_inspection_due = db.Column(AcceptsDateString)

    # Documents/photos
    document_references = db.Column(db.Text)  # JSON array of document URLs/IDs

    # Audit fields
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Indexes
    __table_args__ = (
        db.Index('idx_track_item_id', 'track_item_id'),
        db.Index('idx_inspection_type', 'inspection_type'),
        db.Index('idx_inspection_date', 'inspection_date'),
        db.Index('idx_inspection_status', 'inspection_status'),
    )

    def to_dict(self):
        """Convert inspection to dictionary"""
        return {
            'id': self.id,
            'track_item_id': self.track_item_id,
            'inspection_type': self.inspection_type,
            'inspection_date': self.inspection_date.isoformat() if self.inspection_date else None,
            'inspector_name': self.inspector_name,
            'inspector_designation': self.inspector_designation,
            'inspection_status': self.inspection_status,
            'quality_grade': self.quality_grade,
            'remarks': self.remarks,
            'defects_found': self.defects_found,
            'action_taken': self.action_taken,
            'next_inspection_due': self.next_inspection_due.isoformat() if self.next_inspection_due else None,
            'document_references': self.document_references,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Inspection {self.inspection_type} - {self.track_item_id}>'
