# Fix for "fatal: ambiguous argument 'origin/main...HEAD'" Error

## Problem
When running `git diff origin/main...HEAD` in a GitHub Actions workflow during a pull request, you get:
```
fatal: ambiguous argument 'origin/main...HEAD': unknown revision or path not in the working tree.
```

## Root Cause
GitHub Actions performs a shallow clone by default and doesn't fetch all branches, especially in PR contexts. The base branch (`origin/main`) isn't available in the runner's git repository.

## Solutions

### Solution 1: Fetch Full History (Recommended)
```yaml
steps:
  - name: Checkout repository
    uses: actions/checkout@v4
    with:
      fetch-depth: 0  # Fetch all history for all branches
```

### Solution 2: Explicitly Fetch Base Branch
```yaml
steps:
  - name: Checkout repository
    uses: actions/checkout@v4
    
  - name: Fetch base branch
    run: |
      git fetch origin main:main
      git fetch origin ${{ github.base_ref }}
```

### Solution 3: Use GitHub Context Variables
```yaml
steps:
  - name: Checkout repository  
    uses: actions/checkout@v4
    with:
      fetch-depth: 0
      
  - name: Get PR diff
    run: |
      # Use the PR's base branch from GitHub context
      git diff origin/${{ github.event.pull_request.base.ref }}...HEAD
```

### Solution 4: Complete PR Checkout Pattern
```yaml
steps:
  - name: Checkout PR
    uses: actions/checkout@v4
    with:
      fetch-depth: 0
      # For PRs, also fetch the base branch
      ref: ${{ github.event.pull_request.head.sha }}
      
  - name: Fetch base branch for comparison
    run: |
      git fetch origin ${{ github.event.pull_request.base.ref }}:${{ github.event.pull_request.base.ref }}
      
  - name: Get PR diff
    run: |
      git diff ${{ github.event.pull_request.base.ref }}...HEAD
```

## Best Practice for PR Workflows

```yaml
name: PR Analysis

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code with history
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # IMPORTANT: Get full history
          
      - name: Fetch base branch
        run: |
          # Ensure we have the base branch
          git fetch origin ${{ github.event.pull_request.base.ref }}
          
      - name: Analyze PR changes
        run: |
          echo "Base branch: ${{ github.event.pull_request.base.ref }}"
          echo "Head branch: ${{ github.event.pull_request.head.ref }}"
          
          # Now this will work
          git diff origin/${{ github.event.pull_request.base.ref }}...HEAD
          
          # Or get just the list of changed files
          git diff --name-only origin/${{ github.event.pull_request.base.ref }}...HEAD
          
          # Or get diff statistics
          git diff --stat origin/${{ github.event.pull_request.base.ref }}...HEAD
```

## Debugging Commands

Add these to your workflow to debug git state:

```yaml
- name: Debug git state
  run: |
    echo "=== Git branches ==="
    git branch -a
    
    echo "=== Git remotes ==="
    git remote -v
    
    echo "=== Git log ==="
    git log --oneline -10
    
    echo "=== GitHub context ==="
    echo "Base ref: ${{ github.event.pull_request.base.ref }}"
    echo "Head ref: ${{ github.event.pull_request.head.ref }}"
    echo "Base SHA: ${{ github.event.pull_request.base.sha }}"
    echo "Head SHA: ${{ github.event.pull_request.head.sha }}"
```

## Key Points

1. **Always use `fetch-depth: 0`** for workflows that need git history
2. **Explicitly fetch the base branch** when working with PRs
3. **Use GitHub context variables** instead of hardcoding branch names
4. **Test with different PR scenarios** (from forks, different branches, etc.)

## Applied to SecureReview-7

If SecureReview-7 needs to analyze PR diffs, update the checkout step:

```yaml
- name: Checkout repository
  uses: actions/checkout@v4
  with:
    fetch-depth: 0  # Add this line
    
- name: Fetch base branch for comparison
  run: |
    git fetch origin ${{ github.event.pull_request.base.ref }}
```

This ensures the Gemini analysis has access to the complete diff between the PR and its base branch.