"""Extracts AI workflow cards from interview transcripts using LangExtract.

Takes: Full interview transcript text + interview ID
Outputs: Complete WorkflowCardsOutput with structured workflow information
Used by: Integration pipeline for processing interview data into website format
"""

import langextract as lx
from typing import List, Any
from backend_app.models.workflow_card_models import (
    WorkflowDetail,
    WorkflowCard,
    WorkflowCardsOutput
)
from backend_app.services.ai_workflow_examples import get_examples_for_card_type


WORKFLOW_EXTRACTION_PROMPT = """
Extract AI engineering workflow information from this interview transcript.

Look for:
- Tools: Software, platforms, AI models, IDEs
- Approaches: Methodologies, techniques, steps
- Rules: Personal principles, guidelines, habits
- Artifacts: Files, documents, deliverables
- Quotes: Exact verbatim statements

Categories: Planning & Scoping, Context Management, Codegen Loop,
Verification & Safeguards, Iteration Style, Deployment & Delivery

Format: extraction_class, extraction_text, attributes
"""


def extract_single_workflow_card(
    transcript_text: str, 
    card_type: str, 
    model_id: str = "gemini-2.5-pro"
) -> WorkflowCard:
    """Extract one workflow card from transcript using LangExtract.
    
    Args:
        transcript_text: Full interview transcript
        card_type: Workflow category (planning_scoping, context_management, etc.)
        model_id: LLM model for extraction
        
    Returns:
        WorkflowCard with extracted and categorized information
        
    Raises:
        ValueError: If extraction fails or card_type invalid
    """
    examples = get_examples_for_card_type(card_type)
    
    results = lx.extract(
        text_or_documents=transcript_text,
        prompt_description=WORKFLOW_EXTRACTION_PROMPT,
        examples=examples,
        model_id=model_id
    )
    
    extractions = list(results.extractions)
    return convert_extractions_to_card(extractions, card_type)


def convert_extractions_to_card(extractions: List[Any], card_type: str) -> WorkflowCard:
    """Convert LangExtract results to structured WorkflowCard.
    
    Args:
        extractions: List of LangExtract Extraction objects
        card_type: Workflow category name
        
    Returns:
        WorkflowCard with categorized details and summary
    """
    tools, approaches, rules, quotes, artifacts = [], [], [], [], []
    
    for extraction in extractions:
        detail = create_workflow_detail(extraction)
        
        if extraction.extraction_class == "tool":
            tools.append(detail)
        elif extraction.extraction_class == "approach":
            approaches.append(detail)
        elif extraction.extraction_class == "rule":
            rules.append(detail)
        elif extraction.extraction_class == "quote":
            quotes.append(detail)
        elif extraction.extraction_class == "artifact":
            artifacts.append(detail)
    
    summary = generate_card_summary(extractions, card_type)
    
    return WorkflowCard(
        summary=summary,
        tools=tools,
        approaches=approaches,
        rules=rules,
        quotes=quotes,
        artifacts=artifacts
    )


def create_workflow_detail(extraction: Any) -> WorkflowDetail:
    """Create WorkflowDetail from LangExtract extraction.
    
    Args:
        extraction: LangExtract Extraction object
        
    Returns:
        WorkflowDetail with content and optional source grounding
    """
    source_interval = None
    if hasattr(extraction, 'char_interval') and extraction.char_interval:
        source_interval = (
            extraction.char_interval.start_pos,
            extraction.char_interval.end_pos
        )
    
    return WorkflowDetail(
        type=extraction.extraction_class,
        content=extraction.extraction_text,
        source_interval=source_interval
    )


def generate_card_summary(extractions: List[Any], card_type: str) -> str:
    """Generate concise summary for workflow card.
    
    Args:
        extractions: List of LangExtract Extraction objects
        card_type: Workflow category
        
    Returns:
        Two-sentence summary describing the workflow approach
    """
    approaches = [e.extraction_text for e in extractions if e.extraction_class == "approach"]
    tools = [e.extraction_text for e in extractions if e.extraction_class == "tool"]
    
    if card_type == "planning_scoping":
        if tools and approaches:
            return f"Uses {', '.join(tools[:2])} for planning. Follows structured approach with {approaches[0][:50]}..."
        elif approaches:
            return f"Planning methodology: {approaches[0][:60]}. Systematic project setup process."
        return "Structured approach to planning and scoping AI development projects."
    
    elif card_type == "context_management":
        if approaches:
            return f"Context strategy: {approaches[0][:60]}. Organized information management for AI tools."
        return "Systematic approach to managing context and information flow to AI models."
    
    elif card_type == "codegen_loop":
        if approaches:
            return f"Development process: {approaches[0][:60]}. Iterative AI-assisted coding workflow."
        return "Structured approach to AI-assisted code generation and iteration."
    
    elif card_type == "verification_safeguards":
        if approaches:
            return f"Quality assurance: {approaches[0][:60]}. Systematic error prevention and recovery."
        return "Structured approach to code verification and debugging safeguards."
    
    elif card_type == "iteration_style":
        if approaches:
            return f"Development cadence: {approaches[0][:60]}. Incremental improvement methodology."
        return "Systematic approach to iterative development and refinement cycles."
    
    elif card_type == "deployment_delivery":
        if approaches:
            return f"Delivery strategy: {approaches[0][:60]}. Phased deployment methodology."
        return "Structured approach to shipping and delivering software projects."
    
    return f"Systematic methodology for {card_type.replace('_', ' ')} in AI workflows."


def extract_complete_workflow_cards(
    transcript_text: str,
    interview_id: str,
    model_id: str = "gemini-2.5-pro"
) -> WorkflowCardsOutput:
    """Extract all workflow cards from interview transcript.
    
    Args:
        transcript_text: Full interview transcript
        interview_id: Unique identifier for interview
        model_id: LLM model for extraction
        
    Returns:
        WorkflowCardsOutput with all 6 workflow categories
        
    Raises:
        ValueError: If extraction fails for any category
    """
    planning_card = extract_single_workflow_card(transcript_text, "planning_scoping", model_id)
    context_card = extract_single_workflow_card(transcript_text, "context_management", model_id)
    codegen_card = extract_single_workflow_card(transcript_text, "codegen_loop", model_id)
    verification_card = extract_single_workflow_card(transcript_text, "verification_safeguards", model_id)
    iteration_card = extract_single_workflow_card(transcript_text, "iteration_style", model_id)
    delivery_card = extract_single_workflow_card(transcript_text, "deployment_delivery", model_id)
    
    return WorkflowCardsOutput(
        interview_id=interview_id,
        planning_scoping=planning_card,
        context_management=context_card,
        codegen_loop=codegen_card,
        verification_safeguards=verification_card,
        iteration_style=iteration_card,
        deployment_delivery=delivery_card
    )