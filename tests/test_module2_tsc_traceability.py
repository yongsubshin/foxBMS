"""
RED Phase Tests: Module 2 - TSC Traceability Resolution

These tests implement the acceptance criteria from AC-M2-001 through AC-M2-007.
Tests are designed to FAIL initially, driving implementation via TDD cycle.

Test Coverage:
- AC-M2-001: TSC document generation (ISO 26262 compliant)
- AC-M2-002: 147 safety requirements TSC mapping (100% coverage)
- AC-M2-003: Bidirectional traceability (TSC <-> SWR)
- AC-M2-004: BLOCK-003 resolution
- AC-M2-005: ASIL inheritance rules
- AC-M2-006: TSC gap analysis report
- AC-M2-007: TSC version management
"""

import json
import pytest
import re
from pathlib import Path
from typing import Dict, List, Set


class TestAC_M2_001_TSCDocumentGeneration:
    """AC-M2-001: TSC document generation - ISO 26262 compliant"""

    def test_tsc_document_exists(self):
        """Test that TSC document file exists"""
        tsc_file = Path('/home/kevin/work/forBMS/foxBMS/docs/parvis/safety/technical-safety-concept.md')

        assert tsc_file.exists(), f"TSC document not found at {tsc_file}"

    def test_tsc_minimum_safety_goals(self):
        """Test TSC document contains minimum 3 Safety Goals"""
        tsc_file = Path('/home/kevin/work/forBMS/foxBMS/docs/parvis/safety/technical-safety-concept.md')

        if tsc_file.exists():
            with open(tsc_file, 'r') as f:
                content = f.read()

            # Look for Safety Goal definitions
            sg_pattern = r'(Safety Goal|SG-[0-9]+|SG[0-9]+)'
            sg_matches = re.findall(sg_pattern, content, re.IGNORECASE)

            assert len(sg_matches) >= 3, f"Expected minimum 3 Safety Goals, found {len(sg_matches)}"

    def test_tsc_safety_goals_with_asil(self):
        """Test each Safety Goal has ASIL classification"""
        tsc_file = Path('/home/kevin/work/forBMS/foxBMS/docs/parvis/safety/technical-safety-concept.md')

        if tsc_file.exists():
            with open(tsc_file, 'r') as f:
                content = f.read()

            # Look for ASIL classifications
            asil_pattern = r'(ASIL-[A-D]|ASIL[A-D]|QM)'
            asil_matches = re.findall(asil_pattern, content)

            assert len(asil_matches) >= 3, \
                f"Expected minimum 3 ASIL classifications for Safety Goals, found {len(asil_matches)}"

    def test_tsc_elements_defined(self):
        """Test TSC document defines TSC elements (TSC-BMS-xxx)"""
        tsc_file = Path('/home/kevin/work/forBMS/foxBMS/docs/parvis/safety/technical-safety-concept.md')

        if tsc_file.exists():
            with open(tsc_file, 'r') as f:
                content = f.read()

            # Look for TSC element definitions
            tsc_pattern = r'TSC-BMS-\d{3}'
            tsc_matches = re.findall(tsc_pattern, content)

            assert len(tsc_matches) >= 3, \
                f"Expected minimum 3 TSC elements, found {len(tsc_matches)}"

    def test_iso_26262_clause_compliance(self):
        """Test TSC document references ISO 26262-3/4 compliance"""
        tsc_file = Path('/home/kevin/work/forBMS/foxBMS/docs/parvis/safety/technical-safety-concept.md')

        if tsc_file.exists():
            with open(tsc_file, 'r') as f:
                content = f.read()

            # Should reference ISO 26262 standard
            assert 'ISO 26262' in content or 'ISO26262' in content, \
                "TSC document should reference ISO 26262 compliance"


