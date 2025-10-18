#!/usr/bin/env python3
"""
Claude AI Code Review Script
Performs intelligent code review on pull requests
"""

import os
import sys
import json
from anthropic import Anthropic
from github import Github

# Configuration
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
REPO_OWNER = os.environ.get('REPO_OWNER')
REPO_NAME = os.environ.get('REPO_NAME')
PR_NUMBER = int(os.environ.get('PR_NUMBER'))
PR_TITLE = os.environ.get('PR_TITLE')
PR_AUTHOR = os.environ.get('PR_AUTHOR')
PR_LABELS = os.environ.get('PR_LABELS', '').split(',')
IS_RENOVATE = os.environ.get('IS_RENOVATE', 'false') == 'true'
HAS_DOCKERFILE = os.environ.get('HAS_DOCKERFILE', 'false') == 'true'
HAS_WORKFLOW = os.environ.get('HAS_WORKFLOW', 'false') == 'true'

def get_pr_diff(github_client, repo, pr_number):
    """Get the PR diff content"""
    pr = repo.get_pull(pr_number)
    files = pr.get_files()

    diff_content = []
    for file in files:
        if file.patch:
            diff_content.append(f"\n### File: {file.filename}\n")
            diff_content.append(f"Status: {file.status}\n")
            diff_content.append(f"Changes: +{file.additions} -{file.deletions}\n")
            diff_content.append(f"\n```diff\n{file.patch}\n```\n")

    return "\n".join(diff_content)

def build_review_prompt(pr, diff_content):
    """Build the Claude prompt for code review"""

    # Determine focus areas based on PR context
    focus_areas = []

    if IS_RENOVATE:
        focus_areas.extend([
            "Dependency security (check for known CVEs)",
            "Version compatibility with GeoServer",
            "Breaking changes in updated packages"
        ])

    if HAS_DOCKERFILE:
        focus_areas.extend([
            "Docker best practices (multi-stage builds, layer optimization)",
            "Security hardening (non-root user, minimal base image)",
            "UBI9/RHEL enterprise compatibility"
        ])

    if HAS_WORKFLOW:
        focus_areas.extend([
            "GitHub Actions security (pinned versions, secrets handling)",
            "Workflow efficiency and optimization",
            "Error handling and retry logic"
        ])

    # Add general focus areas
    focus_areas.extend([
        "Security vulnerabilities and CVEs",
        "Code quality and maintainability",
        "GeoServer-specific configuration issues"
    ])

    prompt = f"""You are a senior DevOps engineer reviewing a pull request for the geoserver-docker-rhel repository.

**Repository Context:**
This is an enterprise fork of the GeoServer Docker project that uses RHEL9/UBI9 base images for security and compliance.
The repository emphasizes security, stability, and enterprise hardening.

**Pull Request Details:**
- Title: {PR_TITLE}
- Author: {PR_AUTHOR}
- Labels: {', '.join(PR_LABELS) if PR_LABELS else 'None'}
- Type: {'Renovate dependency update' if IS_RENOVATE else 'Manual contribution'}

**Review Focus Areas:**
{chr(10).join(f"- {area}" for area in focus_areas)}

**Changes to Review:**
{diff_content}

**Your Task:**
1. Review the code changes thoroughly
2. Identify any security issues, bugs, or quality concerns
3. Check if changes align with enterprise best practices
4. For Renovate PRs, verify the dependency update is safe
5. Provide constructive feedback

**Response Format:**
Provide your review in this exact format:

## Security Analysis
[Your security assessment]

## Code Quality
[Your code quality assessment]

## GeoServer/Docker Specific
[Any GeoServer or Docker-specific concerns]

## Recommendation
[One of: APPROVE, REQUEST_CHANGES, or COMMENT]

## Summary
[2-3 sentence summary of your review]

## Detailed Feedback
[Specific line-by-line feedback if needed]

**Important:**
- Only APPROVE if there are NO security issues and changes are safe
- For Renovate PRs with 'automerge' label, be strict but fair
- For major version updates, always REQUEST_CHANGES for manual review
- Provide actionable feedback
"""

    return prompt

def post_review_comment(github_client, repo, pr_number, review_text, recommendation):
    """Post the review as a PR comment"""
    pr = repo.get_pull(pr_number)

    # Determine review event type
    if recommendation == "APPROVE":
        event = "APPROVE"
        emoji = "✅"
    elif recommendation == "REQUEST_CHANGES":
        event = "REQUEST_CHANGES"
        emoji = "⚠️"
    else:
        event = "COMMENT"
        emoji = "💡"

    # Format the comment
    comment_body = f"""## {emoji} Claude AI Code Review

{review_text}

---
<sub>🤖 Automated review by Claude AI | [Learn more](.github/AI-AGENTS.md)</sub>
"""

    # Create the review
    try:
        pr.create_review(body=comment_body, event=event)
        print(f"Posted {event} review on PR #{pr_number}")

        # Write approval status to file for workflow
        if recommendation == "APPROVE":
            with open('/tmp/claude_approval.txt', 'w') as f:
                f.write('APPROVE')

    except Exception as e:
        print(f"Error posting review: {e}")
        # Fallback to comment
        pr.create_issue_comment(comment_body)

def main():
    """Main execution"""
    if not ANTHROPIC_API_KEY:
        print("Error: ANTHROPIC_API_KEY not set")
        sys.exit(1)

    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN not set")
        sys.exit(1)

    print(f"Starting Claude review for PR #{PR_NUMBER}")

    # Initialize clients
    anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)
    github_client = Github(GITHUB_TOKEN)
    repo = github_client.get_repo(f"{REPO_OWNER}/{REPO_NAME}")

    # Get PR diff
    print("Fetching PR diff...")
    diff_content = get_pr_diff(github_client, repo, PR_NUMBER)

    if not diff_content or len(diff_content) < 10:
        print("No significant changes to review")
        sys.exit(0)

    # Build review prompt
    print("Building review prompt...")
    prompt = build_review_prompt(repo.get_pull(PR_NUMBER), diff_content)

    # Call Claude API
    print("Calling Claude API for review...")
    try:
        message = anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            temperature=0.3,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        review_text = message.content[0].text

        # Extract recommendation
        recommendation = "COMMENT"
        if "APPROVE" in review_text and "## Recommendation" in review_text:
            if review_text.split("## Recommendation")[1].split("\n")[1].strip() == "APPROVE":
                recommendation = "APPROVE"
        elif "REQUEST_CHANGES" in review_text:
            recommendation = "REQUEST_CHANGES"

        print(f"Claude recommendation: {recommendation}")

        # Post review
        print("Posting review to PR...")
        post_review_comment(github_client, repo, PR_NUMBER, review_text, recommendation)

        print("✅ Review completed successfully")

    except Exception as e:
        print(f"Error calling Claude API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
