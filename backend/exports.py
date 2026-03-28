"""
Export Routes - CSV and PDF Export for Vendors and Track Items
"""
import io
import csv
from datetime import datetime
from flask import Blueprint, request, jsonify, send_file, make_response
from flask_jwt_extended import jwt_required
from werkzeug.exceptions import NotFound

from extensions import db, limiter
from models import Vendor, TrackItem, Inspection

exports_bp = Blueprint('exports', __name__)


# ============== CSV Export Functions ==============

def export_vendors_to_csv(vendors):
    """Convert vendors list to CSV format"""
    output = io.StringIO()
    fieldnames = [
        'id', 'vendor_name', 'vendor_code', 'contact_person', 'contact_email',
        'contact_phone', 'address_line1', 'city', 'state', 'postal_code',
        'country', 'tax_id', 'certification_status', 'performance_rating',
        'is_approved', 'created_at'
    ]
    
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    
    for vendor in vendors:
        row = {
            'id': vendor.id,
            'vendor_name': vendor.vendor_name,
            'vendor_code': vendor.vendor_code,
            'contact_person': vendor.contact_person,
            'contact_email': vendor.contact_email,
            'contact_phone': vendor.contact_phone,
            'address_line1': vendor.address_line1,
            'city': vendor.city,
            'state': vendor.state,
            'postal_code': vendor.postal_code,
            'country': vendor.country,
            'tax_id': vendor.tax_id,
            'certification_status': vendor.certification_status,
            'performance_rating': vendor.performance_rating,
            'is_approved': vendor.is_approved,
            'created_at': vendor.created_at.isoformat() if vendor.created_at else ''
        }
        writer.writerow(row)
    
    output.seek(0)
    return output.getvalue()


def export_track_items_to_csv(items):
    """Convert track items list to CSV format"""
    output = io.StringIO()
    fieldnames = [
        'id', 'item_type', 'lot_number', 'vendor_id', 'vendor_name', 'quantity',
        'manufacture_date', 'supply_date', 'installation_date', 'warranty_expiry_date',
        'status', 'performance_status', 'defect_count', 'replacement_count',
        'installation_location', 'section_name', 'division', 'zone', 'created_at'
    ]
    
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    
    for item in items:
        row = {
            'id': item.id,
            'item_type': item.item_type,
            'lot_number': item.lot_number,
            'vendor_id': item.vendor_id,
            'vendor_name': item.vendor.vendor_name if item.vendor else '',
            'quantity': item.quantity,
            'manufacture_date': item.manufacture_date.isoformat() if item.manufacture_date else '',
            'supply_date': item.supply_date.isoformat() if item.supply_date else '',
            'installation_date': item.installation_date.isoformat() if item.installation_date else '',
            'warranty_expiry_date': item.warranty_expiry_date.isoformat() if item.warranty_expiry_date else '',
            'status': item.status,
            'performance_status': item.performance_status,
            'defect_count': item.defect_count,
            'replacement_count': item.replacement_count,
            'installation_location': item.installation_location,
            'section_name': item.section_name,
            'division': item.division,
            'zone': item.zone,
            'created_at': item.created_at.isoformat() if item.created_at else ''
        }
        writer.writerow(row)
    
    output.seek(0)
    return output.getvalue()


# ============== CSV Export Endpoints ==============

@exports_bp.route('/api/export/vendors/csv', methods=['GET'])
@jwt_required()
@limiter.limit("30 per hour")
def export_vendors_csv():
    """Export vendors list to CSV"""
    try:
        # Get filters from query params
        item_type = request.args.get('item_type')
        status = request.args.get('status')
        
        query = Vendor.query
        if item_type:
            query = query.filter_by(item_type=item_type)
        if status:
            query = query.filter_by(status=status)
        
        vendors = query.all()
        
        csv_data = export_vendors_to_csv(vendors)
        
        # Create response
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        response = make_response(csv_data)
        response.headers['Content-Disposition'] = f'attachment; filename=vendors_export_{timestamp}.csv'
        response.headers['Content-Type'] = 'text/csv'
        
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@exports_bp.route('/api/export/track-items/csv', methods=['GET'])
@jwt_required()
@limiter.limit("30 per hour")
def export_track_items_csv():
    """Export track items list to CSV"""
    try:
        # Get filters from query params
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
        
        items = query.all()
        
        csv_data = export_track_items_to_csv(items)
        
        # Create response
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        response = make_response(csv_data)
        response.headers['Content-Disposition'] = f'attachment; filename=track_items_export_{timestamp}.csv'
        response.headers['Content-Type'] = 'text/csv'
        
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============== PDF Export Functions ==============

