# GitHub Actions Agent Capabilities

## Complete Guide to Agentic Actions in GitHub Workflows

This document outlines all the capabilities an AI agent can have when integrated into GitHub Actions workflows, with API references and implementation examples.

---

## 📚 Table of Contents

1. [Core Capabilities Overview](#core-capabilities-overview)
2. [Repository Management](#repository-management)
3. [Pull Request Operations](#pull-request-operations)
4. [Issue Management](#issue-management)
5. [Workflow Control](#workflow-control)
6. [File Operations](#file-operations)
7. [Security and Secrets](#security-and-secrets)
8. [Implementation Patterns](#implementation-patterns)

---

## Core Capabilities Overview

### Required Permissions

```yaml
permissions:
  contents: write      # Push commits, create files, manage branches
  pull-requests: write # Create/modify PRs, add reviews
  issues: write        # Create/modify issues
  actions: write       # Trigger workflows, manage runs
  packages: write      # Publish packages
  deployments: write   # Create deployments
```

**Documentation**: [GitHub Actions Permissions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#permissions)

### Authentication Methods

1. **GITHUB_TOKEN** (Default)
   - Automatically provided
   - Scoped to current repository
   - [Token Permissions Docs](https://docs.github.com/en/actions/security-guides/automatic-token-authentication)

2. **Personal Access Token (PAT)**
   - Cross-repository access
   - Stored as secret
   - [PAT Creation Guide](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

3. **GitHub App**
   - Fine-grained permissions
   - Organization-wide access
   - [GitHub Apps Docs](https://docs.github.com/en/developers/apps/getting-started-with-apps/about-apps)

---

## Repository Management

### 1. Create Branch

```yaml
- name: Create Branch via API
  uses: actions/github-script@v7
  with:
    script: |
      await github.rest.git.createRef({
        owner: context.repo.owner,
        repo: context.repo.repo,
        ref: 'refs/heads/new-feature-branch',
        sha: context.sha
      });
```

**API Reference**: [git.createRef](https://octokit.github.io/rest.js/v20#git-create-ref)

### 2. Delete Branch

```yaml
- name: Delete Branch
  uses: actions/github-script@v7
  with:
    script: |
      await github.rest.git.deleteRef({
        owner: context.repo.owner,
        repo: context.repo.repo,
        ref: 'heads/branch-to-delete'
      });
```

**API Reference**: [git.deleteRef](https://octokit.github.io/rest.js/v20#git-delete-ref)

### 3. Commit Files

```yaml
- name: Commit Files via Git
  run: |
    git config user.name "github-actions[bot]"
    git config user.email "github-actions[bot]@users.noreply.github.com"
    echo "new content" > file.txt
    git add .
    git commit -m "Automated commit"
    git push
```

### 4. Create/Update File via API

```yaml
- name: Create or Update File
  uses: actions/github-script@v7
  with:
    script: |
      const content = Buffer.from('File content here').toString('base64');
      
      await github.rest.repos.createOrUpdateFileContents({
        owner: context.repo.owner,
        repo: context.repo.repo,
        path: 'path/to/file.txt',
        message: 'Create/update file',
        content: content,
        branch: 'main'
      });
```

**API Reference**: [repos.createOrUpdateFileContents](https://octokit.github.io/rest.js/v20#repos-create-or-update-file-contents)

### 5. Get Repository Content

```yaml
- name: Get File Content
  uses: actions/github-script@v7
  with:
    script: |
      const { data } = await github.rest.repos.getContent({
        owner: context.repo.owner,
        repo: context.repo.repo,
        path: 'README.md'
      });
      
      const content = Buffer.from(data.content, 'base64').toString();
      console.log(content);
```

**API Reference**: [repos.getContent](https://octokit.github.io/rest.js/v20#repos-get-content)

---

## Pull Request Operations

### 1. Create Pull Request

```yaml
- name: Create PR
  uses: actions/github-script@v7
  with:
    script: |
      const { data: pr } = await github.rest.pulls.create({
        owner: context.repo.owner,
        repo: context.repo.repo,
        title: 'Automated PR',
        head: 'feature-branch',
        base: 'main',
        body: 'This PR was created automatically',
        draft: false
      });
      
      console.log(`Created PR #${pr.number}`);
```

**API Reference**: [pulls.create](https://octokit.github.io/rest.js/v20#pulls-create)

### 2. Update Pull Request

```yaml
- name: Update PR
  uses: actions/github-script@v7
  with:
    script: |
      await github.rest.pulls.update({
        owner: context.repo.owner,
        repo: context.repo.repo,
        pull_number: 123,
        title: 'Updated Title',
        body: 'Updated description',
        state: 'open' // or 'closed'
      });
```

**API Reference**: [pulls.update](https://octokit.github.io/rest.js/v20#pulls-update)

### 3. Add PR Review

```yaml
- name: Add Review
  uses: actions/github-script@v7
  with:
    script: |
      await github.rest.pulls.createReview({
        owner: context.repo.owner,
        repo: context.repo.repo,
        pull_number: context.issue.number,
        event: 'APPROVE', // or 'REQUEST_CHANGES' or 'COMMENT'
        body: 'Looks good to me!'
      });
```

**API Reference**: [pulls.createReview](https://octokit.github.io/rest.js/v20#pulls-create-review)

### 4. Add PR Comment

```yaml
- name: Add PR Comment
  uses: actions/github-script@v7
  with:
    script: |
      await github.rest.issues.createComment({
        owner: context.repo.owner,
        repo: context.repo.repo,
        issue_number: context.issue.number,
        body: '## Automated Comment\nThis is an automated message.'
      });
```

**API Reference**: [issues.createComment](https://octokit.github.io/rest.js/v20#issues-create-comment)

### 5. Request Reviewers

```yaml
- name: Request Reviewers
  uses: actions/github-script@v7
  with:
    script: |
      await github.rest.pulls.requestReviewers({
        owner: context.repo.owner,
        repo: context.repo.repo,
        pull_number: 123,
        reviewers: ['username1', 'username2'],
        team_reviewers: ['team-name']
      });
```

**API Reference**: [pulls.requestReviewers](https://octokit.github.io/rest.js/v20#pulls-request-reviewers)

### 6. Merge Pull Request

```yaml
- name: Merge PR
  uses: actions/github-script@v7
  with:
    script: |
      await github.rest.pulls.merge({
        owner: context.repo.owner,
        repo: context.repo.repo,
        pull_number: 123,
        commit_title: 'Merging PR #123',
        merge_method: 'squash' // or 'merge' or 'rebase'
      });
```

**API Reference**: [pulls.merge](https://octokit.github.io/rest.js/v20#pulls-merge)

---

## Issue Management

### 1. Create Issue

```yaml
- name: Create Issue
  uses: actions/github-script@v7
  with:
    script: |
      const { data: issue } = await github.rest.issues.create({
        owner: context.repo.owner,
        repo: context.repo.repo,
        title: 'Automated Issue',
        body: 'This issue was created automatically',
        labels: ['bug', 'automated'],
        assignees: ['username']
      });
      
      console.log(`Created issue #${issue.number}`);
```

**API Reference**: [issues.create](https://octokit.github.io/rest.js/v20#issues-create)

### 2. Update Issue

```yaml
- name: Update Issue
  uses: actions/github-script@v7
  with:
    script: |
      await github.rest.issues.update({
        owner: context.repo.owner,
        repo: context.repo.repo,
        issue_number: 123,
        title: 'Updated Title',
        body: 'Updated body',
        state: 'closed', // or 'open'
        labels: ['resolved']
      });
```

**API Reference**: [issues.update](https://octokit.github.io/rest.js/v20#issues-update)

### 3. Add Labels

```yaml
- name: Add Labels
  uses: actions/github-script@v7
  with:
    script: |
      await github.rest.issues.addLabels({
        owner: context.repo.owner,
        repo: context.repo.repo,
        issue_number: 123,
        labels: ['priority:high', 'needs-review']
      });
```

**API Reference**: [issues.addLabels](https://octokit.github.io/rest.js/v20#issues-add-labels)

---

## Workflow Control

### 1. Trigger Workflow Dispatch

```yaml
- name: Trigger Another Workflow
  uses: actions/github-script@v7
  with:
    script: |
      await github.rest.actions.createWorkflowDispatch({
        owner: context.repo.owner,
        repo: context.repo.repo,
        workflow_id: 'workflow-file.yml',
        ref: 'main',
        inputs: {
          parameter1: 'value1',
          parameter2: 'value2'
        }
      });
```

**API Reference**: [actions.createWorkflowDispatch](https://octokit.github.io/rest.js/v20#actions-create-workflow-dispatch)

### 2. Cancel Workflow Run

```yaml
- name: Cancel Workflow
  uses: actions/github-script@v7
  with:
    script: |
      await github.rest.actions.cancelWorkflowRun({
        owner: context.repo.owner,
        repo: context.repo.repo,
        run_id: 123456789
      });
```

**API Reference**: [actions.cancelWorkflowRun](https://octokit.github.io/rest.js/v20#actions-cancel-workflow-run)

### 3. Re-run Workflow

```yaml
- name: Re-run Workflow
  uses: actions/github-script@v7
  with:
    script: |
      await github.rest.actions.reRunWorkflow({
        owner: context.repo.owner,
        repo: context.repo.repo,
        run_id: 123456789
      });
```

**API Reference**: [actions.reRunWorkflow](https://octokit.github.io/rest.js/v20#actions-re-run-workflow)

### 4. Get Workflow Runs

```yaml
- name: Get Workflow Runs
  uses: actions/github-script@v7
  with:
    script: |
      const { data } = await github.rest.actions.listWorkflowRuns({
        owner: context.repo.owner,
        repo: context.repo.repo,
        workflow_id: 'ci.yml',
        status: 'completed'
      });
      
      console.log(`Found ${data.total_count} completed runs`);
```

**API Reference**: [actions.listWorkflowRuns](https://octokit.github.io/rest.js/v20#actions-list-workflow-runs)

---

## File Operations

### 1. Using GitHub CLI

```yaml
- name: GitHub CLI Operations
  run: |
    # Create issue
    gh issue create --title "Bug" --body "Description"
    
    # Create PR
    gh pr create --title "Feature" --body "Description" --base main
    
    # Add PR comment
    gh pr comment ${{ github.event.pull_request.number }} --body "Comment"
    
    # Trigger workflow
    gh workflow run workflow.yml -f param=value
```

**Documentation**: [GitHub CLI Manual](https://cli.github.com/manual/)

### 2. Archive Creation

```yaml
- name: Create Archive
  run: |
    tar -czf archive.tar.gz src/
    
- name: Upload as Release Asset
  uses: actions/github-script@v7
  with:
    script: |
      const fs = require('fs');
      
      // Create release
      const { data: release } = await github.rest.repos.createRelease({
        owner: context.repo.owner,
        repo: context.repo.repo,
        tag_name: 'v1.0.0',
        name: 'Release v1.0.0'
      });
      
      // Upload asset
      await github.rest.repos.uploadReleaseAsset({
        owner: context.repo.owner,
        repo: context.repo.repo,
        release_id: release.id,
        name: 'archive.tar.gz',
        data: fs.readFileSync('archive.tar.gz')
      });
```

**API Reference**: [repos.createRelease](https://octokit.github.io/rest.js/v20#repos-create-release)

---

## Security and Secrets

### 1. Create Repository Secret

```yaml
- name: Create Secret (requires admin)
  uses: actions/github-script@v7
  with:
    script: |
      const sodium = require('tweetsodium');
      
      // Get public key
      const { data: key } = await github.rest.actions.getRepoPublicKey({
        owner: context.repo.owner,
        repo: context.repo.repo
      });
      
      // Encrypt secret
      const messageBytes = Buffer.from('secret_value');
      const keyBytes = Buffer.from(key.key, 'base64');
      const encryptedBytes = sodium.seal(messageBytes, keyBytes);
      const encrypted = Buffer.from(encryptedBytes).toString('base64');
      
      // Create secret
      await github.rest.actions.createOrUpdateRepoSecret({
        owner: context.repo.owner,
        repo: context.repo.repo,
        secret_name: 'MY_SECRET',
        encrypted_value: encrypted,
        key_id: key.key_id
      });
```

**API Reference**: [actions.createOrUpdateRepoSecret](https://octokit.github.io/rest.js/v20#actions-create-or-update-repo-secret)

### 2. Manage Deploy Keys

```yaml
- name: Add Deploy Key
  uses: actions/github-script@v7
  with:
    script: |
      await github.rest.repos.createDeployKey({
        owner: context.repo.owner,
        repo: context.repo.repo,
        title: 'Deploy Key',
        key: 'ssh-rsa AAAAB3...',
        read_only: false
      });
```

**API Reference**: [repos.createDeployKey](https://octokit.github.io/rest.js/v20#repos-create-deploy-key)

---

## Implementation Patterns

### Pattern 1: Command Parser for AI Agents

```yaml
- name: AI Agent Executor
  run: |
    RESPONSE="${{ steps.ai_agent.outputs.response }}"
    
    # Parse [COMMAND] blocks
    echo "$RESPONSE" | grep -oP '\[COMMAND\]: \K.*' | while read -r cmd; do
      echo "Executing: $cmd"
      eval "$cmd"
    done
    
    # Parse [GH] GitHub CLI commands
    echo "$RESPONSE" | grep -oP '\[GH\]: \K.*' | while read -r cmd; do
      gh $cmd
    done
    
    # Parse [FILE] creation requests
    if echo "$RESPONSE" | grep -q '\[FILE\]:'; then
      FILE_PATH=$(echo "$RESPONSE" | grep -oP '\[FILE\]: \K.*')
      CONTENT=$(echo "$RESPONSE" | grep -oP '\[CONTENT\]: \K.*' | base64 -d)
      mkdir -p $(dirname "$FILE_PATH")
      echo "$CONTENT" > "$FILE_PATH"
    fi
```

### Pattern 2: Multi-Step Agent Workflow

```yaml
name: AI Agent with Full Capabilities
on:
  pull_request:
    types: [opened]

permissions:
  contents: write
  pull-requests: write
  issues: write
  actions: write

jobs:
  ai-agent:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run AI Analysis
        id: ai
        # Your AI agent here
        
      - name: Execute AI Commands
        uses: actions/github-script@v7
        with:
          script: |
            const response = `${{ steps.ai.outputs.response }}`;
            
            // Parse JSON commands from AI
            const commands = response.match(/\[JSON\]:(.*?)\[\/JSON\]/gs) || [];
            
            for (const cmdBlock of commands) {
              const cmd = JSON.parse(cmdBlock.replace(/\[JSON\]:|\/JSON\]/g, ''));
              
              switch(cmd.action) {
                case 'create_pr':
                  await github.rest.pulls.create({
                    owner: context.repo.owner,
                    repo: context.repo.repo,
                    ...cmd.params
                  });
                  break;
                  
                case 'create_issue':
                  await github.rest.issues.create({
                    owner: context.repo.owner,
                    repo: context.repo.repo,
                    ...cmd.params
                  });
                  break;
                  
                case 'trigger_workflow':
                  await github.rest.actions.createWorkflowDispatch({
                    owner: context.repo.owner,
                    repo: context.repo.repo,
                    ...cmd.params
                  });
                  break;
              }
            }
```

### Pattern 3: Safe Sandboxed Execution

```yaml
- name: Sandboxed Command Execution
  run: |
    RESPONSE="${{ steps.ai.outputs.response }}"
    
    # Extract code blocks marked as executable
    if echo "$RESPONSE" | grep -q '```execute'; then
      CODE=$(echo "$RESPONSE" | sed -n '/```execute/,/```/p' | sed '1d;$d')
      
      # Run in Docker container for safety
      docker run --rm \
        --network none \
        --memory 512m \
        --cpus 0.5 \
        -v $PWD:/workspace:ro \
        alpine:latest \
        sh -c "$CODE"
    fi
```

---

## Repository Settings Requirements

### Enable PR Creation

1. Go to **Settings** → **Actions** → **General**
2. Under **Workflow permissions**, enable:
   - ✅ Read and write permissions
   - ✅ Allow GitHub Actions to create and approve pull requests

### Organization Settings

For organization repositories, these must first be enabled at the organization level:
1. **Organization Settings** → **Actions** → **General**
2. Enable the same permissions as above

---

## Security Best Practices

1. **Principle of Least Privilege**
   - Only grant permissions actually needed
   - Use job-level permissions when possible

2. **Token Handling**
   - Never log tokens
   - Use GitHub Secrets for sensitive data
   - Rotate tokens regularly

3. **Fork PR Restrictions**
   - PRs from forks get read-only tokens by default
   - Be cautious with `pull_request_target` trigger

4. **Audit and Monitoring**
   - Review workflow runs regularly
   - Monitor for unexpected behavior
   - Use branch protection rules

---

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Octokit.js REST API Reference](https://octokit.github.io/rest.js/v20)
- [GitHub CLI Manual](https://cli.github.com/manual/)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Authentication in Workflows](https://docs.github.com/en/actions/security-guides/automatic-token-authentication)
- [GitHub Actions Permissions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#permissions)
- [actions/github-script](https://github.com/actions/github-script)