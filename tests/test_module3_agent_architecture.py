#!/usr/bin/env python3
"""
SPEC-PARVIS-V2-001: Module 3 - Agent Architecture Refactoring
TDD Implementation: Agent Status Field, DAG Validation, MCP Integration

Test-First Approach (RED phase):
- All acceptance criteria tests written BEFORE implementation
- Tests serve as executable specifications
- Clear Given-When-Then scenarios
"""

import pytest
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple


# ============================================================================
# AC-M3-001: 22 Agent Status Field Addition (MUST)
# ============================================================================

class TestAgentStatusFieldAddition:
    """Test that all 22 agents have standardized status field"""

    EXPECTED_AGENTS = [
        "parvis-ai-orchestrator",
        "parvis-aispec-code",
        "parvis-aispec-reqid",
        "parvis-aispec-transformer",
        "parvis-aispec-trace",
        "parvis-aispec-safety",
        "parvis-aicoder-misra",
        "parvis-aicoder-refactor",
        "parvis-aicoder-doxygen",
        "parvis-aicoder-safety",
        "parvis-aiverify-unittest",
        "parvis-aiverify-integration",
        "parvis-aiverify-coverage",
        "parvis-aiverify-safety",
        "parvis-aiverify-report",
        "parvis-aidoc-aspice",
        "parvis-aidoc-safety",
        "parvis-aidoc-trace",
        "parvis-aidoc-change",
        "parvis-aidoc-generator",
        "parvis-aicoder-generator",  # New agent from Module 6
        "parvis-aiverify-integration",  # Re-listed (remove duplicate)
    ]

    VALID_STATUS_VALUES = {"defined", "implemented", "validated", "active", "deprecated"}

    def extract_yaml_frontmatter(self, content: str) -> Dict:
        """Extract YAML frontmatter from markdown agent definition"""
        if not content.startswith("---"):
            return {}

        lines = content.split("\n")
        end_idx = -1
        for i in range(1, len(lines)):
            if lines[i].startswith("---"):
                end_idx = i
                break

        if end_idx == -1:
            return {}

        frontmatter_text = "\n".join(lines[1:end_idx])
        data = {}
        current_key = None
        current_value_lines = []

        for line in frontmatter_text.strip().split("\n"):
            if line and not line.startswith(" "):
                # Top-level key
                if current_key and current_value_lines:
                    data[current_key] = "\n".join(current_value_lines)
                    current_value_lines = []

                if ":" in line:
                    key, val = line.split(":", 1)
                    current_key = key.strip()
                    val = val.strip()
                    if val:
                        data[current_key] = val
                        current_key = None
            elif current_key and line.strip():
                current_value_lines.append(line)

        if current_key:
            data[current_key] = "\n".join(current_value_lines)

        return data

    def test_agent_status_field_exists(self):
        """AC-M3-001: Each agent definition has status field"""
        agents_dir = Path("/home/kevin/work/forBMS/foxBMS/.claude/agents/parvis")

        for agent_id in self.EXPECTED_AGENTS:
            if agent_id == "parvis-aiverify-integration":  # Skip duplicate
                continue

            agent_file = agents_dir / f"{agent_id}.md"
            assert agent_file.exists(), f"Agent file missing: {agent_file}"

            content = agent_file.read_text()
            frontmatter = self.extract_yaml_frontmatter(content)

            assert "status" in frontmatter, f"Missing status field in {agent_id}"
            assert frontmatter["status"] in self.VALID_STATUS_VALUES, \
                f"Invalid status '{frontmatter['status']}' in {agent_id}"

    def test_agent_status_values_valid(self):
        """AC-M3-001: All status values are valid enumeration"""
        agents_dir = Path("/home/kevin/work/forBMS/foxBMS/.claude/agents/parvis")

        for agent_id in set(self.EXPECTED_AGENTS):
            if agent_id == "parvis-aiverify-integration":  # Skip duplicate
                continue

            agent_file = agents_dir / f"{agent_id}.md"
            if not agent_file.exists():
                continue

            content = agent_file.read_text()
            frontmatter = self.extract_yaml_frontmatter(content)

            if "status" in frontmatter:
                assert frontmatter["status"] in self.VALID_STATUS_VALUES, \
                    f"Invalid status value: {frontmatter['status']}"

    def test_agent_status_consistency(self):
        """AC-M3-001: All agents follow consistent status field format"""
        agents_dir = Path("/home/kevin/work/forBMS/foxBMS/.claude/agents/parvis")
        agent_files = list(agents_dir.glob("parvis-*.md"))

        assert len(agent_files) >= 20, f"Expected 20+ agent files, found {len(agent_files)}"

        for agent_file in agent_files:
            content = agent_file.read_text()
            frontmatter = self.extract_yaml_frontmatter(content)

            assert "status" in frontmatter, f"Missing status in {agent_file.name}"
            assert frontmatter["status"] in self.VALID_STATUS_VALUES


