"""Tests for workflow card Pydantic models.

Tests model creation, validation, and serialization with Palmer's example data.
"""

import pytest
from backend_app.models.workflow_card_models import (
    WorkflowDetail,
    WorkflowCard, 
    WorkflowCardsOutput
)


def test_workflow_detail_creation():
    """Test creating a WorkflowDetail with Palmer's data."""
    detail = WorkflowDetail(
        type="tool",
        content="Cursor",
        source_interval=(100, 150)
    )
    
    assert detail.type == "tool"
    assert detail.content == "Cursor"
    assert detail.source_interval == (100, 150)


def test_workflow_card_creation():
    """Test creating a WorkflowCard with Palmer's planning data."""
    planning_card = WorkflowCard(
        summary="Plans outside the IDE. Co-plans in Grok, then asks it to summarize the conversation.",
        tools=[
            WorkflowDetail(type="tool", content="Grok"),
            WorkflowDetail(type="tool", content="Perplexity")
        ],
        approaches=[
            WorkflowDetail(type="approach", content="Start with a written overview/spec before coding")
        ],
        quotes=[
            WorkflowDetail(
                type="quote", 
                content="Before you start your project, you should have a document that clearly outlines what you're building.",
                source_interval=(478, 632)
            )
        ]
    )
    
    assert "Plans outside the IDE" in planning_card.summary
    assert len(planning_card.tools) == 2
    assert len(planning_card.approaches) == 1
    assert len(planning_card.quotes) == 1
    assert planning_card.tools[0].content == "Grok"


def test_workflow_cards_output_creation():
    """Test creating complete WorkflowCardsOutput with minimal data."""
    empty_card = WorkflowCard(summary="Test summary")
    
    output = WorkflowCardsOutput(
        interview_id="test_palmer",
        planning_scoping=empty_card,
        context_management=empty_card,
        codegen_loop=empty_card,
        verification_safeguards=empty_card,
        iteration_style=empty_card,
        deployment_delivery=empty_card
    )
    
    assert output.interview_id == "test_palmer"
    assert output.planning_scoping.summary == "Test summary"
    assert len(output.context_management.tools) == 0


def test_json_serialization():
    """Test that models can be serialized to/from JSON."""
    detail = WorkflowDetail(type="tool", content="Cursor")
    card = WorkflowCard(summary="Test", tools=[detail])
    
    # Test serialization to dict/JSON
    card_dict = card.model_dump()
    assert card_dict["summary"] == "Test"
    assert card_dict["tools"][0]["content"] == "Cursor"
    
    # Test deserialization from dict
    card_from_dict = WorkflowCard.model_validate(card_dict)
    assert card_from_dict.summary == "Test"
    assert card_from_dict.tools[0].content == "Cursor"