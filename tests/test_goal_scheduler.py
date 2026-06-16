import importlib.util
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEDULER = ROOT / "workflows" / "scripts" / "goal_scheduler.py"

spec = importlib.util.spec_from_file_location("goal_scheduler", SCHEDULER)
goal_scheduler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(goal_scheduler)


class GoalSchedulerTests(unittest.TestCase):
    def test_slugify_issue_title_is_branch_safe(self):
        self.assertEqual(goal_scheduler.slugify_issue_title("Fix checkout retry!", 42), "fix-checkout-retry")
        self.assertEqual(goal_scheduler.branch_for_issue(42, "Fix checkout retry!"), "goal/42-fix-checkout-retry")

    def test_analyze_goal_definition_ready(self):
        body = """
## Goal
Ship checkout retry support.

## Completion Contract
Retry support is merged and old checkout behavior still passes.

## Evidence / Verification
Run `npm test -- checkout` and `npm run lint`; both must exit 0.

## Scope and Constraints
Only touch `src/checkout/**` and `tests/checkout/**`. Do not change public APIs.

## Iteration Policy
Move one coherent checkpoint at a time and verify the narrowest useful test.

## Blocked Stop Condition
If credentials are missing, report the exact command output and required secret.
"""

        analysis = goal_scheduler.analyze_goal_definition(body)

        self.assertEqual(analysis["definition_status"], "ready")
        self.assertEqual(analysis["missing_sections"], [])

    def test_analyze_goal_definition_flags_placeholders(self):
        body = """
## Goal
REPLACE THIS with the desired outcome.

## Completion Contract
TODO
"""

        analysis = goal_scheduler.analyze_goal_definition(body)

        self.assertEqual(analysis["definition_status"], "needs_action")
        self.assertIn("goal", analysis["missing_sections"])
        self.assertIn("evidence", analysis["missing_sections"])

    def test_select_goal_prefers_never_run_then_oldest(self):
        goals = [
            {"number": 1, "title": "Newer", "last_run": "2026-01-02T00:00:00Z"},
            {"number": 2, "title": "Never", "last_run": None},
            {"number": 3, "title": "Older", "last_run": "2026-01-01T00:00:00Z"},
        ]

        selected, deferred, error = goal_scheduler.select_goal(goals)

        self.assertIsNone(error)
        self.assertEqual(selected["number"], 2)
        self.assertEqual({goal["number"] for goal in deferred}, {1, 3})

    def test_select_goal_can_force_issue(self):
        goals = [
            {"number": 1, "title": "First", "last_run": None},
            {"number": 2, "title": "Second", "last_run": None},
        ]

        selected, deferred, error = goal_scheduler.select_goal(goals, forced_issue="#2")

        self.assertIsNone(error)
        self.assertEqual(selected["number"], 2)
        self.assertEqual([goal["number"] for goal in deferred], [1])

    def test_workflow_problem_reports_do_not_create_issues(self):
        for workflow_path in (ROOT / "workflows" / "goal.md", ROOT / ".github" / "workflows" / "goal.md"):
            with self.subTest(workflow_path=workflow_path):
                workflow = workflow_path.read_text(encoding="utf-8")

                self.assertIn("report-failure-as-issue: false", workflow)
                self.assertIn("missing-tool:\n    create-issue: false", workflow)
                self.assertIn("missing-data:\n    create-issue: false", workflow)
                self.assertIn("report-incomplete:\n    create-issue: false", workflow)
                self.assertIn("noop:\n    report-as-issue: false", workflow)
                self.assertIn("use `add_comment` on\n`selected.number`. Do not open a new issue.", workflow)
                self.assertIn("comment on\n  the goal issue instead.", workflow)

        lock = (ROOT / ".github" / "workflows" / "goal.lock.yml").read_text(encoding="utf-8")
        config_match = re.search(r"^\s+(\{\"add_comment\".+})$", lock, flags=re.MULTILINE)
        handler_match = re.search(r'GH_AW_SAFE_OUTPUTS_HANDLER_CONFIG: "(.+)"', lock)
        self.assertIsNotNone(config_match)
        self.assertIsNotNone(handler_match)

        configs = [
            json.loads(config_match.group(1)),
            json.loads(json.loads(f'"{handler_match.group(1)}"')),
        ]
        for config in configs:
            with self.subTest(config=config):
                self.assertIs(config["missing_tool"]["create_issue"], False)
                self.assertIs(config["missing_data"]["create_issue"], False)
                self.assertIs(config["report_incomplete"]["create_issue"], False)
                self.assertIn(config["noop"]["report-as-issue"], (False, "false"))

        expected_false_flags = {
            "GH_AW_NOOP_REPORT_AS_ISSUE",
            "GH_AW_MISSING_TOOL_CREATE_ISSUE",
            "GH_AW_REPORT_INCOMPLETE_CREATE_ISSUE",
            "GH_AW_FAILURE_REPORT_AS_ISSUE",
        }
        present_flags = set()
        for match in re.finditer(r"(GH_AW_[A-Z_]*(?:REPORT_AS_ISSUE|CREATE_ISSUE)): \"([^\"]+)\"", lock):
            present_flags.add(match.group(1))
            self.assertEqual(match.group(2), "false")
        self.assertTrue(expected_false_flags.issubset(present_flags))


if __name__ == "__main__":
    unittest.main()