def create_vendor_pdf(vendor_data, inspections=None, ai_analysis=None):
    """Create PDF report for vendor"""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=0.75*inch,
                           leftMargin=0.75*inch,
                           topMargin=0.75*inch,
                           bottomMargin=0.75*inch)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    elements.append(Paragraph("Vendor Report", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Vendor Info Table
    vendor_info = [
        ['Vendor ID:', vendor_data.get('id', 'N/A')],
        ['Vendor Name:', vendor_data.get('vendor_name', 'N/A')],
        ['Vendor Code:', vendor_data.get('vendor_code', 'N/A')],
        ['Contact Person:', vendor_data.get('contact_person', 'N/A')],
        ['Email:', vendor_data.get('contact_email', 'N/A')],
        ['Phone:', vendor_data.get('contact_phone', 'N/A')],
        ['Address:', f"{vendor_data.get('address_line1', '')}, {vendor_data.get('city', '')}, {vendor_data.get('state', '')} {vendor_data.get('postal_code', '')}"],
        ['Country:', vendor_data.get('country', 'N/A')],
        ['Tax ID:', vendor_data.get('tax_id', 'N/A')],
        ['Certification:', vendor_data.get('certification_status', 'N/A')],
        ['Performance Rating:', f"{vendor_data.get('performance_rating', 'N/A')}/5.0"],
        ['Approved:', 'Yes' if vendor_data.get('is_approved') else 'No'],
    ]
    
    vendor_table = Table(vendor_info, colWidths=[2*inch, 4*inch])
    vendor_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
    ]))
    
    elements.append(vendor_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # AI Analysis Section
    if ai_analysis:
        elements.append(Paragraph("AI Risk Assessment", styles['Heading2']))
        elements.append(Spacer(1, 0.1*inch))
        
        # Risk Score
        risk_score = ai_analysis.get('risk_score', 0)
        risk_color = colors.red if risk_score >= 70 else colors.orange if risk_score >= 40 else colors.green
        risk_level = 'High' if risk_score >= 70 else 'Medium' if risk_score >= 40 else 'Low'
        
        risk_info = [
            ['Risk Score:', f"{risk_score}/100"],
            ['Risk Level:', risk_level],
        ]
        
        risk_table = Table(risk_info, colWidths=[2*inch, 4*inch])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
            ('BACKGROUND', (1, 0), (1, 0), risk_color),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ]))
        
        elements.append(risk_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Flags
        if ai_analysis.get('flags'):
            elements.append(Paragraph("Risk Flags", styles['Heading3']))
            for flag in ai_analysis['flags']:
                elements.append(Paragraph(f"• {flag}", styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
        
        # Recommendations
        if ai_analysis.get('recommendations'):
            elements.append(Paragraph("Recommendations", styles['Heading3']))
            for rec in ai_analysis['recommendations']:
                elements.append(Paragraph(f"• {rec}", styles['Normal']))
        
        elements.append(Spacer(1, 0.2*inch))
    
    # Inspections Section
    if inspections and len(inspections) > 0:
        elements.append(Paragraph("Inspection History", styles['Heading2']))
        elements.append(Spacer(1, 0.1*inch))
        
        insp_data = [['Date', 'Type', 'Status', 'Grade', 'Inspector']]
        for insp in inspections:
            insp_data.append([
                insp.get('inspection_date', 'N/A'),
                insp.get('inspection_type', 'N/A'),
                insp.get('inspection_status', 'N/A'),
                insp.get('quality_grade', 'N/A'),
                insp.get('inspector_name', 'N/A')
            ])
        
        insp_table = Table(insp_data, colWidths=[1.2*inch, 1.2*inch, 1*inch, 0.8*inch, 1.8*inch])
        insp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ]))
        
        elements.append(insp_table)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer


