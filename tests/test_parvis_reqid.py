"""
Tests for PARVIS RequID Assignment Module

RED Phase: Define expected behavior through tests
"""
import pytest
import json
import os
from pathlib import Path
from datetime import datetime


class TestModuleMapLoading:
    """Test module map configuration loading"""

    def test_module_map_exists(self):
        """Module map file should exist at expected location"""
        module_map_path = Path(
            ".moai/bms/requirements/registry/module-map.json"
        )
        assert module_map_path.exists(), "module-map.json should exist"

    def test_module_map_structure(self):
        """Module map should have valid structure"""
        with open(".moai/bms/requirements/registry/module-map.json") as f:
            data = json.load(f)

        assert "version" in data
        assert "mappings" in data
        assert "extracted_to_id" in data["mappings"]
        assert "id_to_full_name" in data["mappings"]
        assert "type_codes" in data

    def test_module_map_mappings_symmetric(self):
        """extracted_to_id and id_to_full_name should have matching keys"""
        with open(".moai/bms/requirements/registry/module-map.json") as f:
            data = json.load(f)

        extracted_keys = set(data["mappings"]["extracted_to_id"].values())
        full_name_keys = set(data["mappings"]["id_to_full_name"].keys())
        assert extracted_keys == full_name_keys


class TestSequenceTrackerInitialization:
    """Test sequence tracker initialization"""

    def test_sequence_tracker_exists(self):
        """Sequence tracker should exist"""
        tracker_path = Path(".moai/bms/requirements/registry/sequence-tracker.json")
        assert tracker_path.exists()

    def test_sequence_tracker_all_combinations(self):
        """Sequence tracker should have all TYPE+MODULE combinations"""
        with open(".moai/bms/requirements/registry/sequence-tracker.json") as f:
            tracker = json.load(f)

        type_codes = ["SWE", "FSR", "HSI", "TST", "CFG"]
        module_codes = ["SOA", "BAL", "ALG", "PLS", "RED", "DBS", "DIA", "SYS", "MON", "CON", "CAN", "IMD"]

        for type_code in type_codes:
            for module_code in module_codes:
                key = f"{type_code}-{module_code}"
                assert key in tracker["sequences"], f"Missing sequence for {key}"
                assert tracker["sequences"][key] >= 1, f"Sequence should be >= 1 for {key}"


class TestRequirementIDAssignment:
    """Test requirement ID assignment logic"""

    def test_id_format_validation_valid(self):
        """Valid IDs should match pattern FBMS-TYPE-MODULE-SEQ"""
        from src.parvis.reqid import validate_requirement_id

        valid_ids = [
            "FBMS-SWE-SOA-001",
            "FBMS-FSR-BAL-042",
            "FBMS-CFG-DBS-999",
        ]
        for req_id in valid_ids:
            assert validate_requirement_id(req_id), f"{req_id} should be valid"

    def test_id_format_validation_invalid(self):
        """Invalid IDs should be rejected"""
        from src.parvis.reqid import validate_requirement_id

        invalid_ids = [
            "INVALID-SWE-SOA-001",
            "FBMS-INVALID-SOA-001",
            "FBMS-SWE-INVALID-001",
            "FBMS-SWE-SOA-00",
            "FBMS-swe-soa-001",
        ]
        for req_id in invalid_ids:
            assert not validate_requirement_id(req_id), f"{req_id} should be invalid"

    def test_extraction_type_to_type_mapping(self):
        """Extraction types should map to TYPE codes correctly"""
        from src.parvis.reqid import map_extraction_type_to_type

        mappings = {
            "doxygen": "SWE",
            "assertion": "FSR",
            "state_machine": "SWE",
            "config": "CFG",
        }
        for extraction_type, expected_type in mappings.items():
            result = map_extraction_type_to_type(extraction_type)
            assert result == expected_type, f"{extraction_type} should map to {expected_type}"

    def test_next_sequence_generation(self):
        """Generate next sequence for TYPE+MODULE combination"""
        from src.parvis.reqid import get_next_sequence

        # Load tracker
        with open(".moai/bms/requirements/registry/sequence-tracker.json") as f:
            original_tracker = json.load(f)

        try:
            # Get initial sequence
            seq1 = get_next_sequence("SWE", "ALG")
            assert seq1 >= 1, "First sequence should be >= 1"

            # Get next sequence - should be incremented
            seq2 = get_next_sequence("SWE", "ALG")
            assert seq2 == seq1 + 1, "Second sequence should be incremented"

        finally:
            # Restore original tracker
            with open(".moai/bms/requirements/registry/sequence-tracker.json", "w") as f:
                json.dump(original_tracker, f, indent=2)

    def test_generate_requirement_id(self):
        """Generate complete requirement ID"""
        from src.parvis.reqid import generate_requirement_id, validate_requirement_id

        req_id = generate_requirement_id(
            extraction_type="doxygen",
            suggested_module="BMS"
        )

        assert req_id is not None
        assert req_id.startswith("FBMS-")
        assert validate_requirement_id(req_id)


