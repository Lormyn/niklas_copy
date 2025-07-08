GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT="syb-production-experimentation"
GOOGLE_CLOUD_LOCATION="us-central1"
STAGING_BUCKET="gs://audio_expert_staging_bucket"

# Set the path to your agent code directory
export AGENT_PATH="./audio_expert_agent" # Assuming capital_agent is in the current directory

# Set a name for your Cloud Run service (optional)
export SERVICE_NAME="audio-expert"

# Set an application name (optional)
export APP_NAME="audio_expert_agent"

export GOOGLE_APPLICATION_CREDENTIALS="/Users/niklasnorinder/Documents/audio-expert-adk/syb-production-experimentation-02d16255afe0-1.json"

adk deploy cloud_run \
--project=$GOOGLE_CLOUD_PROJECT \
--region=$GOOGLE_CLOUD_LOCATION \
--service_name=$SERVICE_NAME \
--app_name=$APP_NAME \
--with_ui \
$AGENT_PATH