def create_track_item_pdf(item_data, inspections=None, ai_analysis=None):
    """Create PDF report for track item"""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.enums import TA_CENTER
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=0.75*inch,
                           leftMargin=0.75*inch,
                           topMargin=0.75*inch,
                           bottomMargin=0.75*inch)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    item_type_display = item_data.get('item_type', 'Track Item').replace('_', ' ').title()
    elements.append(Paragraph(f"{item_type_display} Report", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Item Info Table
    item_info = [
        ['Item ID:', item_data.get('id', 'N/A')],
        ['Lot Number:', item_data.get('lot_number', 'N/A')],
        ['Item Type:', item_type_display],
        ['Vendor:', item_data.get('vendor_name', item_data.get('vendor_id', 'N/A'))],
        ['Quantity:', str(item_data.get('quantity', 'N/A'))],
        ['Manufacture Date:', item_data.get('manufacture_date', 'N/A')],
        ['Supply Date:', item_data.get('supply_date', 'N/A')],
        ['Installation Date:', item_data.get('installation_date', 'N/A')],
        ['Warranty Expiry:', item_data.get('warranty_expiry_date', 'N/A')],
        ['Status:', item_data.get('status', 'N/A').replace('_', ' ').title()],
        ['Performance:', item_data.get('performance_status', 'N/A').replace('_', ' ').title()],
        ['Defect Count:', str(item_data.get('defect_count', 0))],
        ['Location:', item_data.get('installation_location', 'N/A')],
        ['Section:', f"{item_data.get('section_name', 'N/A')}, {item_data.get('division', 'N/A')}, {item_data.get('zone', 'N/A')}"],
    ]
    
    item_table = Table(item_info, colWidths=[2*inch, 4*inch])
    item_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
    ]))
    
    elements.append(item_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # AI Analysis Section
    if ai_analysis:
        elements.append(Paragraph("AI Quality Assessment", styles['Heading2']))
        elements.append(Spacer(1, 0.1*inch))
        
        risk_score = ai_analysis.get('risk_score', 0)
        risk_color = colors.red if risk_score >= 70 else colors.orange if risk_score >= 40 else colors.green
        risk_level = 'High Risk' if risk_score >= 70 else 'Medium Risk' if risk_score >= 40 else 'Low Risk'
        
        risk_info = [
            ['Risk Score:', f"{risk_score}/100"],
            ['Risk Level:', risk_level],
        ]
        
        risk_table = Table(risk_info, colWidths=[2*inch, 4*inch])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
            ('BACKGROUND', (1, 0), (1, 0), risk_color),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ]))
        
        elements.append(risk_table)
        elements.append(Spacer(1, 0.2*inch))
        
        if ai_analysis.get('flags'):
            elements.append(Paragraph("Exceptions Detected", styles['Heading3']))
            for flag in ai_analysis['flags']:
                elements.append(Paragraph(f"• {flag}", styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
        
        if ai_analysis.get('recommendations'):
            elements.append(Paragraph("Recommendations", styles['Heading3']))
            for rec in ai_analysis['recommendations']:
                elements.append(Paragraph(f"• {rec}", styles['Normal']))
        
        elements.append(Spacer(1, 0.2*inch))
    
    # Inspections Section
    if inspections and len(inspections) > 0:
        elements.append(Paragraph("Inspection History", styles['Heading2']))
        elements.append(Spacer(1, 0.1*inch))
        
        insp_data = [['Date', 'Type', 'Status', 'Grade', 'Inspector']]
        for insp in inspections:
            insp_data.append([
                insp.get('inspection_date', 'N/A'),
                insp.get('inspection_type', 'N/A'),
                insp.get('inspection_status', 'N/A'),
                insp.get('quality_grade', 'N/A'),
                insp.get('inspector_name', 'N/A')
            ])
        
        insp_table = Table(insp_data, colWidths=[1.2*inch, 1.2*inch, 1*inch, 0.8*inch, 1.8*inch])
        insp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ]))
        
        elements.append(insp_table)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer


# ============== PDF Export Endpoints ==============

@exports_bp.route('/api/export/vendors/<vendor_id>/pdf', methods=['GET'])
@jwt_required()
@limiter.limit("30 per hour")
def export_vendor_pdf(vendor_id):
    """Export vendor details as PDF"""
    try:
        vendor = Vendor.query.get(vendor_id)
        if not vendor:
            raise NotFound(f"Vendor with ID {vendor_id} not found")
        
        vendor_data = vendor.to_dict()
        
        # Get AI analysis (import here to avoid circular imports)
        from railway_ai import detect_exceptions
        inspections = [insp.to_dict() for insp in vendor.inspections.all()] if hasattr(vendor, 'inspections') else []
        ai_analysis = detect_exceptions(vendor_data, inspections, vendor_data)
        
        pdf_buffer = create_vendor_pdf(vendor_data, inspections, ai_analysis)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f'vendor_{vendor_id}_report_{timestamp}.pdf',
            mimetype='application/pdf'
        )
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@exports_bp.route('/api/export/track-items/<item_id>/pdf', methods=['GET'])
@jwt_required()
@limiter.limit("30 per hour")
def export_track_item_pdf(item_id):
    """Export track item details as PDF"""
    try:
        item = TrackItem.query.get(item_id)
        if not item:
            raise NotFound(f"Track item with ID {item_id} not found")
        
        item_data = item.to_dict()
        item_data['vendor_name'] = item.vendor.vendor_name if item.vendor else item.vendor_id
        
        # Get AI analysis
        from railway_ai import detect_exceptions
        inspections = [insp.to_dict() for insp in item.inspections.all()]
        vendor_info = item.vendor.to_dict() if item.vendor else None
        ai_analysis = detect_exceptions(item_data, inspections, vendor_info)
        
        pdf_buffer = create_track_item_pdf(item_data, inspections, ai_analysis)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f'track_item_{item_id}_report_{timestamp}.pdf',
            mimetype='application/pdf'
        )
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
