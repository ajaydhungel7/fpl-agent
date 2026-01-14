# Quick Start: AWS Bedrock Setup (5 Minutes)

This is the fastest way to get your FPL Assistant running with AWS Bedrock.

## Prerequisites
- AWS Account
- Python 3.10+

## Step 1: Enable AWS Bedrock (2 minutes)

1. **Go to Bedrock Console**: https://console.aws.amazon.com/bedrock/
2. **Select Region**: Choose `us-east-1` (Virginia)
3. **Enable Model Access**:
   - Click "Model access" in sidebar
   - Click "Enable specific models"
   - Check ✓ **Claude 3.5 Sonnet**
   - Click "Request model access"
   - Wait for "Access granted" (usually instant)

## Step 2: Create IAM User (2 minutes)

1. **Go to IAM Console**: https://console.aws.amazon.com/iam/
2. **Create User**:
   - Users → Add users
   - Username: `fpl-assistant`
   - Check: "Access key - Programmatic access"
   - Next
3. **Attach Policy**:
   - "Attach existing policies directly"
   - Search and check: ✓ `AmazonBedrockFullAccess`
   - Next → Create user
4. **Save Credentials**:
   - Download CSV or copy:
     - Access key ID (starts with `AKIA`)
     - Secret access key
   - Keep these secure!

## Step 3: Configure FPL Assistant (1 minute)

Run the setup script:

```bash
cd /Users/ajaydhungel/Documents/strands/fpl-assistant
./setup_bedrock.sh
```

Or manually:

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.bedrock .env
nano .env
```

Edit `.env`:

```bash
# Your FPL Team ID (from fantasy.premierleague.com URL)
FPL_TEAM_ID=123456

# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIA...paste_here...
AWS_SECRET_ACCESS_KEY=...paste_here...

# Use Claude 3.5 Sonnet (best performance)
MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
```

Save and exit (Ctrl+X, then Y)

## Step 4: Run! (30 seconds)

```bash
python agent.py
```

You should see:
```
✓ LLM Provider: AWS Bedrock
✓ Team ID configured: 123456
```

Try it:
```
You: Who should I captain this week?
```

## Done! 🎉

Your FPL Assistant is now running on AWS Bedrock.

## Common Issues

**"AccessDeniedException"**
→ IAM user needs `AmazonBedrockFullAccess` policy

**"ValidationException: model identifier invalid"**
→ Request model access in Bedrock console

**"No LLM API key detected"**
→ Check `.env` file exists and has correct AWS credentials

**"ResourceNotFoundException"**
→ Wrong region. Use `us-east-1` which has all models

## What's Next?

Try these commands:
```
You: Show me my current team
You: Find me midfielders under £8m with good form
You: Compare Haaland and Kane as captain options
You: Suggest some differential players
You: Analyze my team's fixtures for the next 5 gameweeks
```

## Cost Estimate

With Claude 3.5 Sonnet on Bedrock:
- ~10 queries/day = $0.50-2/month
- ~50 queries/day = $2-8/month

Monitor in AWS Cost Explorer.

## Support

- Detailed setup: [AWS_BEDROCK_SETUP.md](AWS_BEDROCK_SETUP.md)
- All LLM options: [LLM_SETUP.md](LLM_SETUP.md)
- Full docs: [README.md](README.md)

---

Good luck with your FPL season! ⚽🏆
