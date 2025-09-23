# Gemini Security Review Setup Guide

## Overview
This repository now includes a Google Gemini-based security review workflow that automatically analyzes pull requests for security vulnerabilities and potential risks.

## Setup Instructions

### 1. Obtain Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Get API Key" or "Create API Key"
4. Copy the generated API key

### 2. Configure GitHub Repository Secrets
1. Navigate to your repository on GitHub
2. Go to **Settings** → **Secrets and variables** → **Actions**
3. Click "New repository secret"
4. Add the following secret:
   - **Name:** `GEMINI_API_KEY`
   - **Value:** Your Gemini API key from step 1

### 3. Workflow Configuration
The workflow is configured in `.github/workflows/securereview-gemini.yml` and will:
- Automatically trigger on pull request events (opened, synchronized, reopened)
- Analyze code changes for security vulnerabilities
- Post analysis results as PR comments
- Approve or request changes based on security assessment

## Required Secrets

| Secret Name | Description | Required |
|------------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key for AI analysis | ✅ Yes |
| `GITHUB_TOKEN` | GitHub token (automatically provided) | ✅ Yes (automatic) |

## Environment Variables
The workflow automatically sets these environment variables:
- `PR_NUMBER` - Pull request number
- `PR_TITLE` - Pull request title
- `PR_BODY` - Pull request description
- `BASE_SHA` - Base commit SHA
- `HEAD_SHA` - Head commit SHA

## Features

### Security Analysis Checks
The Gemini-based review analyzes for:
- Security vulnerabilities
- Potential exploits
- Data leaks
- Authentication/authorization issues
- Injection attacks
- Cryptographic weaknesses
- Supply chain risks

### Workflow Actions
Based on the analysis, the workflow will:
- **APPROVE**: Add `security-approved` label and approve the PR
- **BLOCK**: Add `security-review-failed` label and request changes
- **PENDING**: Post analysis without verdict (in case of errors)

## Testing the Workflow

1. Create a new pull request in your repository
2. The workflow will automatically run
3. Check the "Actions" tab to monitor progress
4. Review the security analysis comment on the PR

## Troubleshooting

### API Key Issues
- Verify the `GEMINI_API_KEY` secret is properly set
- Check that the API key has not expired
- Ensure the API key has sufficient quota

### Workflow Failures
- Check the Actions tab for detailed error logs
- Review the uploaded artifact `securereview-gemini-output` for debugging
- Ensure Python 3.11+ is available (workflow installs it automatically)

### Rate Limits
- Google Gemini API has generous free tier limits
- For production use, consider upgrading to a paid plan
- Monitor API usage in [Google AI Studio](https://aistudio.google.com)

## API Pricing
- **Free Tier**: 60 requests per minute
- **Paid Plans**: Available for higher volume needs
- See [Google AI pricing](https://ai.google.dev/pricing) for details

## Migration from Cursor
This workflow replaces the Cursor-based `securereview-7.yml` with a Gemini-based solution:
- No need for Cursor CLI installation
- Uses Google's Gemini 1.5 Pro model
- Python-based implementation for better control
- Same security analysis capabilities

## Support
For issues or questions:
- Check workflow logs in the Actions tab
- Review this documentation
- Contact repository maintainers