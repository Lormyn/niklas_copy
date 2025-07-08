import vertexai
from audio_expert_agent.agent import root_agent
from vertexai import agent_engines
from vertexai.preview import reasoning_engines
import os
from dotenv import load_dotenv
load_dotenv()

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION")
STAGING_BUCKET = os.environ.get("STAGING_BUCKET")
STAGING_BUCKET = os.environ.get("STAGING_BUCKET")
HARDWARE_RAG = os.environ.get("HARDWARE_RAG")
GOOGLE_GENAI_USE_VERTEXAI=os.environ["GOOGLE_GENAI_USE_VERTEXAI"]
CASE_STUDY_RAG = os.environ.get("CASE_STUDY_RAG")

print(PROJECT_ID, STAGING_BUCKET, CASE_STUDY_RAG)

vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

def create_app(): 

    app = reasoning_engines.AdkApp(
        agent=root_agent,
        enable_tracing=True
    )

    remote_app = agent_engines.create(
        agent_engine=app,
        display_name="audio_expert_agent",
        requirements=[
            "google-cloud-aiplatform[agent_engines]",
            "cloudpickle==3.0.0",
            "pydantic==2.11.7",
            "python-dotenv",
            "requests",
            "pathlib",
            "protobuf==3.20.3",
        ],
        env_vars={
            "STAGING_BUCKET": STAGING_BUCKET,
            "HARDWARE_RAG": HARDWARE_RAG,
            "CASE_STUDY_RAG": CASE_STUDY_RAG,
        },
        extra_packages=["audio_expert_agent"]
    )


def list_deployments() -> None:
    """Lists all deployments."""
    deployments = agent_engines.list()
    if not deployments:
        print("No deployments found.")
        return
    print("Deployments:")
    for deployment in deployments:
        print(f"- {deployment.resource_name}")

def local():

    app = reasoning_engines.AdkApp(
        agent=root_agent,
        enable_tracing=True,
    )

    session = app.create_session(user_id="u_123")
    session

create_app()