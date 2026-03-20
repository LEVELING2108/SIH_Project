"""
API Routes for Railway Track Items (Clips, Pads, Liners, Sleepers)
"""
import json
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import BadRequest, NotFound

from extensions import db, limiter
from models import TrackItem, Vendor, Inspection
from railway_ai import generate_ai_report, detect_exceptions

track_items_bp = Blueprint('track_items', __name__)


@track_items_bp.route('/api/track-items', methods=['GET'])
@jwt_required()
@limiter.limit("100 per hour")
def get_track_items():
    """Get all track items with optional filtering and pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    item_type = request.args.get('item_type')
    status = request.args.get('status')
    vendor_id = request.args.get('vendor_id')

    query = TrackItem.query

    if item_type:
        query = query.filter_by(item_type=item_type)
    if status:
        query = query.filter_by(status=status)
    if vendor_id:
        query = query.filter_by(vendor_id=vendor_id)

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    items = pagination.items

    result = [item.to_dict() for item in items]

    return jsonify({
        "track_items": result,
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": page
    }), 200


@track_items_bp.route('/api/track-items/<item_id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per hour")
def get_track_item(item_id):
    """Get a specific track item by ID with AI analysis"""
    item = TrackItem.query.get(item_id)
    if not item:
        raise NotFound(f"Track item with ID {item_id} not found")

    item_data = item.to_dict()

    # Get inspections
    inspections = [insp.to_dict() for insp in item.inspections.all()]

    # Get vendor info
    vendor_info = item.vendor.to_dict() if item.vendor else None

    # Generate AI report
    ai_analysis = detect_exceptions(item_data, inspections, vendor_info)

    return jsonify({
        **item_data,
        'inspections': inspections,
        'ai_analysis': ai_analysis
    }), 200


@track_items_bp.route('/api/track-items', methods=['POST'])
@jwt_required()
@limiter.limit("30 per hour")
def create_track_item():
    """Create a new track item"""
    data = request.get_json()

    if not data:
        raise BadRequest("No data provided")

    required_fields = ['id', 'item_type', 'lot_number', 'vendor_id', 'quantity', 'manufacture_date']
    for field in required_fields:
        if field not in data:
            raise BadRequest(f"Missing required field: {field}")

    # Check if item already exists
    existing = TrackItem.query.get(data['id'])
    if existing:
        raise BadRequest(f"Track item with ID {data['id']} already exists")

    # Check if vendor exists
    vendor = Vendor.query.get(data['vendor_id'])
    if not vendor:
        raise BadRequest(f"Vendor with ID {data['vendor_id']} not found")

    current_user_id = int(get_jwt_identity())

    # Calculate warranty dates if provided
    warranty_start = None
    warranty_expiry = None
    if data.get('supply_date'):
        warranty_start = datetime.strptime(data['supply_date'], '%Y-%m-%d').date()
        warranty_years = data.get('warranty_period_years', 5)
        from dateutil.relativedelta import relativedelta
        warranty_expiry = warranty_start + relativedelta(years=warranty_years)

    item = TrackItem(
        id=data['id'],
        item_type=data['item_type'],
        lot_number=data['lot_number'],
        vendor_id=data['vendor_id'],
        quantity=data['quantity'],
        manufacture_date=data['manufacture_date'],
        supply_date=data.get('supply_date'),
        installation_date=data.get('installation_date'),
        warranty_period_years=data.get('warranty_period_years', 5),
        warranty_start_date=warranty_start,
        warranty_expiry_date=warranty_expiry,
        installation_location=data.get('installation_location'),
        kilometer_from=data.get('kilometer_from'),
        kilometer_to=data.get('kilometer_to'),
        section_name=data.get('section_name'),
        division=data.get('division'),
        zone=data.get('zone'),
        status=data.get('status', 'in_stock'),
        performance_status=data.get('performance_status', 'good'),
        specifications=data.get('specifications'),
        details=data.get('details'),
        notes=data.get('notes'),
        created_by_id=current_user_id
    )

    db.session.add(item)
    db.session.commit()

    return jsonify({
        "message": "Track item created successfully",
        "track_item": item.to_dict()
    }), 201


@track_items_bp.route('/api/track-items/<item_id>', methods=['PUT'])
@jwt_required()
@limiter.limit("30 per hour")
def update_track_item(item_id):
    """Update a track item"""
    item = TrackItem.query.get(item_id)
    if not item:
        raise NotFound(f"Track item with ID {item_id} not found")

    data = request.get_json()
    if not data:
        raise BadRequest("No data provided")

    # Update fields
    updatable_fields = [
        'quantity', 'supply_date', 'installation_date', 'installation_location',
        'kilometer_from', 'kilometer_to', 'section_name', 'division', 'zone',
        'status', 'performance_status', 'defect_count', 'replacement_count',
        'specifications', 'details', 'notes', 'warranty_period_years'
    ]

    for field in updatable_fields:
        if field in data:
            setattr(item, field, data[field])

    # Recalculate warranty if supply_date or warranty_period changed
    if 'supply_date' in data or 'warranty_period_years' in data:
        if item.supply_date:
            from dateutil.relativedelta import relativedelta
            item.warranty_start_date = item.supply_date
            item.warranty_expiry_date = item.supply_date + relativedelta(years=item.warranty_period_years)

    db.session.commit()

    return jsonify({
        "message": "Track item updated successfully",
        "track_item": item.to_dict()
    }), 200


@track_items_bp.route('/api/track-items/<item_id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("20 per hour")
def delete_track_item(item_id):
    """Delete a track item"""
    item = TrackItem.query.get(item_id)
    if not item:
        raise NotFound(f"Track item with ID {item_id} not found")

    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": "Track item deleted successfully"}), 200


# ============== Inspection Endpoints ==============

@track_items_bp.route('/api/track-items/<item_id>/inspections', methods=['GET'])
@jwt_required()
@limiter.limit("100 per hour")
def get_inspections(item_id):
    """Get all inspections for a track item"""
    item = TrackItem.query.get(item_id)
    if not item:
        raise NotFound(f"Track item with ID {item_id} not found")

    inspections = [insp.to_dict() for insp in item.inspections.order_by(Inspection.inspection_date.desc()).all()]

    return jsonify({"inspections": inspections}), 200


@track_items_bp.route('/api/track-items/<item_id>/inspections', methods=['POST'])
@jwt_required()
@limiter.limit("30 per hour")
def create_inspection(item_id):
    """Create a new inspection record"""
    item = TrackItem.query.get(item_id)
    if not item:
        raise NotFound(f"Track item with ID {item_id} not found")

    data = request.get_json()
    if not data:
        raise BadRequest("No data provided")

    required_fields = ['inspection_type', 'inspection_date', 'inspection_status']
    for field in required_fields:
        if field not in data:
            raise BadRequest(f"Missing required field: {field}")

    current_user_id = int(get_jwt_identity())

    inspection = Inspection(
        track_item_id=item_id,
        inspection_type=data['inspection_type'],
        inspection_date=data['inspection_date'],
        inspector_name=data.get('inspector_name'),
        inspector_designation=data.get('inspector_designation'),
        inspection_status=data['inspection_status'],
        quality_grade=data.get('quality_grade'),
        remarks=data.get('remarks'),
        defects_found=data.get('defects_found'),
        action_taken=data.get('action_taken'),
        next_inspection_due=data.get('next_inspection_due'),
        document_references=data.get('document_references'),
        created_by_id=current_user_id
    )

    # Update item defect count if failed
    if data['inspection_status'] == 'failed':
        item.defect_count += 1
        item.performance_status = 'poor' if item.defect_count < 3 else 'failed'

    db.session.add(inspection)
    db.session.commit()

    return jsonify({
        "message": "Inspection created successfully",
        "inspection": inspection.to_dict()
    }), 201


# ============== QR Code & Scanning Endpoints ==============

@track_items_bp.route('/api/track-items/<item_id>/qr', methods=['GET'])
@jwt_required()
@limiter.limit("50 per hour")
def get_track_item_qr(item_id):
    """Generate QR code for a track item"""
    import qrcode
    import io
    import base64

    item = TrackItem.query.get(item_id)
    if not item:
        raise NotFound(f"Track item with ID {item_id} not found")

    # Create comprehensive QR data
    qr_data = {
        'id': item.id,
        'item_type': item.item_type,
        'lot_number': item.lot_number,
        'vendor_id': item.vendor_id,
        'manufacture_date': item.manufacture_date.isoformat() if item.manufacture_date else None,
        'supply_date': item.supply_date.isoformat() if item.supply_date else None,
        'warranty_expiry': item.warranty_expiry_date.isoformat() if item.warranty_expiry_date else None,
        'quantity': item.quantity,
        'status': item.status
    }

    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(json.dumps(qr_data))
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Convert to base64
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode()

    return jsonify({
        "qr_code": f"data:image/png;base64,{img_base64}",
        "qr_data": qr_data
    }), 200


@track_items_bp.route('/api/scan-track-item', methods=['POST'])
@jwt_required()
@limiter.limit("50 per hour")
def scan_track_item():
    """Scan QR code and get comprehensive AI-powered report"""
    data = request.get_json()
    if not data or 'qr_data' not in data:
        raise BadRequest("QR data required")

    qr_data = data['qr_data']

    # Parse QR data (could be string or dict)
    if isinstance(qr_data, str):
        try:
            qr_data = json.loads(qr_data)
        except:
            raise BadRequest("Invalid QR data format")

    item_id = qr_data.get('id')
    if not item_id:
        raise BadRequest("Invalid QR code: missing item ID")

    # Get full item details
    item = TrackItem.query.get(item_id)
    if not item:
        raise NotFound(f"Track item not found")

    item_data = item.to_dict()

    # Get inspections
    inspections = [insp.to_dict() for insp in item.inspections.all()]

    # Get vendor info
    vendor_info = item.vendor.to_dict() if item.vendor else None

    # Generate comprehensive AI report
    report = generate_ai_report(item_data, inspections, vendor_info)

    return jsonify(report), 200


# ============== Analytics & Dashboard Endpoints ==============

@track_items_bp.route('/api/track-items/analytics', methods=['GET'])
@jwt_required()
@limiter.limit("50 per hour")
def get_track_items_analytics():
    """Get analytics for railway dashboard"""
    # Count by item type
    from sqlalchemy import func

    item_type_counts = db.session.query(
        TrackItem.item_type,
        func.count(TrackItem.id).label('count')
    ).group_by(TrackItem.item_type).all()

    # Count by status
    status_counts = db.session.query(
        TrackItem.status,
        func.count(TrackItem.id).label('count')
    ).group_by(TrackItem.status).all()

    # Performance status
    performance_counts = db.session.query(
        TrackItem.performance_status,
        func.count(TrackItem.id).label('count')
    ).group_by(TrackItem.performance_status).all()

    # Warranty expiring soon (next 90 days)
    from datetime import date, timedelta
    expiring_soon = TrackItem.query.filter(
        TrackItem.warranty_expiry_date <= date.today() + timedelta(days=90),
        TrackItem.warranty_expiry_date >= date.today()
    ).count()

    # Expired warranties
    expired = TrackItem.query.filter(
        TrackItem.warranty_expiry_date < date.today()
    ).count()

    # Total quantities by type
    total_quantities = db.session.query(
        TrackItem.item_type,
        func.sum(TrackItem.quantity).label('total')
    ).group_by(TrackItem.item_type).all()

    # Recent defects
    recent_defective = TrackItem.query.filter(
        TrackItem.defect_count > 0
    ).order_by(TrackItem.updated_at.desc()).limit(10).all()

    return jsonify({
        "total_items": TrackItem.query.count(),
        "item_type_distribution": [{"type": t, "count": c} for t, c in item_type_counts],
        "status_distribution": [{"status": s, "count": c} for s, c in status_counts],
        "performance_distribution": [{"status": p, "count": c} for p, c in performance_counts],
        "warranty_alerts": {
            "expiring_soon": expiring_soon,
            "expired": expired
        },
        "total_quantities": [{"type": t, "quantity": int(q)} for t, q in total_quantities],
        "recent_defects": [item.to_dict() for item in recent_defective]
    }), 200


@track_items_bp.route('/api/track-items/exceptions', methods=['GET'])
@jwt_required()
@limiter.limit("50 per hour")
def get_exceptions():
    """Get all items requiring attention (exceptions)"""
    from datetime import date, timedelta

    exceptions_list = []

    # 1. Warranty expiring/expired
    expiring = TrackItem.query.filter(
        TrackItem.warranty_expiry_date <= date.today() + timedelta(days=90)
    ).all()

    for item in expiring:
        item_data = item.to_dict()
        inspections = [insp.to_dict() for insp in item.inspections.all()]
        vendor_info = item.vendor.to_dict() if item.vendor else None
        analysis = detect_exceptions(item_data, inspections, vendor_info)

        if analysis['exceptions_count'] > 0:
            exceptions_list.append({
                'item': item_data,
                'analysis': analysis
            })

    # 2. Items with defects
    defective = TrackItem.query.filter(TrackItem.defect_count > 0).all()
    for item in defective:
        if item not in expiring:  # Avoid duplicates
            item_data = item.to_dict()
            inspections = [insp.to_dict() for insp in item.inspections.all()]
            vendor_info = item.vendor.to_dict() if item.vendor else None
            analysis = detect_exceptions(item_data, inspections, vendor_info)

            if analysis['exceptions_count'] > 0:
                exceptions_list.append({
                    'item': item_data,
                    'analysis': analysis
                })

    # Sort by risk score
    exceptions_list.sort(key=lambda x: x['analysis']['risk_score'], reverse=True)

    return jsonify({
        "exceptions_count": len(exceptions_list),
        "exceptions": exceptions_list[:50]  # Limit to top 50
    }), 200