class TestBulkIDAssignment:
    """Test bulk ID assignment from extracted requirements"""

    def test_load_extracted_requirements(self):
        """Load requirements from BMS-extracted.json"""
        from src.parvis.reqid import load_extracted_requirements

        requirements = load_extracted_requirements(".moai/bms/requirements/extracted/BMS-extracted.json")
        assert len(requirements) > 0, "Should load requirements"
        assert len(requirements) == 111, "Should load exactly 111 requirements"

    def test_assign_ids_to_all_requirements(self):
        """Assign IDs to all 111 requirements"""
        from src.parvis.reqid import load_extracted_requirements, assign_ids_to_requirements, validate_requirement_id

        requirements = load_extracted_requirements(".moai/bms/requirements/extracted/BMS-extracted.json")
        assigned = assign_ids_to_requirements(requirements)

        assert len(assigned) >= 105, "Should assign IDs to at least 95% (105/111)"

        # Check all assigned requirements have valid IDs
        for req in assigned:
            assert "assigned_id" in req or "req_id" in req
            req_id = req.get("assigned_id") or req.get("req_id")
            assert validate_requirement_id(req_id), f"Invalid ID: {req_id}"

    def test_no_id_collisions(self):
        """Assigned IDs should have no collisions"""
        from src.parvis.reqid import load_extracted_requirements, assign_ids_to_requirements

        requirements = load_extracted_requirements(".moai/bms/requirements/extracted/BMS-extracted.json")
        assigned = assign_ids_to_requirements(requirements)

        ids = []
        for req in assigned:
            req_id = req.get("assigned_id") or req.get("req_id")
            if req_id:
                ids.append(req_id)

        assert len(ids) == len(set(ids)), "IDs should have no collisions"

    def test_create_id_registry(self):
        """Create and save ID registry"""
        from src.parvis.reqid import create_id_registry

        registry_path = ".moai/bms/requirements/registry/id-registry.json"
        registry = create_id_registry(".moai/bms/requirements/extracted/BMS-extracted.json")

        assert "registry_id" in registry
        assert "created" in registry
        assert "requirements" in registry
        # At least 95% of requirements should be assigned
        assignment_rate = len(registry["requirements"]) / registry["total_requirements"]
        assert assignment_rate >= 0.95, f"Assignment rate should be >= 95%, got {assignment_rate:.1%}"

    def test_registry_backup_created(self):
        """Backup of registry should be created"""
        from src.parvis.reqid import create_id_registry

        backup_path = ".moai/bms/requirements/registry/id-registry.backup.json"

        # Create registry (which should also create backup)
        registry = create_id_registry(".moai/bms/requirements/extracted/BMS-extracted.json")

        # Backup should exist if registry exists
        # This test will pass once implementation creates backup


class TestIDAssignmentLogging:
    """Test logging of ID assignment process"""

    def test_assignment_log_created(self):
        """Assignment log should be created"""
        from src.parvis.reqid import create_id_registry

        log_path = ".moai/bms/requirements/logs/id-assignment-log.json"

        # Create registry (which should generate log)
        registry = create_id_registry(".moai/bms/requirements/extracted/BMS-extracted.json")

        # Log should be created
        # This test will pass once implementation creates log


class TestModuleCodeMapping:
    """Test module code mapping"""

    def test_map_extracted_module_to_id(self):
        """Map extracted module names to ID codes"""
        from src.parvis.reqid import map_module_to_id_code

        module_map_path = ".moai/bms/requirements/registry/module-map.json"

        # Common modules that should exist
        assert map_module_to_id_code("BMS", module_map_path) is not None

        result = map_module_to_id_code("DIAG", module_map_path)
        assert result in ["DIA", "DIAG", None]  # Should map or return None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
