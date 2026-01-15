# Deploy FPL Assistant to AWS Bedrock AgentCore

This folder contains everything you need to deploy your FPL Assistant to AWS Bedrock AgentCore.

**The `fpl-agentcore/` folder is pre-configured and ready to deploy** - all agent files are already in place. Just install the toolkit and deploy!

## 📁 Files in This Folder

- `fpl-agentcore/` - Pre-configured AgentCore project ready to deploy
  - `src/main.py` - AgentCore wrapper for your Strands agent
  - `src/agent.py` - FPL Strands agent with all tools
  - `src/fpl_client.py` - FPL API client
  - `src/tools/` - All FPL analysis tools
  - `pyproject.toml` - Python dependencies
- `agentcore_app.py` - Reference AgentCore wrapper (already copied to fpl-agentcore/)
- `agentcore_requirements.txt` - Reference dependencies (for manual setup)
- `agentcore.yaml` - Configuration template (optional)
- `README.md` - This file

## What is AgentCore?

AWS Bedrock AgentCore is a **fully managed platform** that handles:
- ✅ Serverless runtime (no Lambda management needed)
- ✅ Built-in memory across sessions
- ✅ API Gateway automatically
- ✅ Authentication & security
- ✅ Observability & tracing
- ✅ Fast cold starts & auto-scaling

You just deploy your agent code - AgentCore handles everything else!

## Prerequisites

1. **AWS Account** with Bedrock access
2. **AWS CLI** configured with credentials
3. **Python 3.11+**
4. **Bedrock Model Access** enabled for Claude 3.5 Sonnet
5. **uv** package manager: `curl -LsSf https://astral.sh/uv/install.sh | sh`

## Quick Deploy (3 Steps)

### Step 1: Install AgentCore Toolkit

```bash
pip install bedrock-agentcore-starter-toolkit
```

Verify:
```bash
agentcore --version
```

### Step 2: Install uv Package Manager

AgentCore requires `uv` for cross-platform Python compilation:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env  # Add uv to PATH
```

### Step 3: Deploy to AWS

The `fpl-agentcore/` folder is already pre-configured with all necessary files:

```bash
cd agentcore/fpl-agentcore

# Deploy!
agentcore deploy
```

The toolkit will:
- Package your agent code and dependencies (50MB)
- Upload to S3
- Create serverless infrastructure
- Set up IAM roles and permissions
- Configure CloudWatch logging
- Deploy to production endpoint

Takes ~2-3 minutes.

### Test Your Agent

```bash
agentcore invoke '{"prompt": "Search for Mohamed Salah"}'

# Check status
agentcore status

# View logs
agentcore invoke '{"prompt": "Who should I captain?"}'
```

**That's it!** No Terraform, no Lambda configs, no manual setup.

## Enable Memory (Optional but Recommended)

AgentCore Memory allows your agent to remember conversations and user preferences:

```bash
# Create memory resource
agentcore memory create fplassistant_memory \
  --description "FPL Assistant conversation and user preferences" \
  --event-expiry-days 90 \
  --wait

# Update config to use memory
# Edit .bedrock_agentcore.yaml and change:
# memory:
#   mode: NO_MEMORY  → mode: STM_AND_LTM
#   memory_id: null  → memory_id: <your-memory-id>

# Redeploy
agentcore deploy
```

With memory enabled:
- **Short-term (STM)**: Conversation history within sessions
- **Long-term (LTM)**: User preferences across sessions (e.g., FPL team ID)

## How It Works

Your `agentcore_app.py` wraps the Strands agent:

```python
from bedrock_agentcore import BedrockAgentCoreApp
from agent import create_fpl_agent

app = BedrockAgentCoreApp()
fpl_agent = create_fpl_agent()

@app.entrypoint()
def handler(request):
    # AgentCore provides:
    # - request.message: User input
    # - request.memory: Conversation history
    # - request.session_id: Session tracking

    response = fpl_agent(request.message)
    return response
```

AgentCore automatically:
- Stores conversation history in memory
- Isolates sessions
- Handles authentication
- Manages scaling
- Provides observability

## Memory Management

AgentCore Memory is **built-in** and automatic:

```python
@app.entrypoint()
def handler(request):
    # Get previous conversation context
    history = request.memory.get_messages(limit=10)

    # Your agent processes the message
    response = fpl_agent(request.message)

    # Memory is automatically saved
    # No DynamoDB tables to manage!

    return response
