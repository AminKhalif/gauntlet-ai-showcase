"""Test all 6 workflow categories are working.

Tests that all workflow examples load and the complete extraction works.
"""

import pytest
import os
from dotenv import load_dotenv
from backend_app.services.ai_workflow_examples import get_examples_for_card_type
from backend_app.services.langextract_workflow_extractor import extract_complete_workflow_cards

load_dotenv()


def test_all_example_categories_load():
    """Test that all 6 workflow categories have examples."""
    categories = [
        "planning_scoping",
        "context_management", 
        "codegen_loop",
        "verification_safeguards",
        "iteration_style",
        "deployment_delivery"
    ]
    
    for category in categories:
        examples = get_examples_for_card_type(category)
        assert len(examples) > 0, f"No examples found for {category}"
        assert len(examples[0].extractions) > 0, f"No extractions in {category} examples"
        print(f"✅ {category}: {len(examples)} examples, {len(examples[0].extractions)} extractions")


# Simple test transcript for all categories
FULL_TEST_TRANSCRIPT = """
[04:49 - 07:47] Interviewer (A):
So it's a step by step, essentially prompt guide where I've laid out kind of how many is this 12ish steps that you should go through to get the entire, what I consider like the scaffolding put together for your project. So we've got the project overview, which everyone should probably start with before they're writing anything.

[35:25 - 37:33] Interviewer (A):
So if I'm doing anything that's like my own idea, I'll typically dump it into Grok. I've been using Perplexity just because it's quick and simple for just like answering basic questions.

[38:04 - 50:24] Interviewer (A):
So reference a file if you want it just used for like a single message, right? However, if you want this persisted through the entire chat, you should add it up here.

[50:29 - 51:45] Interviewer (A):
Yeah, so I keep chats scoped to tasks or features. If your chats are covering more than one feature, just make a new one. Always.

[56:59 - 57:06] Interviewer (A):
If I've gone through several times where it's trying to use Yarn for this or Yarn for that, I'll say, hey, we're using npm. Create a document that explains what we're using and why we're using it.

[23:33 - 31:05] Interviewer (A):
I want a working product through every phase of my project. Each one builds on itself. I want a working product through every phase. So the thing actually works all the way through delivery.
"""


@pytest.mark.skipif(not os.getenv("LANGEXTRACT_API_KEY"), reason="API key not configured")
def test_complete_workflow_extraction():
    """Test extracting all 6 workflow categories."""
    result = extract_complete_workflow_cards(FULL_TEST_TRANSCRIPT, "complete_test")
    
    # Verify all categories are present
    assert result.interview_id == "complete_test"
    assert len(result.planning_scoping.summary) > 10
    assert len(result.context_management.summary) > 10
    assert len(result.codegen_loop.summary) > 10
    assert len(result.verification_safeguards.summary) > 10
    assert len(result.iteration_style.summary) > 10
    assert len(result.deployment_delivery.summary) > 10
    
    # Check none are placeholder messages
    for card_name, card in result.get_all_cards().items():
        assert "pending" not in card.summary.lower(), f"{card_name} still has placeholder summary"
        assert "implementation" not in card.summary.lower(), f"{card_name} still has placeholder summary"
    
    print("🎉 ALL 6 WORKFLOW CATEGORIES SUCCESSFULLY EXTRACTED!")
    print(f"Planning: {result.planning_scoping.summary[:60]}...")
    print(f"Context: {result.context_management.summary[:60]}...")
    print(f"Codegen: {result.codegen_loop.summary[:60]}...")
    print(f"Verification: {result.verification_safeguards.summary[:60]}...")
    print(f"Iteration: {result.iteration_style.summary[:60]}...")
    print(f"Delivery: {result.deployment_delivery.summary[:60]}...")