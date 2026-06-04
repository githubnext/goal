import importlib.util
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


if __name__ == "__main__":
    unittest.main()
