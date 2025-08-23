"""Tests for LangExtract workflow extraction service.

Tests the complete workflow extraction pipeline with real transcript data.
"""

import pytest
import os
from dotenv import load_dotenv
from backend_app.services.langextract_workflow_extractor import (
    extract_single_workflow_card,
    extract_complete_workflow_cards
)
from backend_app.models.workflow_card_models import WorkflowCard, WorkflowCardsOutput

load_dotenv()

# Sample transcript for testing
TEST_TRANSCRIPT = """
[04:49 - 07:47] Interviewer (A):
So it's a step by step, essentially prompt guide where I've laid out kind of how many is this 12ish steps that you should go through to get the entire, what I consider like the scaffolding put together for your project. So we've got the project overview, which everyone should probably start with before they're writing anything.

[35:25 - 37:33] Interviewer (A):
So if I'm doing anything that's like my own idea, I'll typically dump it into Grok. I've been using Perplexity just because it's quick and simple for just like answering basic questions.

[38:04 - 50:24] Interviewer (A):
So reference a file if you want it just used for like a single message, right? However, if you want this persisted through the entire chat, you should add it up here.
"""


@pytest.mark.skipif(not os.getenv("LANGEXTRACT_API_KEY"), reason="API key not configured")
def test_extract_single_workflow_card():
    """Test extracting one workflow card category."""
    card = extract_single_workflow_card(TEST_TRANSCRIPT, "planning_scoping")
    
    assert isinstance(card, WorkflowCard)
    assert len(card.summary) > 10
    
    # Should find some planning-related information
    total_details = len(card.tools) + len(card.approaches) + len(card.rules) + len(card.quotes) + len(card.artifacts)
    assert total_details > 0
    
    print(f"✅ Planning card extracted with {total_details} details")
    print(f"Summary: {card.summary}")


@pytest.mark.skipif(not os.getenv("LANGEXTRACT_API_KEY"), reason="API key not configured") 
def test_extract_complete_workflow_cards():
    """Test extracting all workflow cards from transcript."""
    result = extract_complete_workflow_cards(TEST_TRANSCRIPT, "test_interview")
    
    assert isinstance(result, WorkflowCardsOutput)
    assert result.interview_id == "test_interview"
    
    # Check implemented categories have content
    assert len(result.planning_scoping.summary) > 10
    assert len(result.context_management.summary) > 10
    assert len(result.codegen_loop.summary) > 10
    
    # Check placeholder categories
    assert "pending" in result.verification_safeguards.summary.lower()
    
    print(f"✅ Complete workflow extraction successful")
    print(f"Planning summary: {result.planning_scoping.summary}")
    print(f"Context summary: {result.context_management.summary}")


def test_workflow_card_structure():
    """Test WorkflowCard structure without API calls."""
    from backend_app.services.langextract_workflow_extractor import convert_extractions_to_card
    
    # Mock extraction objects
    class MockExtraction:
        def __init__(self, extraction_class, extraction_text):
            self.extraction_class = extraction_class
            self.extraction_text = extraction_text
            self.char_interval = None
    
    mock_extractions = [
        MockExtraction("tool", "Cursor IDE"),
        MockExtraction("approach", "Start with project overview"),
        MockExtraction("rule", "Keep files under 500 lines")
    ]
    
    card = convert_extractions_to_card(mock_extractions, "planning_scoping")
    
    assert len(card.tools) == 1
    assert len(card.approaches) == 1  
    assert len(card.rules) == 1
    assert card.tools[0].content == "Cursor IDE"
    assert "planning" in card.summary.lower() or "approach" in card.summary.lower()
    
    print("✅ Card structure validation passed")