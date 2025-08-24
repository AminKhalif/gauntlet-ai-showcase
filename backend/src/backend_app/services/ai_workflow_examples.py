"""Creates high-quality training examples for AI workflow extraction, Langextract requires high quality examples.

Takes: Palmer's transcript snippets + expected workflow outputs
Outputs: langextract.data.ExampleData objects for few-shot learning
Used by: ai_workflow_extractor.py for reliable extraction quality

The quality of these examples determines extraction success.
"""

import langextract as lx
from langextract.data import ExampleData, Extraction


def create_planning_scoping_examples() -> list[ExampleData]:
    """Create training examples for Planning & Scoping workflow extraction."""
    
    # Example 1: Tools and 12-step approach
    example_text_1 = """
[04:49 - 07:47] Interviewer (A):
So it's a step by step, essentially prompt guide where I've laid out kind of how many is this 12ish steps that you should go through to get the entire, what I consider like the scaffolding put together for your project. So we've got the project overview, which everyone should probably start with before they're writing anything.

[35:25 - 37:33] Interviewer (A):
So if I'm doing anything that's like my own idea, I'll typically dump it into Grok. I've been using Perplexity just because it's quick and simple for just like answering basic questions.
"""
    
    expected_extractions_1 = [
        Extraction(
            extraction_class="approach",
            extraction_text="12-step setup guide to get the entire scaffolding put together",
            attributes={"phase": "setup"}
        ),
        Extraction(
            extraction_class="approach", 
            extraction_text="Start with project overview before writing anything",
            attributes={"phase": "planning"}
        ),
        Extraction(
            extraction_class="tool",
            extraction_text="Grok",
            attributes={"purpose": "planning and ideation"}
        ),
        Extraction(
            extraction_class="tool",
            extraction_text="Perplexity", 
            attributes={"purpose": "quick factual questions"}
        )
    ]
    
    # Example 2: Documentation structure
    example_text_2 = """
[07:58 - 10:52] Interviewer (A):
Yeah, so I have this docs folder. I name it with an underscore just so it stays at the top of the hierarchy. Before you start your project, you should have a document that clearly outlines what you're building.
"""
    
    expected_extractions_2 = [
        Extraction(
            extraction_class="artifact",
            extraction_text="docs folder with underscore to stay at top of hierarchy",
            attributes={"type": "organization"}
        ),
        Extraction(
            extraction_class="rule",
            extraction_text="Have a document that clearly outlines what you're building before starting",
            attributes={"timing": "pre_coding"}
        )
    ]
    
    return [
        ExampleData(text=example_text_1, extractions=expected_extractions_1),
        ExampleData(text=example_text_2, extractions=expected_extractions_2)
    ]


def create_context_management_examples() -> list[ExampleData]:
    """Create training examples for Context Management workflow extraction."""
    
    example_text = """
[38:04 - 50:24] Interviewer (A):
So reference a file if you want it just used for like a single message, right? However, if you want this persisted through the entire chat, you should add it up here. Files that are commonly used for this, I would say from the new project setup would be the tech stack, because oftentimes anytime you're making a change to your code base, it's probably going to touch some sort of package or library.
"""
    
    expected_extractions = [
        Extraction(
            extraction_class="rule",
            extraction_text="Reference files for single message, attach files for persistent context",
            attributes={"technique": "file_management"}
        ),
        Extraction(
            extraction_class="approach",
            extraction_text="Keep tech stack file in permanent context for most changes",
            attributes={"context_type": "persistent"}
        )
    ]
    
    return [ExampleData(text=example_text, extractions=expected_extractions)]


def create_codegen_loop_examples() -> list[ExampleData]:
    """Create training examples for Codegen Loop workflow extraction."""
    
    example_text = """
[50:29 - 51:45] Interviewer (A):
Yeah, so I keep chats scoped to tasks or features. If your chats are covering more than one feature, just make a new one. Always.

[51:50 - 53:21] Interviewer (A):
Always start with clean context. One essential thing is always say use tools. Use tools to explore the code base, that's what I've found to be the most effective for gathering context.
"""
    
    expected_extractions = [
        Extraction(
            extraction_class="rule",
            extraction_text="Keep chats scoped to single tasks or features",
            attributes={"scope": "chat_management"}
        ),
        Extraction(
            extraction_class="rule",
            extraction_text="Always tell agent to use tools to explore the codebase",
            attributes={"technique": "context_gathering"}
        ),
        Extraction(
            extraction_class="approach",
            extraction_text="Start new chat with clean context for each task",
            attributes={"initialization": "fresh_start"}
        )
    ]
    
    return [ExampleData(text=example_text, extractions=expected_extractions)]


