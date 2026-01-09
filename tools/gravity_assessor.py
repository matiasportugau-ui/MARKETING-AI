import json
import os
import sys

# CONFIG
OUTPUT_DIR = "../outputs"
CONTEXT_FILE = "context_snapshot.json"
PLAN_FILE = "execution_plan_draft.json"  # Hypothetical input from the Agent

RISK_THRESHOLDS = {
    "roas_floor": 2.0,
    "cpa_ceiling": 15.0,  # Example
    "budget_increase_cap": 0.20,  # 20% max increase
}


def load_json(filepath):
    path = os.path.join(OUTPUT_DIR, filepath)
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)


def assess_risk(plan, context):
    scorecard = {"status": "GREEN", "flags": [], "confidence_score": 100}

    # Example Logic: Check for Budget Increases > 20%
    if "budget_changes" in plan:
        for change in plan["budget_changes"]:
            if change["percentage"] > RISK_THRESHOLDS["budget_increase_cap"]:
                scorecard["flags"].append(
                    f"High Budget Increase: {change['percentage']*100}% on {change['campaign']}"
                )
                scorecard["status"] = "YELLOW"
                scorecard["confidence_score"] -= 20

    # Example Logic: Check if recent performance allows scaling
    # (Requires context)

    return scorecard


def main():
    print("Gravity Assessor: evaluating Plan against Protocols...")

    context = load_json(CONTEXT_FILE)
    plan = load_json(PLAN_FILE)  # This would typically be passed by the Agent

    if not plan:
        print(f"No {PLAN_FILE} found to assess. Generating template...")
        # Create a dummy plan for the user to fill or the Agent to write to
        dummy_plan = {"execution_plan": {"status": "draft", "budget_changes": []}}
        with open(os.path.join(OUTPUT_DIR, PLAN_FILE), "w") as f:
            json.dump(dummy_plan, f, indent=2)
        print("Template created. Agent should write to this file.")
        return

    result = assess_risk(plan, context)

    print(f"\nASSESSMENT RESULT: {result['status']}")
    print(f"Confidence: {result['confidence_score']}/100")
    for flag in result["flags"]:
        print(f"- WARNING: {flag}")


if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    main()
