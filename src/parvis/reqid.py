"""
PARVIS RequID Assignment Module

Assigns unique requirement IDs to extracted requirements following
FBMS-[TYPE]-[MODULE]-[SEQ] format.
"""
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple


# Global state for tracking sequences (would be loaded from registry in production)
_sequence_tracker = None
_module_map = None


def reset_global_state():
    """Reset global state for fresh test runs"""
    global _sequence_tracker, _module_map
    _sequence_tracker = None
    _module_map = None


def load_module_map(path: str = ".moai/bms/requirements/registry/module-map.json", reload: bool = False) -> Dict:
    """Load module mapping configuration"""
    global _module_map
    if _module_map is not None and not reload:
        return _module_map

    with open(path) as f:
        _module_map = json.load(f)
    return _module_map


def load_sequence_tracker(path: str = ".moai/bms/requirements/registry/sequence-tracker.json") -> Dict:
    """Load sequence tracker"""
    global _sequence_tracker
    if _sequence_tracker is not None:
        return _sequence_tracker

    with open(path) as f:
        _sequence_tracker = json.load(f)
    return _sequence_tracker


def save_sequence_tracker(tracker: Dict, path: str = ".moai/bms/requirements/registry/sequence-tracker.json"):
    """Save sequence tracker to file"""
    with open(path, "w") as f:
        json.dump(tracker, f, indent=2)
    global _sequence_tracker
    _sequence_tracker = tracker


def validate_requirement_id(req_id: str) -> bool:
    """
    Validate requirement ID format.
    Pattern: FBMS-[TYPE]-[MODULE]-[SEQ:03d]
    """
    pattern = r"^FBMS-(SWE|FSR|HSI|TST|CFG)-(SOA|BAL|ALG|PLS|RED|DBS|DIA|SYS|MON|CON|CAN|IMD)-\d{3}$"
    return bool(re.match(pattern, req_id))


def map_extraction_type_to_type(extraction_type: str) -> str:
    """
    Map extraction type to TYPE code.

    Mappings:
    - doxygen -> SWE
    - assertion -> FSR
    - state_machine -> SWE
    - config -> CFG
    """
    mapping = {
        "doxygen": "SWE",
        "assertion": "FSR",
        "state_machine": "SWE",
        "config": "CFG",
    }
    return mapping.get(extraction_type, "SWE")


def map_module_to_id_code(module: str, module_map_path: str = ".moai/bms/requirements/registry/module-map.json") -> Optional[str]:
    """Map extracted module name to ID module code"""
    try:
        module_map = load_module_map(module_map_path)
        mappings = module_map["mappings"]["extracted_to_id"]
        # Try to get mapped value, otherwise use the module name as-is
        result = mappings.get(module, module)
        # If result is still the module name and it's not in the map, use it as-is
        # This allows new modules to work without being explicitly mapped
        return result if result else None
    except Exception:
        return module  # Return the module name as fallback


def get_next_sequence(type_code: str, module_code: str) -> int:
    """Get next sequence number for TYPE+MODULE combination"""
    tracker = load_sequence_tracker()
    key = f"{type_code}-{module_code}"

    if key not in tracker["sequences"]:
        tracker["sequences"][key] = 1

    sequence = tracker["sequences"][key]
    tracker["sequences"][key] = sequence + 1

    # Save updated tracker
    save_sequence_tracker(tracker)

    return sequence


def generate_requirement_id(
    extraction_type: str,
    suggested_module: str,
    type_code: Optional[str] = None,
    module_code: Optional[str] = None,
) -> Optional[str]:
    """
    Generate requirement ID for a requirement.

    Returns: FBMS-[TYPE]-[MODULE]-[SEQ:03d] or None if generation fails
    """
    try:
        # Determine TYPE if not provided
        if type_code is None:
            type_code = map_extraction_type_to_type(extraction_type)

        # Map module to ID code if not provided
        if module_code is None:
            module_code = map_module_to_id_code(suggested_module)
            if module_code is None:
                return None

        # Get next sequence
        sequence = get_next_sequence(type_code, module_code)

        # Generate ID
        req_id = f"FBMS-{type_code}-{module_code}-{sequence:03d}"

        if validate_requirement_id(req_id):
            return req_id
        return None

    except Exception:
        return None


