#!/usr/bin/env python3
"""
PARVIS Orchestrator Engine - Phase tracking and quality gate management
Manages V-Model phase transitions and quality gate enforcement
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Tuple
from enum import Enum
from dataclasses import dataclass, asdict


class PhaseStatus(Enum):
    """Phase status enumeration"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class QualityGateStatus(Enum):
    """Quality gate status"""
    PASSED = "passed"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"


@dataclass
class QualityGateCriteria:
    """Quality gate criteria definition"""
    name: str
    description: str
    min_value: float
    current_value: float = 0.0
    metric_name: str = ""

    def is_passed(self) -> bool:
        """Check if criteria is passed"""
        return self.current_value >= self.min_value

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "min_value": self.min_value,
            "current_value": self.current_value,
            "metric_name": self.metric_name,
            "status": "passed" if self.is_passed() else "failed"
        }


class PhaseDef:
    """Phase definition with entry and exit criteria"""

    PHASES = {
        "L1": {
            "name": "Level 1: Requirement Extraction",
            "description": "Extract requirements from source code",
            "entry_criteria": ["Source files available", "Configuration loaded"],
            "exit_criteria": ["Extraction confidence >= 70%", "All source files processed"],
            "quality_gates": {
                "extraction_confidence": {"min": 0.7, "metric": "High confidence ratio"},
                "source_coverage": {"min": 0.6, "metric": "Source file coverage"}
            }
        },
        "L2": {
            "name": "Level 2: Requirement Normalization",
            "description": "Normalize and structure extracted requirements",
            "entry_criteria": ["L1 completed", "Extraction confidence >= 70%"],
            "exit_criteria": ["All requirements normalized", "IDs assigned"],
            "quality_gates": {
                "normalization_complete": {"min": 1.0, "metric": "Normalization coverage"},
                "id_assignment": {"min": 1.0, "metric": "ID assignment coverage"}
            }
        },
        "L3": {
            "name": "Level 3: Safety Analysis",
            "description": "Perform ISO 26262 and ASPICE safety analysis",
            "entry_criteria": ["L2 completed", "All requirements normalized"],
            "exit_criteria": ["Safety analysis complete", "ASIL determined"],
            "quality_gates": {
                "safety_analysis": {"min": 1.0, "metric": "Safety analysis coverage"},
                "asil_determination": {"min": 1.0, "metric": "ASIL assignment"}
            }
        },
        "L4": {
            "name": "Level 4: Specification Documentation",
            "description": "Generate ASPICE specification artifacts",
            "entry_criteria": ["L3 completed", "Safety analysis done"],
            "exit_criteria": ["Specification documents generated", "Traceability verified"],
            "quality_gates": {
                "spec_generation": {"min": 1.0, "metric": "Specification coverage"},
                "traceability": {"min": 0.95, "metric": "Bidirectional traceability"}
            }
        },
        "R1": {
            "name": "Right Side Phase 1: Implementation Planning",
            "description": "Plan implementation and testing strategy",
            "entry_criteria": ["L4 completed"],
            "exit_criteria": ["Implementation plan ready", "Test strategy defined"],
            "quality_gates": {
                "implementation_plan": {"min": 1.0, "metric": "Plan completeness"},
                "test_strategy": {"min": 1.0, "metric": "Strategy definition"}
            }
        },
        "R2": {
            "name": "Right Side Phase 2: Implementation",
            "description": "Implement software according to specification",
            "entry_criteria": ["R1 completed"],
            "exit_criteria": ["Code implementation complete", "Unit tests passing"],
            "quality_gates": {
                "implementation_complete": {"min": 1.0, "metric": "Code coverage"},
                "unit_test_pass": {"min": 1.0, "metric": "Test pass rate"}
            }
        },
        "R3": {
            "name": "Right Side Phase 3: Verification",
            "description": "Verify implementation against specification",
            "entry_criteria": ["R2 completed"],
            "exit_criteria": ["Integration tests passing", "Test coverage >= 85%"],
            "quality_gates": {
                "integration_test": {"min": 1.0, "metric": "Integration test pass rate"},
                "test_coverage": {"min": 0.85, "metric": "Code coverage percentage"}
            }
        },
        "R4": {
            "name": "Right Side Phase 4: Validation",
            "description": "Validate system meets all requirements",
            "entry_criteria": ["R3 completed"],
            "exit_criteria": ["All tests passed", "Traceability verified", "Ready for release"],
            "quality_gates": {
                "all_tests_pass": {"min": 1.0, "metric": "Final test pass rate"},
                "final_traceability": {"min": 1.0, "metric": "Complete traceability"}
            }
        }
    }

    def __init__(self, phase_id: str):
        """Initialize phase definition"""
        if phase_id not in self.PHASES:
            raise ValueError(f"Unknown phase: {phase_id}")
        self.phase_id = phase_id
        self.data = self.PHASES[phase_id]

    @property
    def name(self) -> str:
        """Get phase name"""
        return self.data["name"]

    @property
    def description(self) -> str:
        """Get phase description"""
        return self.data["description"]

    @property
    def entry_criteria(self) -> List[str]:
        """Get entry criteria"""
        return self.data["entry_criteria"]

    @property
    def exit_criteria(self) -> List[str]:
        """Get exit criteria"""
        return self.data["exit_criteria"]

    @property
    def quality_gates(self) -> Dict[str, Dict[str, Any]]:
        """Get quality gates"""
        return self.data["quality_gates"]


