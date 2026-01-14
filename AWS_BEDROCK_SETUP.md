# AWS Bedrock Setup Guide for FPL Assistant

This guide will help you configure AWS Bedrock as your LLM provider for the FPL Assistant.

## Prerequisites

1. **AWS Account**: You need an active AWS account
2. **AWS CLI** (optional but recommended): Install from https://aws.amazon.com/cli/

## Step 1: Enable AWS Bedrock Access

### 1.1 Access the Bedrock Console

1. Log in to [AWS Console](https://console.aws.amazon.com/)
2. Navigate to **Amazon Bedrock** service
   - Search for "Bedrock" in the services search bar
   - Or go directly to: https://console.aws.amazon.com/bedrock/
3. Select your preferred region (e.g., `us-east-1`, `us-west-2`)

### 1.2 Request Model Access

1. In the Bedrock console, click **"Model access"** in the left sidebar
2. Click **"Enable specific models"** or **"Manage model access"**
3. Request access to Claude models (recommended):
   - ✓ **Claude 3.5 Sonnet** (anthropic.claude-3-5-sonnet-20241022-v2:0)
   - ✓ **Claude 3 Sonnet** (anthropic.claude-3-sonnet-20240229-v1:0)
   - ✓ **Claude 3 Haiku** (anthropic.claude-3-haiku-20240307-v1:0)
4. Click **"Request model access"**
5. Wait for approval (usually instant for Claude models)

**Note**: Some models may require you to accept terms of service.

## Step 2: Create IAM User with Bedrock Access

### 2.1 Create IAM User

1. Go to **IAM Console**: https://console.aws.amazon.com/iam/
2. Click **"Users"** → **"Add users"**
3. Enter a username (e.g., `fpl-assistant-bedrock`)
4. Select **"Access key - Programmatic access"**
5. Click **"Next: Permissions"**

### 2.2 Attach Bedrock Permissions

**Option A: Using Managed Policy (Simpler)**
1. Click **"Attach existing policies directly"**
2. Search for and select: **"AmazonBedrockFullAccess"**
3. Click **"Next"** → **"Create user"**

**Option B: Custom Policy (More Secure - Recommended)**
1. Click **"Create policy"**
2. Select **JSON** tab
3. Paste this policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0",
                "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0",
                "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-haiku-20240307-v1:0"
            ]
        }
    ]
}
```

4. Click **"Review policy"**
5. Name it: `FPL-Assistant-Bedrock-Access`
6. Click **"Create policy"**
7. Go back to user creation and attach this policy

### 2.3 Save Access Keys

1. After creating the user, you'll see the **Access key ID** and **Secret access key**
2. **IMPORTANT**: Download the CSV or copy these values - you won't see them again!
3. Keep these secure and never commit them to git

## Step 3: Configure Your FPL Assistant

### 3.1 Update .env File

```bash
cd /Users/ajaydhungel/Documents/strands/fpl-assistant
cp .env.example .env
```

Edit `.env` and configure AWS Bedrock:

```bash
# FPL Team Configuration
FPL_TEAM_ID=your_fpl_team_id

# AWS Bedrock Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIA...your_access_key...
AWS_SECRET_ACCESS_KEY=your_secret_access_key

