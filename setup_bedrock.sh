#!/bin/bash

# FPL Assistant - AWS Bedrock Setup Script

echo "=============================================="
echo "FPL Assistant - AWS Bedrock Setup"
echo "=============================================="
echo ""

# Check if running in the correct directory
if [ ! -f "agent.py" ]; then
    echo "Error: Please run this script from the fpl-assistant directory"
    exit 1
fi

# Step 1: Create virtual environment
echo "Step 1: Creating Python virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Step 2: Activate virtual environment
echo ""
echo "Step 2: Activating virtual environment..."
source .venv/bin/activate
echo "✓ Virtual environment activated"

# Step 3: Install dependencies
echo ""
echo "Step 3: Installing dependencies (including boto3 for AWS)..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Step 4: Configure environment
echo ""
echo "Step 4: Setting up .env file..."
if [ ! -f ".env" ]; then
    cp .env.bedrock .env
    echo "✓ .env file created from template"
    echo ""
    echo "⚠ IMPORTANT: You need to edit .env and add your AWS credentials!"
else
    echo "⚠ .env file already exists - skipping"
fi

# Step 5: Check AWS CLI
echo ""
echo "Step 5: Checking AWS CLI..."
if command -v aws &> /dev/null; then
    echo "✓ AWS CLI is installed"

    # Check if AWS credentials are configured
    if aws sts get-caller-identity &> /dev/null; then
        echo "✓ AWS credentials are configured"
        echo ""
        echo "You can use existing AWS CLI credentials or configure .env file"
    else
        echo "⚠ AWS CLI is installed but credentials not configured"
        echo "  Run: aws configure"
    fi
else
    echo "⚠ AWS CLI not installed (optional)"
    echo "  Install from: https://aws.amazon.com/cli/"
fi

# Step 6: Test Bedrock access
echo ""
echo "Step 6: Testing AWS Bedrock access..."
if aws bedrock list-foundation-models --region us-east-1 &> /dev/null 2>&1; then
    echo "✓ AWS Bedrock is accessible"

    # Check for Claude models
    if aws bedrock list-foundation-models --region us-east-1 --by-provider anthropic &> /dev/null 2>&1; then
        echo "✓ Claude models are available"
    fi
else
    echo "⚠ Cannot access AWS Bedrock"
    echo "  Make sure you have:"
    echo "  1. Valid AWS credentials"
    echo "  2. Bedrock access enabled in your region"
    echo "  3. Model access requested in Bedrock console"
fi

# Final instructions
echo ""
echo "=============================================="
echo "Setup Complete!"
echo "=============================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Edit .env file with your credentials:"
echo "   nano .env"
echo ""
echo "   Required fields:"
echo "   - FPL_TEAM_ID (from fantasy.premierleague.com)"
echo "   - AWS_REGION (e.g., us-east-1)"
echo "   - AWS_ACCESS_KEY_ID"
echo "   - AWS_SECRET_ACCESS_KEY"
echo ""
echo "2. Request model access in AWS Bedrock console:"
echo "   https://console.aws.amazon.com/bedrock/"
echo "   Enable: Claude 3.5 Sonnet"
echo ""
echo "3. Run the assistant:"
echo "   python agent.py"
echo ""
echo "For detailed setup instructions, see:"
echo "   AWS_BEDROCK_SETUP.md"
echo ""
