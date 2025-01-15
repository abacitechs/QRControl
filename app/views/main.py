from flask import Blueprint, render_template, request, jsonify, abort, flash, redirect, url_for
from flask_login import login_required, current_user
from ..models import SystemDetails
from .. import db
import re
import requests
import secrets
from ..gpio_actions import toggle_gpio
from ..redis_actions import sync_to_redis,get_from_redis
import json

main_bp = Blueprint('main', __name__)

def update_systeminfo_in_redis():
    details = SystemDetails.get_or_create()
    sync_to_redis("system_info",json.dumps(details.to_dict())) 



@main_bp.route('/')
@login_required
def home():
    socket_token = {"socket_token" : secrets.token_hex(32)}
    sync_to_redis("socket_token",socket_token["socket_token"])
    # Fetch system details
    details = SystemDetails.get_or_create()
    if details.server_url == "":
        results = {
        "server_url": details.server_url
        }
        return render_template('home.html', user=current_user, details=results)
    elif details.device_name == "":
        results = {
        "server_url": details.server_url,
        "device_name": details.device_name
        }
        return render_template('home.html', user=current_user, details=results)
    elif details.device_id == "":
        results = {
        "server_url": details.server_url,
        "device_name": details.device_name,
        "device_id": details.device_id
        }
        return render_template('home.html', user=current_user, details=results)
    elif details.tenant == "":
        url = details.server_url + '/public_api/qrcontroller_client_fetch'
        data = {
                    "device_id": details.device_id,
                    "device_secret": details.device_secret
                }
        try:
            # Make the POST request
            response = requests.post(url, json=data)
            tenant = response.json().get('tenant', None)
            if tenant is not None:
                details.tenant = tenant
                db.session.commit()
                update_systeminfo_in_redis()
            results = {
                "server_url": details.server_url,
                "device_name": details.device_name,
                "device_id": details.device_id,
                "tenant": response.json().get('tenant', None),
                "server_availability": True,
            }
            return render_template('home.html', user=current_user, details=results)
        except:
            results = {
                "server_url": details.server_url,
                "device_name": details.device_name,
                "device_id": details.device_id,
                "server_availability": False,
            }
            return render_template('home.html', user=current_user, details=results)
    else:
        server_connectivity = get_from_redis("server_connectivity")
        server_availability = "False" if server_connectivity is None else server_connectivity
        results = {
                "server_url": details.server_url,
                "device_name": details.device_name,
                "device_id": details.device_id,
                "tenant": details.tenant,
                "server_availability": server_availability,
            }
        return render_template('home.html', user=current_user, details=results, socket_token = socket_token)
        

@main_bp.route('/system_details_update', methods=['POST'])
@login_required
def system_details_update():
    # Fetch the existing system details
    details = SystemDetails.get_or_create()

    # Determine the action
    action = request.form.get('action')

    if action == 'update_server_url':
        server_url = request.form.get('server_url')
        # Validate the URL format
        if server_url and not is_valid_url(server_url):
            flash('Invalid URL format. Please enter a valid URL.', 'danger')
            return redirect(url_for('main.home'))

        # If valid, update the database
        if server_url:
            details.server_url = server_url

            # Commit the updates to the database
            db.session.commit()
            update_systeminfo_in_redis()


            flash('Server URL updated successfully.', 'success')
            return redirect(url_for('main.home'))
    elif action == 'reset_server_url':
        details.server_url = ""
        # Commit the updates to the database
        db.session.commit()
        update_systeminfo_in_redis()
        flash('Server URL reset successfully.', 'success')
        return redirect(url_for('main.home'))
    elif action == 'set_device_name':
        device_name = request.form.get('device_name')
        # Validate the URL format
        if not device_name:
            flash('Please enter a valid Device Name', 'danger')
            return redirect(url_for('main.home'))

        else:
            details.device_name = device_name
            # Commit the updates to the database
            db.session.commit()
            update_systeminfo_in_redis()
            flash('Device Name updated successfully.', 'success')
            return redirect(url_for('main.home'))
    elif action == 'reset_device_name':
        details.device_name = ""
        # Commit the updates to the database
        db.session.commit()
        update_systeminfo_in_redis()

        flash('Device name reset successfully.', 'success')
        return redirect(url_for('main.home'))
    elif action == 'get_device_id':
        url = details.server_url + '/public_api/qrcontroller_id_fetch'

        data = {
            "device_name": details.device_name,
            "secret": details.device_secret,
            "gpio_pins":[4,5,6,12,13,16,17,18,19,20,21,22,23,24,25,26,27]
            }
        
        try:
            # Make the POST request
            response = requests.post(url, json=data)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the response and update the device_id
                device_id = response.json().get('device_id', None)
                if device_id is not None:
                    details.device_id = device_id
                    db.session.commit()
                    update_systeminfo_in_redis()
                    flash('Device ID fetched successfully.', 'success')
                    return redirect(url_for('main.home'))
                else:
                    flash('Failed to fetch Device ID. Please try again.', 'danger')
                    return redirect(url_for('main.home'))
            else:
                # Handle failed response
                flash('Failed to fetch Device ID. Please try again.', 'danger')
                return redirect(url_for('main.home'))
        except requests.exceptions.RequestException as e:
            # Handle exceptions during the request
            flash(f'An error occurred: {str(e)}', 'danger')
    elif action == 'reset_device':
        details.server_url = ""
        details.device_name = ""
        details.device_id = ""
        details.tenant = ""
        details.device_secret = secrets.token_hex(32)
        # Commit the updates to the database
        db.session.commit()
        update_systeminfo_in_redis()
        flash('Device ID reset successfully.', 'success')
        return redirect(url_for('main.home'))
    else:
        return redirect(url_for('main.home'))

def is_valid_url(url):
    """
    Validate a URL using regex.
    """
    url_regex = re.compile(
        r'^(https?|ftp)://'  # http:// or https:// or ftp://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or IPv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or IPv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )
    return re.match(url_regex, url) is not None

@main_bp.route('/gpio_table')
@login_required
def gpio_table():
    return render_template('gpio_table.html')


@main_bp.route('/gpio_action', methods=['POST'])
@login_required
def gpio_action():
    pin_number = request.form.get('pin_number')
    if pin_number:
        # Perform GPIO activation or any related action here
        toggle_gpio(int(pin_number))
        flash(f'GPIO {pin_number} activated successfully.', 'success')
    else:
        flash('Failed to activate GPIO. Pin number is missing.', 'danger')
    return redirect(url_for('main.gpio_table'))