class ModulePhaseStatus:
    """Tracks phase status for a module"""

    PHASE_ORDER = ["L1", "L2", "L3", "L4", "R1", "R2", "R3", "R4"]

    def __init__(self, module_id: str, status_file: Path):
        """Initialize module phase status"""
        self.module_id = module_id
        self.status_file = status_file
        self.data = self._load_status()

    def _load_status(self) -> Dict[str, Any]:
        """Load status from file"""
        if self.status_file.exists():
            with open(self.status_file, 'r') as f:
                return json.load(f)
        return self._create_default_status()

    def _create_default_status(self) -> Dict[str, Any]:
        """Create default status structure"""
        return {
            "module_id": self.module_id,
            "current_phase": "L1",
            "phase_status": {phase: PhaseStatus.NOT_STARTED.value for phase in self.PHASE_ORDER},
            "quality_gates": {},
            "extraction_status": {},
            "last_updated": datetime.now().isoformat() + "Z",
            "created_at": datetime.now().isoformat() + "Z"
        }

    def get_current_phase(self) -> str:
        """Get current phase"""
        return self.data.get("current_phase", "L1")

    def get_phase_status(self, phase_id: str) -> str:
        """Get status of specific phase"""
        return self.data["phase_status"].get(phase_id, PhaseStatus.NOT_STARTED.value)

    def can_enter_phase(self, phase_id: str) -> Tuple[bool, List[str]]:
        """Check if phase entry criteria are met"""
        phase_def = PhaseDef(phase_id)
        current_index = self.PHASE_ORDER.index(phase_id)

        # Check if dependencies are completed
        blocking_reasons = []

        # Check entry criteria based on dependency
        if phase_id.startswith("L"):
            if phase_id != "L1":
                prev_phase = self.PHASE_ORDER[current_index - 1]
                if self.get_phase_status(prev_phase) != PhaseStatus.COMPLETED.value:
                    blocking_reasons.append(f"Previous phase {prev_phase} not completed")

        elif phase_id.startswith("R"):
            l4_status = self.get_phase_status("L4")
            if l4_status != PhaseStatus.COMPLETED.value:
                blocking_reasons.append("L4 specification phase not completed")

        return len(blocking_reasons) == 0, blocking_reasons

    def update_phase_status(self, phase_id: str, status: str) -> None:
        """Update phase status"""
        self.data["phase_status"][phase_id] = status
        self.data["last_updated"] = datetime.now().isoformat() + "Z"

    def update_quality_gate(self, phase_id: str, gate_name: str, current_value: float,
                          min_value: float, passed: bool) -> None:
        """Update quality gate status"""
        if phase_id not in self.data["quality_gates"]:
            self.data["quality_gates"][phase_id] = {}

        self.data["quality_gates"][phase_id][gate_name] = {
            "min_value": min_value,
            "current_value": current_value,
            "status": "passed" if passed else "failed"
        }

    def can_transition_to_next(self, phase_id: str) -> Tuple[bool, List[str]]:
        """Check if phase exit criteria are met"""
        phase_def = PhaseDef(phase_id)
        gates = self.data["quality_gates"].get(phase_id, {})

        blocking_reasons = []

        # Check if all quality gates passed
        for gate_name, gate_data in gates.items():
            if gate_data.get("status") == "failed":
                blocking_reasons.append(f"Quality gate '{gate_name}' failed")

        return len(blocking_reasons) == 0, blocking_reasons

    def transition_to_next_phase(self, phase_id: str) -> Tuple[bool, str]:
        """Transition to next phase if criteria met"""
        # Verify current phase exit criteria
        can_transition, reasons = self.can_transition_to_next(phase_id)

        if not can_transition:
            return False, f"Cannot transition: {'; '.join(reasons)}"

        # Mark current phase as completed
        self.update_phase_status(phase_id, PhaseStatus.COMPLETED.value)

        # Find next phase
        current_index = self.PHASE_ORDER.index(phase_id)
        if current_index < len(self.PHASE_ORDER) - 1:
            next_phase = self.PHASE_ORDER[current_index + 1]

            # Verify entry criteria for next phase
            can_enter, entry_reasons = self.can_enter_phase(next_phase)
            if can_enter:
                self.update_phase_status(next_phase, PhaseStatus.IN_PROGRESS.value)
                self.data["current_phase"] = next_phase
                self.save()
                return True, f"Transitioned from {phase_id} to {next_phase}"
            else:
                return False, f"Cannot enter {next_phase}: {'; '.join(entry_reasons)}"
        else:
            self.save()
            return True, f"Phase {phase_id} completed - all phases done"

    def save(self) -> None:
        """Save status to file"""
        self.status_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.status_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def get_report(self) -> str:
        """Generate phase status report"""
        report = []
        report.append(f"# Phase Status Report: {self.module_id}")
        report.append("")
        report.append(f"**Current Phase**: {self.data['current_phase']}")
        report.append(f"**Last Updated**: {self.data['last_updated']}")
        report.append("")

        report.append("## Phase Timeline")
        report.append("")
        for phase in self.PHASE_ORDER:
            status = self.get_phase_status(phase)
            phase_def = PhaseDef(phase)
            status_icon = {
                PhaseStatus.NOT_STARTED.value: "⭕",
                PhaseStatus.IN_PROGRESS.value: "🟡",
                PhaseStatus.COMPLETED.value: "✅",
                PhaseStatus.BLOCKED.value: "🚫"
            }.get(status, "?")
            report.append(f"- {status_icon} **{phase}**: {phase_def.name} - {status}")

        report.append("")
        report.append("## Quality Gates")
        report.append("")
        for phase_id, gates in self.data.get("quality_gates", {}).items():
            report.append(f"### {phase_id}")
            if isinstance(gates, dict):
                for gate_name, gate_status in gates.items():
                    if isinstance(gate_status, dict):
                        status = "PASSED" if gate_status.get("status") == "passed" else "FAILED"
                        current = gate_status.get("current_value", 0)
                        minimum = gate_status.get("min_value", 0)
                        report.append(f"- {status}: {gate_name} ({current:.1%} / {minimum:.1%})")
                    else:
                        report.append(f"- {gate_name}: {gate_status}")
            report.append("")

        return '\n'.join(report)