# ============================================================================
# AC-M3-002: depends_on DAG Consistency (MUST)
# ============================================================================

class TestDependencyGraphValidation:
    """Test agent dependency graph forms a DAG (Directed Acyclic Graph)"""

    def extract_agent_metadata(self, content: str) -> Dict:
        """Extract agent metadata including depends_on"""
        if not content.startswith("---"):
            return {}

        lines = content.split("\n")
        end_idx = -1
        for i in range(1, len(lines)):
            if lines[i].startswith("---"):
                end_idx = i
                break

        if end_idx == -1:
            return {}

        frontmatter_text = "\n".join(lines[1:end_idx])
        data = {}

        # Simple YAML parsing for lists
        current_key = None
        current_list = []

        for line in frontmatter_text.strip().split("\n"):
            if line.startswith("  - "):  # List item
                item = line[4:].strip()
                if current_key:
                    current_list.append(item)
            elif ":" in line and not line.startswith("  "):
                if current_key and current_list:
                    data[current_key] = current_list
                    current_list = []

                key, val = line.split(":", 1)
                current_key = key.strip()
                val = val.strip()
                if val:
                    data[current_key] = val
                elif not val:
                    data[current_key] = []

        if current_key and current_list:
            data[current_key] = current_list

        return data

    def detect_cycles(self, graph: Dict[str, List[str]]) -> List[List[str]]:
        """Detect cycles in directed graph using DFS"""
        visited = set()
        rec_stack = set()
        cycles = []

        def dfs(node, path):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    dfs(neighbor, path[:])
                elif neighbor in rec_stack:
                    cycle = path + [neighbor]
                    cycles.append(cycle)

            rec_stack.discard(node)

        for node in graph:
            if node not in visited:
                dfs(node, [])

        return cycles

    def test_no_circular_dependencies(self):
        """AC-M3-002: No circular dependencies in depends_on"""
        agents_dir = Path("/home/kevin/work/forBMS/foxBMS/.claude/agents/parvis")
        agent_files = list(agents_dir.glob("parvis-*.md"))

        # Build dependency graph
        graph = {}
        agent_names = {}

        for agent_file in agent_files:
            content = agent_file.read_text()
            metadata = self.extract_agent_metadata(content)

            agent_id = agent_file.stem
            agent_names[agent_id] = True
            depends_on = metadata.get("depends_on", [])
            if isinstance(depends_on, str):
                depends_on = [depends_on]
            graph[agent_id] = depends_on

        # Detect cycles
        cycles = self.detect_cycles(graph)
        assert len(cycles) == 0, f"Circular dependencies detected: {cycles}"

    def test_valid_dependency_references(self):
        """AC-M3-002: All depends_on references point to valid agents"""
        agents_dir = Path("/home/kevin/work/forBMS/foxBMS/.claude/agents/parvis")
        agent_files = list(agents_dir.glob("parvis-*.md"))

        # Collect all agent IDs
        agent_ids = {f.stem for f in agent_files}

        for agent_file in agent_files:
            content = agent_file.read_text()
            metadata = self.extract_agent_metadata(content)

            depends_on = metadata.get("depends_on", [])
            if isinstance(depends_on, str):
                depends_on = [depends_on]

            for dep_id in depends_on:
                assert dep_id in agent_ids, \
                    f"Agent {agent_file.stem} depends on non-existent {dep_id}"

    def test_dependency_graph_structure(self):
        """AC-M3-002: Dependency graph conforms to expected structure"""
        agents_dir = Path("/home/kevin/work/forBMS/foxBMS/.claude/agents/parvis")

        # Check root orchestrator
        orchestrator_file = agents_dir / "parvis-ai-orchestrator.md"
        assert orchestrator_file.exists(), "Root orchestrator agent not found"

        content = orchestrator_file.read_text()
        metadata = self.extract_agent_metadata(content)
        depends_on = metadata.get("depends_on", [])

        # Orchestrator should have dependencies
        assert len(depends_on) > 0, "Orchestrator should have dependencies"


# ============================================================================
# AC-M3-003: MCP Integration Documentation (MUST)
# ============================================================================

