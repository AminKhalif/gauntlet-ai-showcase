"""LangExtract proof of concept test.

Tests basic LangExtract functionality with a small transcript snippet.
This test will show you what API key setup is needed.
"""

import pytest
import os
from dotenv import load_dotenv
from backend_app.models.workflow_card_models import WorkflowDetail, WorkflowCard

# Load environment variables from .env file
load_dotenv()

# Sample transcript snippet from Palmer (just planning section)
SAMPLE_TRANSCRIPT = """
[04:49 - 07:47] Interviewer (A):
So this is designed for like starting from complete scratch. You have only an idea of what you want to build in your project. So it's a step by step, essentially prompt guide where I've laid out kind of how many is this 12ish steps that you should go through to get the entire, what I consider like the scaffolding put together for your project. So we've got the project overview, which everyone should probably start with before they're writing anything. It's just your project's purpose, goals, whatever, you know, all the loose features that you're going to have. Then from there you pop into the user flow, which kind of defines the journey through the application.

[07:58 - 10:52] Interviewer (A):
Yeah, so I have this docs folder. I name it with an underscore just so it stays at the top of the hierarchy. Before you start your project, you should have a document that clearly outlines what you're building. Maybe very loosely, like how you want to build it.
"""


def test_langextract_api_key_check():
    """Check if LANGEXTRACT_API_KEY is set up."""
    api_key = os.getenv("LANGEXTRACT_API_KEY")
    
    if not api_key:
        pytest.skip("LANGEXTRACT_API_KEY not set. Please set environment variable to run this test.")
    
    assert len(api_key) > 10, "API key should be longer than 10 characters"


@pytest.mark.skipif(not os.getenv("LANGEXTRACT_API_KEY"), reason="API key not configured")
def test_langextract_basic_extraction():
    """Test basic LangExtract functionality with planning & scoping extraction."""
    
    try:
        import langextract as lx
    except ImportError:
        pytest.fail("langextract not installed properly")
    
    # Simple prompt to extract just planning tools
    prompt = """
    Extract tools and approaches mentioned for project planning and setup.
    Look for:
    - Tools used (software, platforms)
    - Approaches (methodologies, steps)
    
    Format each extraction with:
    - extraction_class: "tool" or "approach"  
    - extraction_text: exact quote from text
    """
    
    # Basic extraction with no examples (simplest test)
    try:
        results = lx.extract(
            text_or_documents=SAMPLE_TRANSCRIPT,
            prompt_description=prompt,
            model_id="gemini-2.0-flash-thinking-exp",  # Fast model for testing
            examples=[]  # No examples for basic test
        )
        
        # Verify we got some results
        assert len(results) > 0, "Should extract at least one item"
        
        # Check result structure
        first_result = results[0]
        assert hasattr(first_result, 'extraction_class')
        assert hasattr(first_result, 'extraction_text')
        
        print(f"✅ LangExtract working! Found {len(results)} extractions")
        for result in results[:3]:  # Show first 3
            print(f"  - {result.extraction_class}: {result.extraction_text[:50]}...")
            
    except Exception as e:
        pytest.fail(f"LangExtract failed: {e}")


@pytest.mark.skipif(not os.getenv("LANGEXTRACT_API_KEY"), reason="API key not configured") 
def test_extraction_to_pydantic_conversion():
    """Test converting LangExtract results to our Pydantic models."""
    
    # Mock LangExtract result (what we expect to get)
    class MockExtraction:
        def __init__(self, extraction_class, extraction_text):
            self.extraction_class = extraction_class
            self.extraction_text = extraction_text
    
    mock_results = [
        MockExtraction("tool", "docs folder with underscore"),
        MockExtraction("approach", "start with project overview before writing anything"),
        MockExtraction("approach", "12-step setup guide for scaffolding")
    ]
    
    # Convert to our Pydantic models
    workflow_details = []
    for result in mock_results:
        detail = WorkflowDetail(
            type=result.extraction_class,
            content=result.extraction_text
        )
        workflow_details.append(detail)
    
    # Create WorkflowCard
    planning_card = WorkflowCard(
        summary="Uses structured approach with docs folder and 12-step setup guide.",
        tools=[d for d in workflow_details if d.type == "tool"],
        approaches=[d for d in workflow_details if d.type == "approach"]
    )
    
    # Verify conversion worked
    assert len(planning_card.tools) == 1
    assert len(planning_card.approaches) == 2
    assert "docs folder" in planning_card.tools[0].content
    assert "12-step" in planning_card.approaches[1].content
    
    print("✅ Pydantic conversion working!")
    print(f"  - Tools: {len(planning_card.tools)}")
    print(f"  - Approaches: {len(planning_card.approaches)}")


@pytest.mark.skipif(not os.getenv("LANGEXTRACT_API_KEY"), reason="API key not configured")
def test_langextract_with_real_examples():
    """Test LangExtract with our carefully crafted examples using Gemini 2.5 Pro."""
    
    try:
        import langextract as lx
        from backend_app.services.ai_workflow_examples import get_examples_for_card_type
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")
    
    # Test with Planning & Scoping examples
    prompt = """
    Extract AI workflow information from interview transcripts.
    Look for:
    - Tools used (software, platforms, AI models)
    - Approaches (methodologies, techniques, steps)  
    - Rules (principles, guidelines, habits)
    - Artifacts (files, documents, deliverables)
    
    Format each extraction with appropriate extraction_class and exact extraction_text.
    """
    
    try:
        # Get our high-quality examples
        examples = get_examples_for_card_type("planning_scoping")
        print(f"Using {len(examples)} training examples")
        
        # Test extraction with examples using Gemini 2.5 Pro
        results = lx.extract(
            text_or_documents=SAMPLE_TRANSCRIPT,
            prompt_description=prompt,
            examples=examples,
            model_id="gemini-2.5-pro"
        )
        
        # Verify we got results (results is an AnnotatedDocument with extractions)
        extractions = list(results.extractions)
        assert len(extractions) > 0, "Should extract at least one item with examples"
        
        print(f"✅ LangExtract working with Gemini 2.5 Pro! Found {len(extractions)} extractions")
        for extraction in extractions[:5]:  # Show first 5
            print(f"  - {extraction.extraction_class}: {extraction.extraction_text[:60]}...")
            
    except Exception as e:
        pytest.fail(f"LangExtract with examples failed: {e}")


if __name__ == "__main__":
    # Instructions for running manually
    print("To run these tests:")
    print("1. Set LANGEXTRACT_API_KEY environment variable") 
    print("2. Run: uv run pytest tests/services/test_langextract_proof_of_concept.py -v -s")
    print("\nWithout API key, only conversion test will run.")