class OrchestratorEngine:
    """Main orchestration engine"""

    def __init__(self, bms_config_path: Path):
        """Initialize orchestrator"""
        self.bms_config_path = Path(bms_config_path)
        self.status_file = self.bms_config_path / "phase-status" / "BMS.json"

    def get_module_status(self, module_id: str = "BMS") -> ModulePhaseStatus:
        """Get module phase status"""
        return ModulePhaseStatus(module_id, self.status_file)

    def verify_quality_gates(self, module_id: str, phase_id: str,
                            metrics: Dict[str, float]) -> Tuple[bool, List[str]]:
        """Verify quality gates for phase"""
        phase_def = PhaseDef(phase_id)
        gates = phase_def.quality_gates
        failures = []

        for gate_name, gate_config in gates.items():
            min_value = gate_config.get("min", 0.0)
            current_value = metrics.get(gate_name, 0.0)

            if current_value < min_value:
                failures.append(f"{gate_name}: {current_value:.1%} < {min_value:.1%}")

        return len(failures) == 0, failures

    def enforce_quality_gates(self, module_id: str, phase_id: str,
                            metrics: Dict[str, float]) -> None:
        """Enforce quality gates and update status"""
        status = self.get_module_status(module_id)
        phase_def = PhaseDef(phase_id)

        passed, failures = self.verify_quality_gates(module_id, phase_id, metrics)

        for gate_name, gate_config in phase_def.quality_gates.items():
            current_value = metrics.get(gate_name, 0.0)
            min_value = gate_config.get("min", 0.0)
            status.update_quality_gate(phase_id, gate_name, current_value, min_value,
                                      current_value >= min_value)

        status.save()

        if not passed:
            status.update_phase_status(phase_id, PhaseStatus.BLOCKED.value)
            status.save()
            return

        # Try to transition to next phase
        success, message = status.transition_to_next_phase(phase_id)

    def get_phase_report(self, module_id: str = "BMS") -> str:
        """Get phase status report"""
        status = self.get_module_status(module_id)
        return status.get_report()

    def get_metrics_for_phase(self, module_id: str, phase_id: str) -> Dict[str, float]:
        """Get current metrics for phase"""
        status = self.get_module_status(module_id)
        gates = status.data["quality_gates"].get(phase_id, {})

        metrics = {}
        for gate_name, gate_status in gates.items():
            metrics[gate_name] = gate_status.get("current_value", 0.0)

        return metrics


