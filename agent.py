import vertexai
import os
from dotenv import load_dotenv
from pathlib import Path

root_dir = Path(__file__).parent
dotenv_path = root_dir / ".env"
load_dotenv(dotenv_path=dotenv_path)

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION")
STAGING_BUCKET = os.environ.get("STAGING_BUCKET")
HARDWARE_RAG = os.environ.get("HARDWARE_RAG")
CASE_STUDY_RAG = os.environ.get("CASE_STUDY_RAG")

if not all([PROJECT_ID, LOCATION, STAGING_BUCKET]):
    raise EnvironmentError("Missing one or more required environment variables: GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION, STAGING_BUCKET")

vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

from google.adk.agents import Agent
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag
from prompt_templates_review import root_prompt, case_study_prompt, wired_prompt, wireless_prompt

hardware_rag = VertexAiRagRetrieval(
    name='retrieve_hardware_rag_documentation',
    description=(
        'Use this tool to retrieve documentation and reference materials for the question from the RAG corpus,'
    ),
    rag_resources=[
        rag.RagResource(
            rag_corpus=HARDWARE_RAG
        )
    ],
    similarity_top_k=10,
    vector_distance_threshold=0.6,
)

case_study_rag = VertexAiRagRetrieval(
    name='retrieve_case_study_rag_documentation',
    description=(
        'Use this tool to retrieve documentation and reference materials for the question from the RAG corpus,'
    ),
    rag_resources=[
        rag.RagResource(
            rag_corpus=CASE_STUDY_RAG
        )
    ],
    similarity_top_k=10,
    vector_distance_threshold=0.6,
)

wireless_agent = Agent(
    name="wireless_agent",
    model="gemini-2.5-flash",
    description="Agent that is an expert on wireless solutions",
    instruction=wireless_prompt,
    tools=[hardware_rag]
)

wired_agent = Agent(
    name="wired_agent",
    model="gemini-2.5-flash",
    description="Agent that is an expert on wired solutions",
    instruction=wired_prompt,
    tools=[hardware_rag]
)

case_study_agent = Agent(
    name="case_study_agent",
    model="gemini-2.5-flash",
    description="Agent that is an expert on hardware case studies",
    instruction=case_study_prompt,
    tools=[case_study_rag],
)

root_agent = Agent(
    name="audio_expert_agent",
    model="gemini-2.5-flash",
    description="Agent to answer hardware leads",
    instruction=root_prompt,
    sub_agents=[wireless_agent, wired_agent, case_study_agent],
)