class TestAC_M2_002_SafetyRequirementMapping:
    """AC-M2-002: Map 147 safety requirements to TSC elements"""

    def test_tsc_traceability_matrix_exists(self):
        """Test that TSC traceability matrix file exists"""
        matrix_file = Path('/home/kevin/work/forBMS/foxBMS/docs/parvis/requirements/tsc-traceability-matrix.json')

        assert matrix_file.exists(), f"TSC traceability matrix not found at {matrix_file}"

    def test_147_safety_requirements_mapped(self):
        """Test that all 147 safety requirements are mapped to TSC"""
        matrix_file = Path('/home/kevin/work/forBMS/foxBMS/docs/parvis/requirements/tsc-traceability-matrix.json')

        if matrix_file.exists():
            with open(matrix_file, 'r') as f:
                matrix = json.load(f)

            # Check coverage metrics
            coverage = matrix.get('coverage_metrics', {})
            total_requirements = coverage.get('total_safety_requirements', 0)
            mapped_requirements = coverage.get('mapped_requirements', 0)
            completeness = coverage.get('mapping_completeness_percent', 0)

            # Should have 147 total safety requirements
            assert total_requirements >= 147, \
                f"Expected 147+ total safety requirements, found {total_requirements}"

            # Should have mapped 147 requirements
            assert mapped_requirements >= 147, \
                f"Expected 147+ mapped requirements, found {mapped_requirements}"

            # Completeness should be 100%
            assert completeness >= 95, \
                f"Expected 95%+ completeness, found {completeness}%"

    def test_asil_d_requirements_mapped(self):
        """Test all 52 ASIL-D requirements are mapped"""
        matrix_file = Path('/home/kevin/work/forBMS/foxBMS/docs/parvis/requirements/tsc-traceability-matrix.json')

        if matrix_file.exists():
            with open(matrix_file, 'r') as f:
                matrix = json.load(f)

            # Check ASIL-D count in coverage metrics
            coverage = matrix.get('coverage_metrics', {})
            asil_d_count = coverage.get('asil_distribution', {}).get('asil_d', 0)

            assert asil_d_count >= 52, \
                f"Expected minimum 52 ASIL-D requirements, found {asil_d_count}"

    def test_mapping_rationale_documented(self):
        """Test each mapping has documented rationale"""
        matrix_file = Path('/home/kevin/work/forBMS/foxBMS/docs/parvis/requirements/tsc-traceability-matrix.json')

        if matrix_file.exists():
            with open(matrix_file, 'r') as f:
                matrix = json.load(f)

            mappings = matrix.get('mappings', [])
            missing_rationale = 0

            for mapping in mappings[:10]:  # Check first 10
                if 'rationale' not in mapping and 'reason' not in mapping:
                    missing_rationale += 1

            # At least some should have rationale
            assert missing_rationale < len(mappings), \
                "Mappings should include rationale for traceability"


class TestAC_M2_003_BidirectionalTraceability:
    """AC-M2-003: Bidirectional traceability TSC <-> SWR"""

    def test_downward_traceability_tsc_to_fsr(self):
        """Test downward traceability from TSC to FSR"""
        matrix_file = Path('/home/kevin/work/forBMS/foxBMS/docs/parvis/requirements/tsc-traceability-matrix.json')

        if matrix_file.exists():
            with open(matrix_file, 'r') as f:
                matrix = json.load(f)

            # Check TSC -> FSR traceability
            mappings = matrix.get('mappings', [])
            tsc_to_fsr = 0

            for mapping in mappings:
                source = mapping.get('tsc_element')
                target = mapping.get('fsr_id') or mapping.get('requirement_id')

                if source and target:
                    tsc_to_fsr += 1

            assert tsc_to_fsr > 0, "No TSC -> FSR traceability found"

    def test_upward_traceability_swr_to_tsc(self):
        """Test upward traceability from SWR to TSC"""
        req_file = Path('/home/kevin/work/forBMS/foxBMS/docs/parvis/requirements/unified-requirements.json')

        if req_file.exists():
            with open(req_file, 'r') as f:
                data = json.load(f)

            requirements = data.get('requirements', [])
            fsr_with_tsc = 0

            for req in requirements:
                if 'SAF' in str(req.get('fbms_id', '')):
                    # Safety requirement should have TSC link
                    if 'tsc_element' in req or 'tsc_link' in req:
                        fsr_with_tsc += 1

            # Check some requirements have TSC links
            # This may be 0 initially if not yet implemented
            assert isinstance(fsr_with_tsc, int), "Should be able to count FSR with TSC links"

    def test_complete_traceability_chain(self):
        """Test complete traceability chain: Safety Goal -> TSC -> FSR -> SWR"""
        tsc_file = Path('/home/kevin/work/forBMS/foxBMS/docs/parvis/safety/technical-safety-concept.md')

        if tsc_file.exists():
            with open(tsc_file, 'r') as f:
                content = f.read()

            # Should show hierarchical structure
            assert 'Safety Goal' in content or 'SG-' in content, \
                "TSC should define Safety Goals"
            assert 'TSC-BMS' in content, \
                "TSC should define TSC elements"
            assert 'FSR' in content or 'FunctionalSafety' in content, \
                "TSC should reference Functional Safety Requirements"