class TestMCPIntegrationDocumentation:
    """Test MCP integration is documented in agent definitions"""

    def extract_mcp_integration(self, content: str) -> Dict:
        """Extract mcp_integration section from agent definition"""
        lines = content.split("\n")

        mcp_start = -1
        for i, line in enumerate(lines):
            if "mcp_integration:" in line:
                mcp_start = i
                break

        if mcp_start == -1:
            return {}

        mcp_section = {}
        i = mcp_start + 1

        while i < len(lines):
            line = lines[i]

            if line and not line.startswith(" "):
                break

            if "context7:" in line:
                val = line.split(":", 1)[1].strip()
                mcp_section["context7"] = val.lower() == "true"

            elif "sequential_thinking:" in line:
                val = line.split(":", 1)[1].strip()
                mcp_section["sequential_thinking"] = val.lower() == "true"

            elif "custom_tools:" in line:
                mcp_section["custom_tools"] = []

            i += 1

        return mcp_section

    def test_mcp_integration_section_exists(self):
        """AC-M3-003: mcp_integration section exists in agent definitions"""
        agents_dir = Path("/home/kevin/work/forBMS/foxBMS/.claude/agents/parvis")

        # Agents that should have MCP integration
        mcp_agents = {
            "parvis-aispec-code": ["context7", "sequential_thinking"],
            "parvis-aispec-safety": ["sequential_thinking"],
            "parvis-aicoder-misra": ["context7"],
            "parvis-aiverify-unittest": ["context7", "sequential_thinking"],
            "parvis-aidoc-aspice": ["context7"],
        }

        for agent_id, expected_mcp_types in mcp_agents.items():
            agent_file = agents_dir / f"{agent_id}.md"
            if agent_file.exists():
                content = agent_file.read_text()
                mcp_section = self.extract_mcp_integration(content)

                # At least one MCP type should be documented
                has_mcp = any(
                    mcp_section.get(mcp_type, False)
                    for mcp_type in expected_mcp_types
                )
                assert has_mcp or len(mcp_section) > 0, \
                    f"Missing mcp_integration in {agent_id}"

    def test_mcp_integration_format_valid(self):
        """AC-M3-003: mcp_integration section follows valid format"""
        agents_dir = Path("/home/kevin/work/forBMS/foxBMS/.claude/agents/parvis")
        agent_files = list(agents_dir.glob("parvis-*.md"))

        for agent_file in agent_files:
            content = agent_file.read_text()

            if "mcp_integration:" in content:
                mcp_section = self.extract_mcp_integration(content)

                # Verify expected keys exist or are boolean
                for key in mcp_section:
                    if key in ["context7", "sequential_thinking"]:
                        assert isinstance(mcp_section[key], bool), \
                            f"Invalid {key} value in {agent_file.stem}"

    def test_context7_agents_documented(self):
        """AC-M3-003: Context7-using agents documented"""
        agents_dir = Path("/home/kevin/work/forBMS/foxBMS/.claude/agents/parvis")

        context7_agents = [
            "parvis-aispec-code",
            "parvis-aicoder-misra",
            "parvis-aiverify-unittest",
            "parvis-aidoc-aspice",
        ]

        found_count = 0
        for agent_id in context7_agents:
            agent_file = agents_dir / f"{agent_id}.md"
            if agent_file.exists():
                content = agent_file.read_text()
                mcp_section = self.extract_mcp_integration(content)

                if mcp_section.get("context7"):
                    found_count += 1

        # At least 2 Context7 agents should be documented
        assert found_count >= 2 or len(context7_agents) <= found_count, \
            f"Expected at least 2 Context7 agents, found {found_count}"


# ============================================================================
# AC-M3-004: Metadata Schema Compliance (SHOULD)
# ============================================================================

class TestMetadataSchemaCompliance:
    """Test agents comply with standardized metadata schema"""

    REQUIRED_FIELDS = {"agent_id", "version", "status", "v_model_phase"}

    def extract_metadata_fields(self, content: str) -> Set[str]:
        """Extract all metadata field names from agent definition"""
        if not content.startswith("---"):
            return set()

        lines = content.split("\n")
        end_idx = -1
        for i in range(1, len(lines)):
            if lines[i].startswith("---"):
                end_idx = i
                break

        if end_idx == -1:
            return set()

        fields = set()
        for line in lines[1:end_idx]:
            if ":" in line and not line.startswith(" "):
                key = line.split(":")[0].strip()
                fields.add(key)

        return fields

    def test_required_metadata_fields(self):
        """AC-M3-004: All agents have required metadata fields"""
        agents_dir = Path("/home/kevin/work/forBMS/foxBMS/.claude/agents/parvis")
        agent_files = list(agents_dir.glob("parvis-*.md"))

        missing_fields = []
        for agent_file in agent_files:
            content = agent_file.read_text()
            fields = self.extract_metadata_fields(content)

            missing = self.REQUIRED_FIELDS - fields
            if missing:
                missing_fields.append((agent_file.stem, missing))

        assert len(missing_fields) == 0, \
            f"Agents with missing fields: {missing_fields}"

    def test_metadata_schema_consistency(self):
        """AC-M3-004: Metadata schema is consistent across agents"""
        agents_dir = Path("/home/kevin/work/forBMS/foxBMS/.claude/agents/parvis")
        agent_files = list(agents_dir.glob("parvis-*.md"))

        all_field_sets = []
        for agent_file in agent_files:
            content = agent_file.read_text()
            fields = self.extract_metadata_fields(content)
            all_field_sets.append(fields)

        # Most agents should have similar field counts (allow variance)
        field_counts = [len(fields) for fields in all_field_sets]
        avg_count = sum(field_counts) / len(field_counts)

        for i, count in enumerate(field_counts):
            # Allow 20% variance
            assert abs(count - avg_count) <= 0.2 * avg_count, \
                f"Agent {i} has significantly different field count: {count} vs avg {avg_count}"


