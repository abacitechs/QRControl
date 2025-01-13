from flask import Blueprint, jsonify, request, abort
from flask_login import login_required
from ..models import SystemDetails

system_bp = Blueprint('system', __name__)

@system_bp.route('/system_details', methods=['GET'])
@login_required
def get_system_details():
    details = SystemDetails.get_or_create()
    results = {
        "server_url": details.server_url,
        "device_id": details.device_id,
        "device_name": details.device_name,
        "device_secret": details.device_secret,
        "device_activated": details.device_activated,
        "device_online_status": details.device_online_status,
    }
    return jsonify(results)

