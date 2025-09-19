# Cursor CLI GitHub Actions Configuration

## Overview

This repository uses the Cursor CLI agent for automated code review, issue triage, and security analysis in GitHub Actions workflows.

## Required Secrets

### CURSOR_API_KEY
- **Required**: Yes
- **Description**: API key for authenticating with the Cursor service
- **How to obtain**:
  1. Go to the Cursor dashboard (https://cursor.com)
  2. Generate an API key from your account settings
- **Setup**: Add as an environment secret in the `cursor-env` environment

### GITHUB_TOKEN
- **Required**: Yes (automatically provided by GitHub Actions)
- **Description**: Token for GitHub API operations
- **Note**: This is automatically available in workflows, no manual setup needed

## Optional Configuration

### APP_ID and APP_PRIVATE_KEY
- **Required**: No (optional for using GitHub App authentication)
- **Description**: If you want to use a GitHub App for authentication instead of GITHUB_TOKEN
- **Setup**: Create a GitHub App and add the credentials as secrets

## Workflow Files

### cursor-dispatch.yml
Main dispatcher that routes requests to appropriate workflows based on triggers:
- PR comments starting with `@cursor`
- PR reviews
- Issue comments
- New PRs and issues

### cursor-review.yml
Performs automated code review on pull requests with full autonomy to:
- Analyze code changes
- Post review comments
- Approve or request changes

### cursor-invoke.yml
General-purpose workflow for handling various development tasks with full git and GitHub CLI access.

### cursor-triage.yml
Automatically labels issues based on their content.

### cursor-scheduled-triage.yml
Runs hourly to triage unlabeled issues.

### securereview-7.yml
Security-focused review workflow that analyzes PRs for vulnerabilities.

## Migration from Gemini CLI

This repository has been migrated from Google's Gemini CLI to Cursor CLI with full autonomy configuration. Key changes:

1. **Simplified Configuration**: No need for Google Cloud Platform setup
2. **Full Autonomy**: The agent has complete access to git and GitHub CLI operations
3. **Direct Command Execution**: Uses `cursor-agent` command directly instead of action-based approach
4. **Single API Key**: Only requires CURSOR_API_KEY instead of multiple GCP credentials

## Usage

### Triggering Reviews

Comment on a PR with:
- `@cursor` - General invoke
- `@cursor /review` - Trigger code review
- `@cursor /triage` - Trigger issue triage

### Environment Setup

For workflows to function properly, ensure:

1. The `cursor-env` environment is configured in repository settings
   - Go to Settings → Environments → New environment
   - Name it `cursor-env`
   - Add the CURSOR_API_KEY secret to this environment
2. CURSOR_API_KEY is added as an environment secret (not repository secret)
3. Workflow permissions are set appropriately (the workflows include required permissions)

## Troubleshooting

### API Key Issues
If you see "CURSOR_API_KEY secret is NOT set or empty":
1. Verify the secret is added in repository settings
2. Check if you're using environment protection and the secret is in the right environment

### Rate Limiting
The Cursor API has rate limits. If you encounter issues:
1. Check your API key tier at https://cursor.com/docs/cli/pricing
2. Consider implementing retry logic or upgrading your plan

### Workflow Failures
Check the workflow logs in the Actions tab for detailed error messages.