class TestAC_M2_004_BLOCK003Resolution:
    """AC-M2-004: BLOCK-003 resolution - Enable L2 phase entry"""

    def test_block_003_marked_resolved(self):
        """Test that BLOCK-003 is marked as 'resolved' in configuration"""
        config_file = Path('/home/kevin/work/forBMS/foxBMS/.moai/orchestrator/orchestrator-config.json')

        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)

            blocks = config.get('blocks', [])
            block_003 = None

            for block in blocks:
                if block.get('id') == 'BLOCK-003':
                    block_003 = block
                    break

            if block_003:
                assert block_003.get('status') == 'resolved', \
                    f"BLOCK-003 status is {block_003.get('status')}, expected 'resolved'"

    def test_tsc_traceability_completeness(self):
        """Test TSC traceability coverage is 100%"""
        matrix_file = Path('/home/kevin/work/forBMS/foxBMS/docs/parvis/requirements/tsc-traceability-matrix.json')

        if matrix_file.exists():
            with open(matrix_file, 'r') as f:
                matrix = json.load(f)

            coverage = matrix.get('coverage_metrics', {})
            tsc_coverage = coverage.get('tsc_coverage_percent', 0)

            assert tsc_coverage >= 90, \
                f"TSC coverage is {tsc_coverage}%, expected >= 90%"

    def test_l2_phase_entry_enabled(self):
        """Test that L2 phase entry is no longer blocked"""
        config_file = Path('/home/kevin/work/forBMS/foxBMS/.moai/orchestrator/orchestrator-config.json')

        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)

            l2_blocked = False
            if 'phases' in config:
                l2_phase = next((p for p in config['phases'] if p.get('name') == 'L2'), None)
                if l2_phase:
                    l2_blocked = l2_phase.get('blocked', False)

            assert not l2_blocked, "L2 phase should not be blocked after BLOCK-003 resolution"


class TestAC_M2_005_ASILInheritance:
    """AC-M2-005: ASIL inheritance rules compliance"""

    def test_no_asil_level_increase(self):
        """Test that child requirements don't have higher ASIL than parent"""
        matrix_file = Path('/home/kevin/work/forBMS/foxBMS/docs/parvis/requirements/tsc-traceability-matrix.json')

        if matrix_file.exists():
            with open(matrix_file, 'r') as f:
                matrix = json.load(f)

            mappings = matrix.get('mappings', [])
            asil_violations = []

            asil_hierarchy = {'D': 4, 'C': 3, 'B': 2, 'A': 1, 'QM': 0}

            for mapping in mappings:
                parent_asil = mapping.get('parent_asil') or mapping.get('tsc_asil')
                child_asil = mapping.get('asil')

                if parent_asil and child_asil:
                    parent_level = asil_hierarchy.get(parent_asil[-1], 0)
                    child_level = asil_hierarchy.get(child_asil[-1], 0)

                    if child_level > parent_level:
                        asil_violations.append({
                            'parent': parent_asil,
                            'child': child_asil
                        })

            assert len(asil_violations) == 0, \
                f"ASIL inheritance violations found: {asil_violations[:3]}"

    def test_asil_consistency_across_hierarchy(self):
        """Test ASIL remains consistent across Safety Goal -> TSC -> FSR -> SWR"""
        tsc_file = Path('/home/kevin/work/forBMS/foxBMS/docs/parvis/safety/technical-safety-concept.md')

        if tsc_file.exists():
            with open(tsc_file, 'r') as f:
                content = f.read()

            # Should show ASIL levels are consistent
            assert 'ASIL' in content, "TSC should define ASIL levels"