```

## Configuration

Create `agentcore.yaml` for custom settings:

```yaml
name: fpl-assistant
runtime:
  memory: 1024  # MB
  timeout: 120  # seconds

memory:
  enabled: true
  retention_days: 30

observability:
  tracing: true
  logs: true
```

## Common Commands

```bash
# Deploy
agentcore deploy --entry-point agentcore_app:app

# Test invoke
agentcore invoke --message "Who should I captain?"

# View logs
agentcore logs --tail

# Get info
agentcore info

# Update deployment
agentcore deploy  # Redeploy with changes

# Delete
agentcore delete
```

## Environment Variables

AgentCore passes environment variables automatically:

```bash
# Set via CLI
agentcore deploy --env MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0

# Or in agentcore.yaml
runtime:
  environment:
    MODEL: anthropic.claude-3-5-sonnet-20241022-v2:0
    FPL_TEAM_ID: "123456"
```

## Migrate Existing Bedrock Agent

If you have an old-style Bedrock Agent:

```bash
agentcore import-agent --agent-id YOUR_AGENT_ID
```

## Local Testing

Test locally before deploying:

```bash
# Run the app locally
python agentcore_app.py

# Or use AgentCore local simulator
agentcore local
```

## Monitoring

View your agent in AWS Console:

```bash
agentcore console
```

Or use CLI:

```bash
# View logs
agentcore logs

# View metrics
agentcore metrics

# View traces
agentcore traces
```

## Cost Estimate

AgentCore charges for:
- **Runtime**: Similar to Lambda pricing
- **Memory**: Small storage cost
- **Model calls**: Standard Bedrock pricing

**Typical monthly cost:**
- Light use (10 queries/day): ~$10-20/month
- Medium use (50 queries/day): ~$50-80/month

No charges for:
- Gateway
- Authentication
- Observability infrastructure

## Comparison

| Feature | Manual Lambda + Terraform | AgentCore Toolkit |
|---------|---------------------------|-------------------|
| Setup | Hours of config | 5 minutes |
| Memory | Build DynamoDB tables | Built-in |
| Gateway | Configure API Gateway | Automatic |
| Auth | Set up Cognito | Built-in |
| Monitoring | Configure CloudWatch | Automatic |
| Updates | Redeploy infrastructure | `agentcore deploy` |
| Cost | Infrastructure costs | Pay for usage only |

## Troubleshooting

### Error: "agentcore: command not found"

```bash
pip install --upgrade bedrock-agentcore-starter-toolkit
```

### Error: "AWS credentials not configured"

```bash
aws configure
# Or set environment variables
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
```

### Error: "Bedrock model access denied"

Enable model access in AWS Console:
1. Go to Bedrock Console
2. Model access → Enable Claude 3.5 Sonnet

### Deployment fails

```bash
# Check logs
agentcore logs --tail

# Validate config
agentcore validate

# Retry with verbose output
agentcore deploy --verbose
```

## Cleanup / Destroy Resources

To remove all AWS resources and avoid charges:

```bash
# From the fpl-agentcore/ directory
cd agentcore/fpl-agentcore

# Destroy everything (agent, memory, IAM roles, S3)
agentcore destroy --force

# Also delete the S3 bucket if empty (optional)
aws s3 rb s3://bedrock-agentcore-codebuild-sources-<account-id>-<region>
```

**Note**: The local `fpl-agentcore/` folder is kept for future deployments. Only AWS resources are deleted to avoid charges.

This removes from AWS:
- ✓ AgentCore runtime
- ✓ Memory resources
- ✓ IAM roles and policies
- ✓ S3 deployment artifacts
- ✓ CloudWatch logs

**Cost: $0 after cleanup!** Local files remain for next deployment.

## Next Steps

1. **Custom tools**: Add more FPL tools to your agent
2. **API integration**: Connect to your frontend
3. **Multi-user**: Use session IDs for user isolation
4. **Knowledge base**: Add RAG with AgentCore Knowledge
5. **Multi-agent**: Deploy multiple specialized agents

## Support

- **Toolkit**: https://github.com/aws/bedrock-agentcore-starter-toolkit
- **SDK**: https://github.com/aws/bedrock-agentcore-sdk-python
- **AWS Docs**: https://docs.aws.amazon.com/bedrock/agentcore/

---

**Zero infrastructure management. Just deploy and scale! 🚀**
