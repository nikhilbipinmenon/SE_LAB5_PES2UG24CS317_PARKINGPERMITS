"""Campus Parking Permit Manager module.

Provides functionalities to register permits, check permit expiration,
scan designated parking zones, and persist permit data.
"""

import json
import secrets
from datetime import datetime, timedelta

# Global state
permits = {}
ZONES = ["A", "B", "C"]


def register_permit(vehicle_plate, zone_id, zone_records=None):
    """Register a new permit for a vehicle in a specific zone."""
    if not vehicle_plate or not isinstance(vehicle_plate, str):
        return None
    vehicle_plate = vehicle_plate.strip().upper()
    if not vehicle_plate or zone_id not in ZONES:
        return None

    if zone_records is None:
        zone_records = []

    try:
        random_num = secrets.randbelow(90000) + 10000
        permit_no = f"P{random_num}"
        expiry = datetime.now() + timedelta(days=180)
        permits[vehicle_plate] = {
            "zone": zone_id,
            "permit": permit_no,
            "expiry": expiry.strftime("%Y-%m-%d"),
        }
        zone_records.append((vehicle_plate, zone_id))
        return permit_no
    except (TypeError, ValueError):
        return None


def revoke_permit(vehicle_plate):
    """Revoke an existing permit for a given vehicle plate."""
    if not vehicle_plate or not isinstance(vehicle_plate, str):
        return False
    vehicle_plate = vehicle_plate.strip().upper()
    return permits.pop(vehicle_plate, None) is not None


def is_expired(vehicle_plate):
    """Check if the permit for a given vehicle plate is expired."""
    if vehicle_plate not in permits:
        return False
    date_str = permits[vehicle_plate].get("expiry", "")
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            expiry = datetime.strptime(date_str, fmt)
            return expiry < datetime.now()
        except ValueError:
            continue
    return False


def scan_zone(zone_id, plates_seen):
    """Scan and flag unauthorized or expired vehicles in a given zone."""
    flagged = []
    for plate in plates_seen:
        if (
            plate not in permits
            or permits[plate]["zone"] != zone_id
            or is_expired(plate)
        ):
            flagged.append(plate)
    return flagged


def load_permit_database(file="permits.json"):
    """Load permit records from a JSON file into memory."""
    try:
        with open(file, "r", encoding="utf-8") as f_in:
            data = json.load(f_in)
            if isinstance(data, dict):
                permits.clear()
                permits.update(data)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        permits.clear()


def save_permit_database(file="permits.json"):
    """Save current permit records to a JSON file."""
    try:
        with open(file, "w", encoding="utf-8") as f_out:
            json.dump(permits, f_out, indent=2)
    except OSError as err:
        print(f"Error saving permit database: {err}")


def set_expiry(vehicle_plate, date_text):
    """Update the expiry date for a registered vehicle plate."""
    if vehicle_plate in permits:
        permits[vehicle_plate]["expiry"] = date_text


setExpiry = set_expiry


def main():
    """Main demonstration entry point for the parking permit manager."""
    load_permit_database()
    register_permit("KA01AB1234", "A")
    register_permit("KA05XY9999", "Z")
    register_permit("", "B")
    register_permit(None, "C")
    set_expiry("KA01AB1234", "01/01/2020")
    revoke_permit("MH12ZZ0000")
    flagged = scan_zone("A", ["KA01AB1234", "KA05XY9999", "TN09QQ1111"])
    print("Flagged in zone A:", flagged)
    plate = input("Plate to revoke (Enter to skip): ").strip()
    if plate:
        revoke_permit(plate)
    save_permit_database()
    print("Permits on file:", len(permits))


if __name__ == "__main__":
    main()