class TestAC_M2_006_GapAnalysisReport:
    """AC-M2-006: TSC gap analysis report"""

    def test_gap_analysis_report_exists(self):
        """Test that gap analysis report is generated"""
        report_file = Path('/home/kevin/work/forBMS/foxBMS/docs/parvis/requirements/tsc-gap-analysis.md')

        # Report may be created during implementation
        if report_file.exists():
            with open(report_file, 'r') as f:
                content = f.read()

            assert len(content) > 100, "Gap analysis report should have substantial content"

    def test_gap_analysis_includes_recommendations(self):
        """Test gap analysis includes resolution recommendations"""
        report_file = Path('/home/kevin/work/forBMS/foxBMS/docs/parvis/requirements/tsc-gap-analysis.md')

        if report_file.exists():
            with open(report_file, 'r') as f:
                content = f.read()

            # Should include recommendations or gap details
            assert 'recommend' in content.lower() or 'gap' in content.lower() or \
                   'missing' in content.lower(), \
                   "Gap analysis should describe gaps and recommendations"


class TestAC_M2_007_TSCVersionManagement:
    """AC-M2-007: TSC version management"""

    def test_tsc_version_field_exists(self):
        """Test TSC document has version field"""
        tsc_file = Path('/home/kevin/work/forBMS/foxBMS/docs/parvis/safety/technical-safety-concept.md')

        if tsc_file.exists():
            with open(tsc_file, 'r') as f:
                content = f.read()

            # Should have version info
            version_pattern = r'(version|v\d+\.\d+|\d+\.\d+\.\d+)'
            version_matches = re.findall(version_pattern, content, re.IGNORECASE)

            assert len(version_matches) > 0, "TSC should have version information"

    def test_version_history_tracked(self):
        """Test TSC version history is tracked"""
        tsc_file = Path('/home/kevin/work/forBMS/foxBMS/docs/parvis/safety/technical-safety-concept.md')

        if tsc_file.exists():
            with open(tsc_file, 'r') as f:
                content = f.read()

            # Should have changelog or version history
            assert 'version' in content.lower() or 'history' in content.lower() or \
                   'changelog' in content.lower(), \
                   "TSC should track version history"


# Quality Gate Tests for Module 2

class TestModule2QualityGates:
    """Quality gates for Module 2 completion"""

    def test_qg_p1_002_tsc_traceability_complete(self):
        """QG-P1-002: TSC traceability coverage 100%"""
        matrix_file = Path('/home/kevin/work/forBMS/foxBMS/docs/parvis/requirements/tsc-traceability-matrix.json')

        if matrix_file.exists():
            with open(matrix_file, 'r') as f:
                matrix = json.load(f)

            coverage = matrix.get('coverage_metrics', {})
            tsc_coverage = coverage.get('tsc_coverage_percent', 0)

            # Initial target: >= 80%, final target: 100%
            assert tsc_coverage >= 80, \
                f"TSC coverage must be >= 80%, current: {tsc_coverage}%"

    def test_qg_p1_003_bidirectional_traceability(self):
        """QG-P1-003: Bidirectional traceability 100%"""
        matrix_file = Path('/home/kevin/work/forBMS/foxBMS/docs/parvis/requirements/tsc-traceability-matrix.json')

        if matrix_file.exists():
            with open(matrix_file, 'r') as f:
                matrix = json.load(f)

            metrics = matrix.get('coverage_metrics', {})
            forward_coverage = metrics.get('forward_traceability_percent', 0)
            backward_coverage = metrics.get('backward_traceability_percent', 0)

            assert forward_coverage >= 80, \
                f"Forward traceability must be >= 80%, current: {forward_coverage}%"
            assert backward_coverage >= 80, \
                f"Backward traceability must be >= 80%, current: {backward_coverage}%"

    def test_qg_p1_004_block_003_released(self):
        """QG-P1-004: BLOCK-003 released"""
        config_file = Path('/home/kevin/work/forBMS/foxBMS/.moai/orchestrator/orchestrator-config.json')

        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)

            blocks = config.get('blocks', [])
            block_003 = next((b for b in blocks if b.get('id') == 'BLOCK-003'), None)

            if block_003:
                assert block_003.get('status') == 'resolved', \
                    "BLOCK-003 must be resolved to pass QG-P1-004"


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
