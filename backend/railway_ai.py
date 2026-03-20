"""
AI-Powered Exception Detection and Analysis for Railway Track Fittings
Monitors quality, warranty, inspections, and generates actionable insights
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any
import json


def calculate_warranty_status(warranty_expiry_date) -> Dict[str, Any]:
    """Calculate warranty status and alert level"""
    if not warranty_expiry_date:
        return {
            'status': 'unknown',
            'days_remaining': None,
            'alert_level': 'high',
            'message': 'Warranty expiry date not set'
        }

    today = datetime.now().date()
    if isinstance(warranty_expiry_date, str):
        warranty_expiry_date = datetime.fromisoformat(warranty_expiry_date).date()

    days_remaining = (warranty_expiry_date - today).days

    if days_remaining < 0:
        return {
            'status': 'expired',
            'days_remaining': days_remaining,
            'alert_level': 'critical',
            'message': f'Warranty expired {abs(days_remaining)} days ago'
        }
    elif days_remaining <= 30:
        return {
            'status': 'expiring_soon',
            'days_remaining': days_remaining,
            'alert_level': 'high',
            'message': f'Warranty expiring in {days_remaining} days'
        }
    elif days_remaining <= 90:
        return {
            'status': 'warning',
            'days_remaining': days_remaining,
            'alert_level': 'medium',
            'message': f'Warranty expires in {days_remaining} days'
        }
    else:
        return {
            'status': 'active',
            'days_remaining': days_remaining,
            'alert_level': 'low',
            'message': f'Warranty valid for {days_remaining} days'
        }


def check_inspection_compliance(track_item, inspections) -> Dict[str, Any]:
    """Check if inspections are up-to-date and compliant"""
    exceptions = []
    missing_inspections = []
    overdue_inspections = []

    # Expected inspection types based on item status
    required_inspections = {
        'in_stock': ['manufacturing', 'supply'],
        'installed': ['manufacturing', 'supply', 'installation'],
        'in_service': ['manufacturing', 'supply', 'installation', 'periodic']
    }

    status = track_item.get('status', 'in_stock')
    required = required_inspections.get(status, [])

    # Check for missing inspections
    inspection_types = [insp.get('inspection_type') for insp in inspections]
    for req_type in required:
        if req_type not in inspection_types:
            missing_inspections.append(req_type)
            exceptions.append(f'Missing {req_type} inspection')

    # Check for failed inspections
    failed_inspections = [
        insp for insp in inspections
        if insp.get('inspection_status') == 'failed'
    ]

    if failed_inspections:
        exceptions.append(f'{len(failed_inspections)} failed inspection(s)')

    # Check for overdue periodic inspections (if in service > 6 months)
    if status == 'in_service':
        installation_date = track_item.get('installation_date')
        if installation_date:
            if isinstance(installation_date, str):
                installation_date = datetime.fromisoformat(installation_date).date()

            months_in_service = (datetime.now().date() - installation_date).days / 30

            if months_in_service > 6:
                periodic_inspections = [
                    insp for insp in inspections
                    if insp.get('inspection_type') == 'periodic'
                ]

                if not periodic_inspections:
                    overdue_inspections.append('periodic')
                    exceptions.append('Periodic inspection overdue (>6 months in service)')
                else:
                    # Check last periodic inspection date
                    last_periodic = max(
                        periodic_inspections,
                        key=lambda x: x.get('inspection_date', '')
                    )
                    last_date = datetime.fromisoformat(last_periodic['inspection_date']).date()
                    days_since = (datetime.now().date() - last_date).days

                    if days_since > 180:  # 6 months
                        overdue_inspections.append('periodic')
                        exceptions.append(f'Periodic inspection overdue by {days_since - 180} days')

    compliance_score = 100
    if missing_inspections:
        compliance_score -= len(missing_inspections) * 20
    if failed_inspections:
        compliance_score -= len(failed_inspections) * 25
    if overdue_inspections:
        compliance_score -= len(overdue_inspections) * 15

    compliance_score = max(0, compliance_score)

    return {
        'compliance_score': compliance_score,
        'is_compliant': compliance_score >= 70,
        'missing_inspections': missing_inspections,
        'failed_inspections': len(failed_inspections),
        'overdue_inspections': overdue_inspections,
        'exceptions': exceptions,
        'alert_level': 'high' if compliance_score < 50 else 'medium' if compliance_score < 70 else 'low'
    }


def calculate_health_score(track_item, inspections) -> Dict[str, Any]:
    """Calculate overall health score for track item"""
    score = 100
    factors = []

    # Factor 1: Defect count
    defect_count = track_item.get('defect_count', 0)
    if defect_count > 0:
        defect_penalty = min(defect_count * 5, 30)
        score -= defect_penalty
        factors.append(f'{defect_count} defect(s) reported (-{defect_penalty})')

    # Factor 2: Replacement count
    replacement_count = track_item.get('replacement_count', 0)
    if replacement_count > 0:
        replacement_penalty = min(replacement_count * 10, 20)
        score -= replacement_penalty
        factors.append(f'{replacement_count} replacement(s) (-{replacement_penalty})')

    # Factor 3: Performance status
    performance_status = track_item.get('performance_status', 'good')
    performance_penalties = {
        'failed': 40,
        'poor': 30,
        'average': 15,
        'good': 0
    }
    penalty = performance_penalties.get(performance_status, 0)
    if penalty > 0:
        score -= penalty
        factors.append(f'Performance: {performance_status} (-{penalty})')

    # Factor 4: Failed inspections
    failed_inspections = [
        insp for insp in inspections
        if insp.get('inspection_status') == 'failed'
    ]
    if failed_inspections:
        inspection_penalty = len(failed_inspections) * 15
        score -= inspection_penalty
        factors.append(f'{len(failed_inspections)} failed inspection(s) (-{inspection_penalty})')

    # Factor 5: Age of item (older items get slight penalty)
    manufacture_date = track_item.get('manufacture_date')
    if manufacture_date:
        if isinstance(manufacture_date, str):
            manufacture_date = datetime.fromisoformat(manufacture_date).date()
        age_years = (datetime.now().date() - manufacture_date).days / 365
        if age_years > 3:
            age_penalty = min(int(age_years - 3) * 2, 10)
            score -= age_penalty
            factors.append(f'Age: {age_years:.1f} years (-{age_penalty})')

    score = max(0, min(100, score))

    return {
        'health_score': score,
        'health_grade': 'A' if score >= 90 else 'B' if score >= 75 else 'C' if score >= 60 else 'D' if score >= 40 else 'F',
        'factors': factors,
        'recommendation': get_health_recommendation(score)
    }


def get_health_recommendation(score: int) -> str:
    """Get recommendation based on health score"""
    if score >= 90:
        return 'Item in excellent condition. Continue regular monitoring.'
    elif score >= 75:
        return 'Item in good condition. Schedule routine inspection.'
    elif score >= 60:
        return 'Item showing signs of wear. Increase monitoring frequency.'
    elif score >= 40:
        return 'Item condition is concerning. Schedule detailed inspection immediately.'
    else:
        return 'Item in poor condition. Consider replacement. Immediate action required.'


def detect_exceptions(track_item, inspections, vendor_info=None) -> Dict[str, Any]:
    """
    Main AI exception detection function
    Identifies quality issues, warranty problems, and compliance violations
    """
    exceptions = []
    alerts = []
    recommendations = []

    # 1. Warranty Analysis
    warranty_status = calculate_warranty_status(track_item.get('warranty_expiry_date'))
    if warranty_status['alert_level'] in ['high', 'critical']:
        exceptions.append({
            'type': 'warranty',
            'severity': warranty_status['alert_level'],
            'message': warranty_status['message']
        })
        if warranty_status['status'] == 'expiring_soon':
            recommendations.append('Contact vendor for warranty renewal or replacement')
        elif warranty_status['status'] == 'expired':
            recommendations.append('Item operating without warranty coverage - assess risk')

    # 2. Inspection Compliance
    inspection_compliance = check_inspection_compliance(track_item, inspections)
    if not inspection_compliance['is_compliant']:
        for exc in inspection_compliance['exceptions']:
            exceptions.append({
                'type': 'inspection_compliance',
                'severity': inspection_compliance['alert_level'],
                'message': exc
            })

        if inspection_compliance['missing_inspections']:
            recommendations.append(
                f"Schedule missing inspections: {', '.join(inspection_compliance['missing_inspections'])}"
            )
        if inspection_compliance['overdue_inspections']:
            recommendations.append('Periodic inspection overdue - schedule immediately')

    # 3. Health Score Analysis
    health_analysis = calculate_health_score(track_item, inspections)
    if health_analysis['health_score'] < 60:
        exceptions.append({
            'type': 'health',
            'severity': 'high' if health_analysis['health_score'] < 40 else 'medium',
            'message': f"Low health score: {health_analysis['health_score']}/100"
        })
        recommendations.append(health_analysis['recommendation'])

    # 4. Performance Status Check
    if track_item.get('performance_status') in ['poor', 'failed']:
        exceptions.append({
            'type': 'performance',
            'severity': 'critical' if track_item.get('performance_status') == 'failed' else 'high',
            'message': f"Performance status: {track_item.get('performance_status')}"
        })
        recommendations.append('Immediate investigation required - item may need replacement')

    # 5. Vendor Performance (if vendor info provided)
    if vendor_info:
        if not vendor_info.get('is_approved'):
            exceptions.append({
                'type': 'vendor',
                'severity': 'medium',
                'message': 'Vendor not approved or certification pending'
            })

        vendor_rating = vendor_info.get('performance_rating', 0)
        if vendor_rating < 2.5:
            exceptions.append({
                'type': 'vendor',
                'severity': 'high',
                'message': f'Low vendor performance rating: {vendor_rating}/5.0'
            })
            recommendations.append('Consider alternative vendors for future procurement')

    # 6. Data Completeness Check
    critical_fields = ['manufacture_date', 'supply_date', 'warranty_expiry_date', 'vendor_id']
    missing_fields = [field for field in critical_fields if not track_item.get(field)]
    if missing_fields:
        exceptions.append({
            'type': 'data_quality',
            'severity': 'medium',
            'message': f"Missing critical data: {', '.join(missing_fields)}"
        })
        recommendations.append('Complete item documentation for better tracking')

    # Calculate overall risk score
    risk_score = calculate_risk_score(exceptions, health_analysis['health_score'])

    return {
        'risk_score': risk_score,
        'risk_level': get_risk_level(risk_score),
        'exceptions_count': len(exceptions),
        'exceptions': exceptions,
        'recommendations': recommendations,
        'warranty_status': warranty_status,
        'inspection_compliance': inspection_compliance,
        'health_analysis': health_analysis,
        'requires_action': risk_score >= 60 or health_analysis['health_score'] < 60
    }


def calculate_risk_score(exceptions: List[Dict], health_score: int) -> int:
    """Calculate overall risk score (0-100, higher is worse)"""
    severity_weights = {
        'critical': 30,
        'high': 20,
        'medium': 10,
        'low': 5
    }

    risk = 0
    for exc in exceptions:
        risk += severity_weights.get(exc.get('severity', 'low'), 5)

    # Factor in health score (inverse relationship)
    risk += (100 - health_score) * 0.3

    return min(100, int(risk))


def get_risk_level(risk_score: int) -> str:
    """Determine risk level from score"""
    if risk_score >= 75:
        return 'critical'
    elif risk_score >= 50:
        return 'high'
    elif risk_score >= 25:
        return 'medium'
    else:
        return 'low'


def generate_ai_report(track_item, inspections, vendor_info=None) -> Dict[str, Any]:
    """
    Generate comprehensive AI-powered report for a track item
    This is what gets displayed when QR code is scanned
    """
    analysis = detect_exceptions(track_item, inspections, vendor_info)

    # Generate summary
    item_type_names = {
        'elastic_rail_clip': 'Elastic Rail Clip',
        'rail_pad': 'Rail Pad',
        'liner': 'Liner',
        'sleeper': 'Sleeper'
    }

    item_type = track_item.get('item_type', 'unknown')
    summary = f"{item_type_names.get(item_type, item_type)} - Lot {track_item.get('lot_number', 'N/A')}"

    if analysis['risk_level'] == 'critical':
        status_message = '🚨 CRITICAL: Immediate action required'
    elif analysis['risk_level'] == 'high':
        status_message = '⚠️ HIGH RISK: Urgent attention needed'
    elif analysis['risk_level'] == 'medium':
        status_message = '⚡ MEDIUM RISK: Schedule inspection soon'
    else:
        status_message = '✅ LOW RISK: Item in good condition'

    return {
        'summary': summary,
        'status_message': status_message,
        'item_details': {
            'lot_number': track_item.get('lot_number'),
            'item_type': item_type_names.get(item_type, item_type),
            'quantity': track_item.get('quantity'),
            'vendor_name': vendor_info.get('vendor_name') if vendor_info else track_item.get('vendor_id'),
            'manufacture_date': track_item.get('manufacture_date'),
            'supply_date': track_item.get('supply_date'),
            'status': track_item.get('status'),
            'location': track_item.get('installation_location')
        },
        'analysis': analysis,
        'inspection_summary': {
            'total_inspections': len(inspections),
            'passed': len([i for i in inspections if i.get('inspection_status') == 'passed']),
            'failed': len([i for i in inspections if i.get('inspection_status') == 'failed']),
            'pending': len([i for i in inspections if i.get('inspection_status') == 'pending'])
        },
        'quick_actions': get_quick_actions(analysis, track_item)
    }


def get_quick_actions(analysis: Dict, track_item: Dict) -> List[str]:
    """Generate quick action items based on analysis"""
    actions = []

    if analysis['requires_action']:
        actions.append('Schedule inspection')

    if analysis['warranty_status']['alert_level'] in ['high', 'critical']:
        actions.append('Check warranty status')

    if not analysis['inspection_compliance']['is_compliant']:
        actions.append('Update inspections')

    if analysis['health_analysis']['health_score'] < 60:
        actions.append('Assess for replacement')

    if track_item.get('performance_status') in ['poor', 'failed']:
        actions.append('Report defect')

    if not actions:
        actions.append('Continue monitoring')

    return actions