# Optional: Specify which Claude model to use
MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
```

### 3.2 Available Models on Bedrock

| Model | Model ID | Best For | Cost |
|-------|----------|----------|------|
| Claude 3.5 Sonnet | `anthropic.claude-3-5-sonnet-20241022-v2:0` | Complex reasoning, best quality | $$ |
| Claude 3 Sonnet | `anthropic.claude-3-sonnet-20240229-v1:0` | Balanced performance | $$ |
| Claude 3 Haiku | `anthropic.claude-3-haiku-20240307-v1:0` | Fast responses, lower cost | $ |

**Recommendation**: Use Claude 3.5 Sonnet for best results.

## Step 4: Install Dependencies

```bash
# Activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies (includes boto3 for AWS)
pip install -r requirements.txt
```

## Step 5: Test Your Configuration

```bash
python agent.py
```

You should see:
```
✓ LLM Provider: AWS Bedrock
✓ Team ID configured: 12345
```

Try a test query:
```
You: Search for Mohamed Salah
```

If you get player information back, you're all set!

## Alternative: Using AWS CLI Credentials

Instead of using environment variables, you can configure AWS CLI:

```bash
aws configure
```

Enter:
- AWS Access Key ID: `AKIA...`
- AWS Secret Access Key: `...`
- Default region: `us-east-1`
- Default output format: `json`

This stores credentials in `~/.aws/credentials` and the FPL Assistant will automatically use them.

**Pros**:
- More secure (credentials not in .env)
- Can use with other AWS tools
- Supports profiles for multiple accounts

**Cons**:
- System-wide configuration
- Less explicit in the project

## Regions with Bedrock Availability

Not all AWS regions support Bedrock. Supported regions include:

- `us-east-1` (N. Virginia) - **Recommended**
- `us-west-2` (Oregon)
- `ap-southeast-1` (Singapore)
- `ap-northeast-1` (Tokyo)
- `eu-central-1` (Frankfurt)
- `eu-west-1` (Ireland)
- `eu-west-3` (Paris)

Choose the region closest to you for best latency.

## Cost Estimation

AWS Bedrock Claude 3.5 Sonnet pricing (as of 2024):

**Input tokens**: $3.00 per 1M tokens
**Output tokens**: $15.00 per 1M tokens

**Estimated costs for FPL Assistant**:

- **Light use** (10 queries/day): ~$0.50-2/month
- **Medium use** (50 queries/day): ~$2-8/month
- **Heavy use** (100 queries/day): ~$5-15/month

Each query typically uses:
- ~500-2000 input tokens (tools, context)
- ~200-500 output tokens (response)

You can monitor costs in AWS Cost Explorer.

## Troubleshooting

### Error: "Could not connect to the endpoint URL"

**Solution**: Check your AWS region is correct and supports Bedrock.

```bash
# Try a different region in .env
AWS_REGION=us-west-2
```

### Error: "AccessDeniedException"

**Solution**: Your IAM user doesn't have Bedrock permissions.

1. Go to IAM Console
2. Find your user
3. Ensure `AmazonBedrockFullAccess` policy is attached
4. Or check that your custom policy includes `bedrock:InvokeModel`

### Error: "ValidationException: The provided model identifier is invalid"

**Solution**: The model ID is wrong or you haven't requested access.

1. Check Model Access in Bedrock console
2. Verify the model ID in your .env matches exactly:
   ```bash
   MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
   ```

### Error: "ResourceNotFoundException"

**Solution**: Model not available in your region.

- Try `us-east-1` which has all models
- Or check which models are available in your region

### Error: "ThrottlingException"

**Solution**: You're hitting rate limits.

- Wait a few seconds between requests
- Consider using Claude 3 Haiku (higher limits)
- Request a service limit increase in AWS console

### Connection timeout issues

**Solution**: Check your internet connection and AWS service status.

```bash
# Test AWS connectivity
aws bedrock list-foundation-models --region us-east-1
```

## Security Best Practices

1. **Never commit credentials to git**
   - The `.gitignore` already excludes `.env`
   - Double-check before committing

2. **Use IAM roles when possible**
   - If running on EC2/ECS, use IAM roles instead of access keys
   - No need to store credentials

3. **Rotate access keys regularly**
   - Change keys every 90 days
   - Use AWS Secrets Manager for production

4. **Principle of least privilege**
   - Only grant permissions needed (InvokeModel)
   - Restrict to specific model ARNs

5. **Enable CloudTrail logging**
   - Monitor Bedrock API calls
   - Set up alerts for suspicious activity

6. **Use separate AWS accounts**
   - Development vs Production
   - Different credentials for each

## Monitoring and Optimization

### View Usage in AWS Console

1. Go to Bedrock console
2. Click **"Usage"** in the left sidebar
3. View token usage and costs

### Optimize Costs

1. **Use Claude 3 Haiku for simple queries**: ~70% cheaper
2. **Cache system prompt**: Strands SDK handles this
3. **Limit response length**: Add constraints to prompts
4. **Use specific tools**: Reduces token usage vs open-ended queries

### Set up Billing Alerts

1. Go to AWS Billing console
2. Create a budget alert (e.g., $10/month)
3. Get notified before costs get high

## Advanced: Using with Docker

If you want to containerize the FPL Assistant:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Don't copy .env - pass as environment variables
CMD ["python", "agent.py"]
```

Run with:
```bash
docker run -e AWS_REGION=us-east-1 \
           -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
           -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
           -e FPL_TEAM_ID=12345 \
           fpl-assistant
```

## Support

For AWS Bedrock specific issues:
- AWS Support: https://console.aws.amazon.com/support/
- Bedrock Documentation: https://docs.aws.amazon.com/bedrock/
- Service Status: https://status.aws.amazon.com/

For Strands SDK issues:
- GitHub: https://github.com/strands-agents/sdk-python

---

You're now ready to use AWS Bedrock with your FPL Assistant! 🚀