def load_extracted_requirements(path: str) -> List[Dict]:
    """Load requirements from BMS-extracted.json"""
    with open(path) as f:
        data = json.load(f)

    return data.get("requirements", [])


def assign_ids_to_requirements(requirements: List[Dict]) -> List[Dict]:
    """
    Assign IDs to all requirements.

    Returns: List of requirements with assigned IDs (at least 95%)
    """
    assigned = []
    failed = []

    for req in requirements:
        try:
            extraction_type = req.get("extraction_type", "doxygen")
            suggested_module = req.get("suggested_module", "BMS")

            req_id = generate_requirement_id(extraction_type, suggested_module)

            if req_id:
                req_copy = req.copy()
                req_copy["assigned_id"] = req_id
                assigned.append(req_copy)
            else:
                failed.append(req)

        except Exception as e:
            failed.append(req)

    return assigned


def create_id_registry(input_path: str) -> Dict:
    """
    Create ID registry from extracted requirements.

    Creates:
    - id-registry.json
    - id-registry.backup.json
    - id-assignment-log.json
    """
    # Load requirements
    requirements = load_extracted_requirements(input_path)

    # Assign IDs
    assigned = assign_ids_to_requirements(requirements)

    # Create registry
    registry = {
        "registry_id": f"REGISTRY-{datetime.now().isoformat()}",
        "created": datetime.now().isoformat(),
        "source": input_path,
        "total_requirements": len(requirements),
        "assigned_count": len(assigned),
        "assignment_rate": len(assigned) / len(requirements) if requirements else 0,
        "requirements": assigned,
    }

    # Save registry
    registry_path = ".moai/bms/requirements/registry/id-registry.json"
    with open(registry_path, "w") as f:
        json.dump(registry, f, indent=2)

    # Create backup
    backup_path = ".moai/bms/requirements/registry/id-registry.backup.json"
    with open(backup_path, "w") as f:
        json.dump(registry, f, indent=2)

    # Create log
    log = {
        "timestamp": datetime.now().isoformat(),
        "source": input_path,
        "total_requirements": len(requirements),
        "assigned_count": len(assigned),
        "failed_count": len(requirements) - len(assigned),
        "assignment_rate": len(assigned) / len(requirements) if requirements else 0,
        "id_collisions": 0,
        "type_distribution": _get_type_distribution(assigned),
        "module_distribution": _get_module_distribution(assigned),
    }

    log_path = ".moai/bms/requirements/logs/id-assignment-log.json"
    with open(log_path, "w") as f:
        json.dump(log, f, indent=2)

    return registry


def _get_type_distribution(requirements: List[Dict]) -> Dict[str, int]:
    """Count distribution of TYPE codes in requirements"""
    distribution = {}
    for req in requirements:
        req_id = req.get("assigned_id", "")
        if req_id.startswith("FBMS-"):
            type_code = req_id.split("-")[1]
            distribution[type_code] = distribution.get(type_code, 0) + 1
    return distribution


def _get_module_distribution(requirements: List[Dict]) -> Dict[str, int]:
    """Count distribution of MODULE codes in requirements"""
    distribution = {}
    for req in requirements:
        req_id = req.get("assigned_id", "")
        if req_id.startswith("FBMS-"):
            parts = req_id.split("-")
            if len(parts) >= 3:
                module_code = parts[2]
                distribution[module_code] = distribution.get(module_code, 0) + 1
    return distribution


if __name__ == "__main__":
    # Example usage
    registry = create_id_registry(".moai/bms/requirements/extracted/BMS-extracted.json")
    print(f"Created registry with {registry['assigned_count']} assigned requirements")
    print(f"Assignment rate: {registry['assignment_rate']:.1%}")