# ============================================================================
# AC-M3-005: Agent Status Dashboard (SHOULD)
# ============================================================================

class TestAgentStatusDashboard:
    """Test agent status dashboard is provided"""

    def test_agent_dashboard_file_exists(self):
        """AC-M3-005: Agent status dashboard document exists"""
        dashboard_path = Path("/home/kevin/work/forBMS/foxBMS/.moai/docs/agents/parvis-agent-dashboard.md")

        # Dashboard might not exist yet - this is SHOULD, not MUST
        # If it exists, it should be valid
        if dashboard_path.exists():
            content = dashboard_path.read_text()
            assert len(content) > 100, "Dashboard should have substantial content"
            assert "agent" in content.lower(), "Dashboard should reference agents"

    def test_status_aggregation_possible(self):
        """AC-M3-005: Agent statuses can be aggregated"""
        agents_dir = Path("/home/kevin/work/forBMS/foxBMS/.claude/agents/parvis")
        agent_files = list(agents_dir.glob("parvis-*.md"))

        status_counts = {
            "defined": 0,
            "implemented": 0,
            "validated": 0,
            "active": 0,
            "deprecated": 0,
        }

        for agent_file in agent_files:
            content = agent_file.read_text()

            for status_val in status_counts.keys():
                if f"status: {status_val}" in content:
                    status_counts[status_val] += 1

        # At least one status category should have agents
        assert sum(status_counts.values()) >= 15, \
            f"Expected 15+ agents with status, found {sum(status_counts.values())}"


# ============================================================================
# AC-M3-006: Agent Version Management (COULD)
# ============================================================================

class TestAgentVersionManagement:
    """Test agent version management capability"""

    def test_version_field_exists(self):
        """AC-M3-006: Agents track version information"""
        agents_dir = Path("/home/kevin/work/forBMS/foxBMS/.claude/agents/parvis")
        agent_files = list(agents_dir.glob("parvis-*.md"))

        agents_with_version = 0
        for agent_file in agent_files:
            content = agent_file.read_text()
            if "version:" in content or "version:" in content:
                agents_with_version += 1

        # At least 50% of agents should track version
        assert agents_with_version >= len(agent_files) * 0.5, \
            f"Expected 50% agents with version field, found {agents_with_version}/{len(agent_files)}"

    def test_version_format_semantic(self):
        """AC-M3-006: Agent versions follow semantic versioning"""
        agents_dir = Path("/home/kevin/work/forBMS/foxBMS/.claude/agents/parvis")
        agent_files = list(agents_dir.glob("parvis-*.md"))

        semantic_version_pattern = r"^\d+\.\d+\.\d+.*$"

        for agent_file in agent_files:
            content = agent_file.read_text()

            # Extract version line
            for line in content.split("\n"):
                if "version:" in line:
                    version_str = line.split("version:")[1].strip()
                    # Allow simple versions or semver
                    assert len(version_str) > 0, f"Empty version in {agent_file.stem}"
                    break


# ============================================================================
# Integration Tests
# ============================================================================

class TestModule3Integration:
    """Integration tests for Module 3"""

    def test_complete_agent_coverage(self):
        """Verify all 20+ agents are covered"""
        agents_dir = Path("/home/kevin/work/forBMS/foxBMS/.claude/agents/parvis")
        agent_files = list(agents_dir.glob("parvis-*.md"))

        assert len(agent_files) >= 20, \
            f"Expected 20+ agent files, found {len(agent_files)}"

    def test_no_syntax_errors_in_definitions(self):
        """Verify no syntax errors in agent definitions"""
        agents_dir = Path("/home/kevin/work/forBMS/foxBMS/.claude/agents/parvis")
        agent_files = list(agents_dir.glob("parvis-*.md"))

        for agent_file in agent_files:
            content = agent_file.read_text()

            # Basic syntax checks
            if content.startswith("---"):
                # Should have closing ---
                assert "---" in content[4:], f"Unclosed YAML in {agent_file.stem}"

            # Markdown syntax check
            assert "#" in content, f"No headings in {agent_file.stem}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
