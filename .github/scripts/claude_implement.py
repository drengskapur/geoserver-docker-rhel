#!/usr/bin/env python3
"""
Claude AI Feature Implementation Script
Implements features based on GitHub issues
"""

import os
import sys
import subprocess
from anthropic import Anthropic
from github import Github

# Configuration
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
REPO_OWNER = os.environ.get('REPO_OWNER')
REPO_NAME = os.environ.get('REPO_NAME')
ISSUE_NUMBER = int(os.environ.get('ISSUE_NUMBER'))
ISSUE_TITLE = os.environ.get('ISSUE_TITLE')
ISSUE_BODY = os.environ.get('ISSUE_BODY', '')

def read_file_content(filepath):
    """Read file content safely"""
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except:
        return None

def write_file_content(filepath, content):
    """Write file content safely"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)

def get_repository_context():
    """Get relevant repository files for context"""
    context = {}

    # Key files to provide context
    files_to_read = [
        'README.md',
        'Dockerfile',
        'Dockerfile.rhel9',
        'docker-compose-demo.yml',
        '.github/renovate.json',
        '.github/AUTOMATION.md'
    ]

    for filepath in files_to_read:
        content = read_file_content(filepath)
        if content:
            context[filepath] = content

    return context

def build_implementation_prompt(issue_title, issue_body, repo_context):
    """Build the Claude prompt for feature implementation"""

    context_str = "\n\n".join([
        f"### {filepath}\n```\n{content[:2000]}...\n```"
        if len(content) > 2000 else f"### {filepath}\n```\n{content}\n```"
        for filepath, content in repo_context.items()
    ])

    prompt = f"""You are an expert DevOps engineer working on the geoserver-docker-rhel repository.

**Repository Context:**
This is an enterprise fork of GeoServer Docker using RHEL9/UBI9 base images.
Key focus areas: security, stability, enterprise hardening, automated CI/CD.

**Current Repository Files:**
{context_str}

**Feature Request:**
Title: {issue_title}
Description: {issue_body}

**Your Task:**
Analyze the feature request and implement the necessary changes.

**Guidelines:**
1. Maintain security and enterprise best practices
2. Follow existing code patterns and conventions
3. Update documentation if needed
4. Ensure changes are compatible with RHEL9/UBI9
5. Keep Docker images optimized and secure

**Response Format:**
Provide your implementation in this exact JSON format:

{{
  "analysis": "Brief analysis of what needs to be done",
  "files_to_modify": [
    {{
      "path": "path/to/file",
      "action": "create|modify|delete",
      "content": "full file content (for create/modify)",
      "reason": "why this change is needed"
    }}
  ],
  "testing_notes": "How to test these changes",
  "documentation_updates": "What documentation needs updating"
}}

**Important:**
- Provide COMPLETE file contents, not diffs
- Use proper formatting and indentation
- Follow repository conventions
- Include error handling
- Add appropriate comments
"""

    return prompt

def apply_changes(changes_json):
    """Apply the changes suggested by Claude"""
    import json

    try:
        changes = json.loads(changes_json)
    except:
        print("Error: Could not parse Claude response as JSON")
        return False

    print(f"Analysis: {changes.get('analysis', 'N/A')}")
    print(f"\nApplying {len(changes.get('files_to_modify', []))} file changes...")

    for file_change in changes.get('files_to_modify', []):
        filepath = file_change['path']
        action = file_change['action']
        content = file_change.get('content', '')
        reason = file_change.get('reason', '')

        print(f"\n  {action.upper()}: {filepath}")
        print(f"  Reason: {reason}")

        if action == 'create' or action == 'modify':
            write_file_content(filepath, content)
            subprocess.run(['git', 'add', filepath])
        elif action == 'delete':
            if os.path.exists(filepath):
                os.remove(filepath)
                subprocess.run(['git', 'rm', filepath])

    # Create implementation notes file
    notes = f"""# Implementation Notes

## Analysis
{changes.get('analysis', 'N/A')}

## Testing
{changes.get('testing_notes', 'N/A')}

## Documentation Updates Needed
{changes.get('documentation_updates', 'N/A')}
"""

    write_file_content('/tmp/IMPLEMENTATION_NOTES.md', notes)

    return True

def main():
    """Main execution"""
    if not ANTHROPIC_API_KEY:
        print("Error: ANTHROPIC_API_KEY not set")
        sys.exit(1)

    print(f"Starting Claude implementation for issue #{ISSUE_NUMBER}")
    print(f"Title: {ISSUE_TITLE}")

    # Initialize Anthropic client
    anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)

    # Get repository context
    print("\nGathering repository context...")
    repo_context = get_repository_context()
    print(f"Loaded {len(repo_context)} context files")

    # Build implementation prompt
    print("\nBuilding implementation prompt...")
    prompt = build_implementation_prompt(ISSUE_TITLE, ISSUE_BODY, repo_context)

    # Call Claude API
    print("\nCalling Claude API for implementation...")
    try:
        message = anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8192,
            temperature=0.2,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        response_text = message.content[0].text
        print("\n✅ Received implementation from Claude")

        # Extract JSON from response (might be wrapped in markdown)
        if "```json" in response_text:
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            response_json = response_text[json_start:json_end].strip()
        elif "```" in response_text:
            json_start = response_text.find("```") + 3
            json_end = response_text.find("```", json_start)
            response_json = response_text[json_start:json_end].strip()
        else:
            response_json = response_text

        # Apply changes
        print("\nApplying changes...")
        if apply_changes(response_json):
            print("\n✅ Implementation completed successfully")

            # Post comment on issue
            if GITHUB_TOKEN:
                github_client = Github(GITHUB_TOKEN)
                repo = github_client.get_repo(f"{REPO_OWNER}/{REPO_NAME}")
                issue = repo.get_issue(ISSUE_NUMBER)

                comment = f"""🤖 **Claude AI Implementation Complete**

I've analyzed your feature request and created the necessary changes.

**Next Steps:**
1. A pull request will be created automatically with the implementation
2. Please review the changes carefully
3. Test the implementation in your environment
4. Merge when ready

See the PR for detailed implementation notes and testing instructions.
"""
                issue.create_comment(comment)
                print("Posted update comment on issue")

        else:
            print("❌ Error applying changes")
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
