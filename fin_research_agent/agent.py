from .observability import init_tracing
init_tracing()

import asyncio
####from google.adk.runners import InMemoryRunner
from google.adk.agents import SequentialAgent
from .subagents.planner import planner_agent
from .subagents.writer import writer_agent
from .subagents.verifier import verifier_agent

root_agent = SequentialAgent(    
    name='FinResearchPipeline',
    description="A multi-agent pipeline for strategic financial research and audit.",
    sub_agents=[
        planner_agent,
        writer_agent,
        verifier_agent
    ],
)

