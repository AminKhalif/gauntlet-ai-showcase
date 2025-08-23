"""Pydantic models for workflow card extraction.

Takes: Raw extraction data from LangExtract  
Outputs: Clean WorkflowCard objects for any interview transcript
Used by: langextract_workflow_extractor.py for data validation

Structure follows the 6-card workflow format defined in project-overview.md
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class WorkflowDetail(BaseModel):
    """Single piece of workflow information with optional source grounding."""
    type: str = Field(description="tool, approach, rule, quote, or artifact")
    content: str = Field(description="The actual text content")
    source_interval: Optional[tuple[int, int]] = Field(
        default=None, 
        description="Character positions in transcript (start, end)"
    )


class WorkflowCard(BaseModel):
    """One of the 6 workflow categories containing categorized details."""
    summary: str = Field(description="2-sentence summary")
    approaches: List[WorkflowDetail] = Field(default_factory=list)
    tools: List[WorkflowDetail] = Field(default_factory=list) 
    rules: List[WorkflowDetail] = Field(default_factory=list)
    quotes: List[WorkflowDetail] = Field(default_factory=list)
    artifacts: List[WorkflowDetail] = Field(default_factory=list)


class WorkflowCardsOutput(BaseModel):
    """Complete set of 6 workflow cards for one interview."""
    interview_id: str
    planning_scoping: WorkflowCard
    context_management: WorkflowCard
    codegen_loop: WorkflowCard
    verification_safeguards: WorkflowCard
    iteration_style: WorkflowCard
    deployment_delivery: WorkflowCard