def create_verification_safeguards_examples() -> list[ExampleData]:
    """Create training examples for Verification & Safeguards workflow extraction."""
    
    example_text = """
[56:59 - 57:06] Interviewer (A):
If I've gone through several times where it's trying to use Yarn for this or Yarn for that, I'll say, hey, we're using npm. Create a document that explains what we're using and why we're using it. That way you can provide it to the LLM so it doesn't make the same mistake again. That's like a critical debugging step, in my opinion.

[58:25 - 58:51] Interviewer (A):
But if you make changes to a file in a prompt up here, there'll be like this little restore checkpoint option at the bottom. If you don't reach a resolution, don't keep going down that same chat because you have all these bad examples and bad paths previously. Typically, you're better off just trying to one shot it again from the start. If it tries something that doesn't work, just restore your checkpoint.
"""
    
    expected_extractions = [
        Extraction(
            extraction_class="approach",
            extraction_text="Create a document explaining tools and decisions to prevent AI from repeating mistakes",
            attributes={"prevention": "mistake_avoidance"}
        ),
        Extraction(
            extraction_class="rule", 
            extraction_text="Use restore checkpoint to revert bad debugging paths instead of continuing long chats",
            attributes={"debugging": "error_recovery"}
        ),
        Extraction(
            extraction_class="approach",
            extraction_text="Start fresh debugging session rather than continuing with bad examples in context",
            attributes={"debugging": "clean_context"}
        )
    ]
    
    return [ExampleData(text=example_text, extractions=expected_extractions)]


def create_iteration_style_examples() -> list[ExampleData]:
    """Create training examples for Iteration Style workflow extraction."""
    
    example_text = """
[50:29 - 51:45] Interviewer (A):
Yeah, so I keep chats scoped to tasks or features. If your chats are covering more than one feature, just make a new one. Always. I don't go beyond that unless it's just like really cooking every once in a while.

[51:46 - 53:21] Interviewer (A):
If a chat gets sufficiently long, I don't use the summarize feature super often, just make a new one. I like having it be a two-way street, but typically I recommend splitting it up as much as you can.
"""
    
    expected_extractions = [
        Extraction(
            extraction_class="rule",
            extraction_text="Keep chats scoped to single tasks or features, make new chat if covering multiple",
            attributes={"scope": "task_isolation"}
        ),
        Extraction(
            extraction_class="approach",
            extraction_text="Split work into small increments rather than large changes",
            attributes={"methodology": "incremental"}
        ),
        Extraction(
            extraction_class="rule",
            extraction_text="Make new chat instead of using summarize feature for long conversations",
            attributes={"chat_management": "fresh_context"}
        )
    ]
    
    return [ExampleData(text=example_text, extractions=expected_extractions)]


def create_deployment_delivery_examples() -> list[ExampleData]:
    """Create training examples for Deployment & Delivery workflow extraction."""
    
    example_text = """
[23:33 - 31:05] Interviewer (A):
I want a working product through every phase of my project. Each one builds on itself. I want a working product through every phase. So the thing actually works all the way through delivery. Structure work into setup phase, then like an MVP phase and then like several more like expansion phases on top of that.

[12:52 - 15:54] Interviewer (A):
I made this GitHub CLI example document. It'll create issues, read issues, and even resolve issues. It's almost like having a miniature Devin in your code base.
"""
    
    expected_extractions = [
        Extraction(
            extraction_class="approach",
            extraction_text="Structure work in phases (setup → MVP → expansion) ensuring working product at each stage",
            attributes={"methodology": "phased_delivery"}
        ),
        Extraction(
            extraction_class="rule",
            extraction_text="Maintain working product through every phase all the way through delivery",
            attributes={"principle": "continuous_functionality"}
        ),
        Extraction(
            extraction_class="tool",
            extraction_text="GitHub CLI",
            attributes={"purpose": "issue_management"}
        ),
        Extraction(
            extraction_class="artifact",
            extraction_text="GitHub CLI example document for creating and managing issues",
            attributes={"type": "automation_doc"}
        )
    ]
    
    return [ExampleData(text=example_text, extractions=expected_extractions)]


def get_examples_for_card_type(card_type: str) -> list[ExampleData]:
    """Get training examples for a specific workflow card type."""
    examples_map = {
        "planning_scoping": create_planning_scoping_examples,
        "context_management": create_context_management_examples,
        "codegen_loop": create_codegen_loop_examples,
        "verification_safeguards": create_verification_safeguards_examples,
        "iteration_style": create_iteration_style_examples,
        "deployment_delivery": create_deployment_delivery_examples,
    }
    
    if card_type not in examples_map:
        raise ValueError(f"Unknown card type: {card_type}. Available: {list(examples_map.keys())}")
    
    return examples_map[card_type]()