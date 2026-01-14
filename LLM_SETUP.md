# LLM Provider Setup Guide

The FPL Assistant supports multiple LLM providers through the Strands Agents SDK. Choose the one that best fits your needs.

## Supported LLM Providers

### Option 1: Anthropic Claude (Recommended)

**Best for**: Production use, reliability, and tool calling capabilities

**Setup:**
1. Get API key from [Anthropic Console](https://console.anthropic.com/)
2. Add to `.env`:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-...
   ```

**Models available:**
- `claude-3-5-sonnet-20241022` (Default - Best for complex reasoning)
- `claude-3-sonnet-20240229` (Good balance)
- `claude-3-haiku-20240307` (Fastest, cheaper)

**Pricing** (as of 2024):
- Sonnet 3.5: $3/$15 per 1M input/output tokens
- Very cost-effective for this use case

---

### Option 2: OpenAI (GPT-4, GPT-3.5)

**Best for**: Widespread availability, familiar API

**Setup:**
1. Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Add to `.env`:
   ```bash
   OPENAI_API_KEY=sk-...
   ```

**Models available:**
- `gpt-4-turbo-preview` (Most capable)
- `gpt-4` (Reliable)
- `gpt-3.5-turbo` (Fast and cheap)

**Pricing:**
- GPT-4: $10/$30 per 1M input/output tokens
- GPT-3.5: $0.50/$1.50 per 1M tokens

---

### Option 3: AWS Bedrock

**Best for**: Enterprise use, AWS integration, compliance

**Setup:**
1. Enable Bedrock in your AWS account
2. Request model access for Claude or other models
3. Configure AWS credentials:
   ```bash
   AWS_REGION=us-east-1
   AWS_ACCESS_KEY_ID=your_key
   AWS_SECRET_ACCESS_KEY=your_secret
   ```

**Models available:**
- `anthropic.claude-3-sonnet-20240229-v1:0`
- `anthropic.claude-3-haiku-20240307-v1:0`
- `meta.llama3-70b-instruct-v1:0`
- And more...

**Benefits:**
- No separate API key needed
- Integrated billing with AWS
- VPC/PrivateLink support
- Enterprise compliance

---

### Option 4: Google Gemini

**Best for**: Google Cloud integration, multimodal capabilities

**Setup:**
1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to `.env`:
   ```bash
   GOOGLE_API_KEY=...
   ```

**Models available:**
- `gemini-pro` (Default)
- `gemini-pro-vision` (Multimodal)

**Pricing:**
- Gemini Pro: Free tier available, then $0.50/$1.50 per 1M tokens

---

### Option 5: Ollama (Local/Free)

**Best for**: Privacy, offline use, no API costs

**Setup:**
1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Pull a model:
   ```bash
   ollama pull llama2
   # or
   ollama pull mistral
   ollama pull codellama
   ```
3. Add to `.env`:
   ```bash
   OLLAMA_MODEL=llama2
   ```

**Models available:**
- `llama2` (7B, 13B, 70B)
- `mistral` (7B)
- `codellama` (7B, 13B, 34B)
- `mixtral` (8x7B)

**Requirements:**
- Runs locally on your machine
- Requires sufficient RAM (8GB+ for 7B models)
- No API costs
- Complete privacy

---

## Recommended Setup by Use Case

### For Development/Testing
```bash
# Option 1: Ollama (Free, local)
OLLAMA_MODEL=llama2

# Option 2: Anthropic (Reliable, cheap)
ANTHROPIC_API_KEY=sk-ant-...
```

### For Production
```bash
# Best reliability and tool calling
ANTHROPIC_API_KEY=sk-ant-...
MODEL=claude-3-5-sonnet-20241022
```

### For Enterprise
```bash
# AWS Bedrock with Claude
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
MODEL=anthropic.claude-3-sonnet-20240229-v1:0
```

### For Privacy/Offline
```bash
# Local Ollama - no data leaves your machine
OLLAMA_MODEL=llama2
```

---

## Model Override

By default, Strands SDK uses the best model for your provider. To override:

```bash
# In .env
MODEL=your-specific-model-name
```

Examples:
- `MODEL=claude-3-haiku-20240307` (Faster Anthropic)
- `MODEL=gpt-3.5-turbo` (Cheaper OpenAI)
- `MODEL=mistral` (Different Ollama model)

---

## Cost Estimation

For typical FPL Assistant usage:

**Light use** (10 queries/day):
- Anthropic: ~$0.10-0.50/month
- OpenAI: ~$0.20-1.00/month
- Ollama: $0 (free)

**Heavy use** (100 queries/day):
- Anthropic: ~$1-5/month
- OpenAI: ~$2-10/month
- Ollama: $0 (free)

Tool calls add minimal cost as responses are relatively small.

---

## Testing Your Configuration

After configuring your `.env`, test it:

```bash
python agent.py
```

You should see:
```
✓ LLM Provider: Anthropic Claude  # or your chosen provider
✓ Team ID configured: 12345
```

Try a simple query:
```
You: Search for Salah
```

If it works, you're all set!

---

## Troubleshooting

**"No LLM API key detected"**
- Make sure `.env` file exists
- Check that the API key is uncommented
- Verify no typos in variable names

**"Authentication failed"**
- Verify your API key is correct
- Check that your account has credits/access
- For AWS: verify IAM permissions

**"Model not found"**
- For Bedrock: ensure model access is enabled
- For Ollama: run `ollama pull model-name` first
- Check model name spelling

**Slow responses**
- Try a smaller/faster model (Haiku, GPT-3.5, or smaller Ollama model)
- Check internet connection (for API providers)
- For Ollama: ensure sufficient RAM

---

## Switching Providers

To switch between providers, just update `.env`:

```bash
# From Anthropic to OpenAI
# Comment out:
# ANTHROPIC_API_KEY=sk-ant-...

# Uncomment:
OPENAI_API_KEY=sk-...
```

Restart `agent.py` and it will use the new provider automatically.

---

## Best Practices

1. **Start with Anthropic or Ollama**: Anthropic for reliability, Ollama for free/privacy
2. **Use environment variables**: Never commit API keys to git
3. **Monitor costs**: Most providers have dashboards to track usage
4. **Use cheaper models for testing**: Switch to Haiku/GPT-3.5 during development
5. **Consider Ollama for privacy**: If handling sensitive team data

---

For more information on Strands SDK:
- GitHub: https://github.com/strands-agents/sdk-python
- Documentation: Check the repo for latest docs