def main():
    """Main entry point"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: orchestrator_engine.py <command> [args]")
        print("Commands:")
        print("  status <module>                     - Get phase status")
        print("  report <module>                     - Generate phase report")
        print("  transition <module> <phase>         - Attempt phase transition")
        print("  verify-gates <module> <phase> <json> - Verify quality gates")
        sys.exit(1)

    command = sys.argv[1]
    config_path = Path(".claude/parvis-data/config")
    engine = OrchestratorEngine(config_path)

    if command == "status":
        module = sys.argv[2] if len(sys.argv) > 2 else "BMS"
        status = engine.get_module_status(module)
        print(json.dumps(status.data, indent=2))

    elif command == "report":
        module = sys.argv[2] if len(sys.argv) > 2 else "BMS"
        report = engine.get_phase_report(module)
        print(report)

    elif command == "transition":
        module = sys.argv[2] if len(sys.argv) > 2 else "BMS"
        phase = sys.argv[3] if len(sys.argv) > 3 else "L1"
        status = engine.get_module_status(module)
        success, message = status.transition_to_next_phase(phase)
        print(f"Transition {'successful' if success else 'failed'}: {message}")

    elif command == "verify-gates":
        module = sys.argv[2] if len(sys.argv) > 2 else "BMS"
        phase = sys.argv[3] if len(sys.argv) > 3 else "L1"
        metrics_json = sys.argv[4] if len(sys.argv) > 4 else "{}"
        metrics = json.loads(metrics_json)
        engine.enforce_quality_gates(module, phase, metrics)
        print("Quality gates verified and status updated")


if __name__ == "__main__":
    main()
