# Claude AI Agent Setup Guide

🤖 This guide will help you set up Claude AI to automatically review PRs and implement features for your geoserver-docker-rhel repository.

## 📋 What You'll Get

Once configured, Claude will automatically:
- ✅ Review every pull request for security, quality, and best practices
- ✅ Auto-approve safe dependency updates (Renovate PRs)
- ✅ Provide detailed feedback on code changes
- ✅ Implement features from GitHub issues (when labeled)
- ✅ Check Docker and GeoServer-specific concerns

## 🚀 Quick Setup (5 minutes)

### Step 1: Get Your Claude API Key

1. **Visit Anthropic Console**
   - Go to: https://console.anthropic.com/

2. **Sign up or Log in**
   - Create an account if you don't have one
   - You'll get $5 in free credits to start

3. **Create API Key**
   - Click on "API Keys" in the left sidebar
   - Click "Create Key"
   - Name it: `geoserver-docker-rhel-ci`
   - Copy the key (starts with `sk-ant-`)
   - **⚠️ Save it securely - you won't see it again!**

4. **Add Credits (Optional)**
   - Add payment method for ongoing use
   - Typical cost: $0.30-3 per PR review
   - Expected monthly cost: $5-15 for this repo

### Step 2: Add API Key to GitHub

1. **Go to Repository Settings**
   ```
   https://github.com/drengskapur/geoserver-docker-rhel/settings/secrets/actions
   ```

2. **Create New Secret**
   - Click "New repository secret"
   - Name: `ANTHROPIC_API_KEY`
   - Value: Paste your Claude API key
   - Click "Add secret"

### Step 3: Enable Workflow Permissions

1. **Go to Actions Settings**
   ```
   Settings → Actions → General → Workflow permissions
   ```

2. **Set Permissions**
   - ✅ Select "Read and write permissions"
   - ✅ Check "Allow GitHub Actions to create and approve pull requests"
   - Click "Save"

### Step 4: Done! 🎉

The Claude agent is now active and will automatically review the next PR.

## 📖 How to Use

### Automatic PR Reviews

Claude will automatically review every PR:

```
1. Developer or Renovate opens a PR
     ↓
2. Claude analyzes the changes
     ↓
3. Claude posts detailed review with:
   - Security analysis
   - Code quality feedback
   - Docker/GeoServer-specific concerns
   - Recommendation (APPROVE/REQUEST_CHANGES/COMMENT)
     ↓
4. If safe and labeled 'automerge', auto-approves
```

**Example PR Comment from Claude:**

```markdown
## ✅ Claude AI Code Review

### Security Analysis
No security concerns detected. This dependency update patches CVE-2025-XXXXX.

### Code Quality
Changes follow repository standards. Updated version is stable (released 7 days ago).

### GeoServer/Docker Specific
Compatible with current GeoServer 2.27.2. No breaking changes in this version.

### Recommendation
APPROVE

### Summary
Safe dependency update. All tests passing. Recommended for auto-merge.
```

### Manual Claude Commands

**In PR Comments:**
```markdown
@claude review security implications of this change
@claude check if this is compatible with GeoServer 2.27.x
@claude suggest improvements for Docker optimization
```

### Feature Implementation from Issues

**Create an issue, then add label:**

```markdown
Title: Add health check endpoint to Dockerfile

Description:
We need a proper health check endpoint for the GeoServer container
that checks if GeoServer is responding and ready to serve requests.

Labels: [claude-implement]
```

Claude will:
1. Read the issue
2. Analyze the codebase
3. Implement the feature
4. Create a PR with the changes
5. Add testing notes

## 🎯 Configuration

### Customize Review Focus

Edit `.github/workflows/claude-pr-agent.yml` to adjust review priorities:

```yaml
# Current focus areas (automatically detected):
- Security vulnerabilities (CVEs)
- Docker best practices
- GeoServer configuration
- Dependency safety
- RHEL9/UBI9 compatibility
```

### Add Custom Review Rules

Create `.github/claude-config.yml`:

```yaml
review_rules:
  # Always flag these for manual review
  require_human_review:
    - path: "Dockerfile*"
      reason: "Critical security config"
    - path: ".github/workflows/*"
      reason: "CI/CD changes"

  # Auto-approve these if tests pass
  auto_approve:
    - labels: ["dependencies", "automerge"]
      conditions:
        - "All tests passing"
        - "No security issues"
        - "Renovate bot author"

  # Custom focus areas by file type
  focus_by_file:
    "Dockerfile*":
      - "Multi-stage build optimization"
      - "Security hardening (non-root user)"
      - "UBI9 enterprise compatibility"
    "*.yml":
      - "Secrets handling"
      - "Pinned action versions"
```

## 💰 Cost Estimation

Based on typical usage for this repository:

| Activity | Frequency | Cost per | Monthly Cost |
|----------|-----------|----------|--------------|
| **PR Reviews** | ~8-12/month | $0.30-1.50 | $2.40-18 |
| **Feature Implementation** | 1-2/month | $1-3 | $1-6 |
| **Re-reviews (iterations)** | 2-3/month | $0.30 | $0.60-0.90 |
| **Total** | | | **$5-25/month** |

**Free tier:** $5 in credits = ~5-16 PR reviews

**Cost optimization tips:**
- Claude only runs on PRs (not every commit)
- Reviews are cached (re-reviews are cheaper)
- Implementation feature is opt-in (add label to use)

## 🔍 Monitoring

### View Claude Activity

```bash
# Check recent workflow runs
gh run list --workflow=claude-pr-agent.yml

# View specific run
gh run view <run-id>

# Check API usage
# Visit: https://console.anthropic.com/settings/usage
```

### Sample Workflow Output

```
✅ Claude PR Agent
├── PR #42: chore(deps): update trivy-action
│   ├── Fetching PR diff... ✓
│   ├── Calling Claude API... ✓
│   ├── Security Analysis: No issues
│   ├── Recommendation: APPROVE
│   └── Posted review ✓
└── Auto-approved for merge
```

## 🛡️ Security & Privacy

**What Claude Can See:**
- ✅ PR diffs (code changes only)
- ✅ Repository README and key files
- ✅ Issue descriptions (when implementing)

**What Claude CANNOT See:**
- ❌ Your git history
- ❌ GitHub secrets
- ❌ Private repository data (unless you configure it)
- ❌ Other private repositories

**Data Retention:**
- Anthropic: 30 days (then deleted)
- GitHub Actions logs: 90 days
- Your repo: No Claude data stored

## 🐛 Troubleshooting

### Claude Not Reviewing PRs

**Check:**
1. API key is set correctly: `Settings → Secrets → ANTHROPIC_API_KEY`
2. Workflow permissions enabled (Step 3 above)
3. Check workflow run logs: `Actions → Claude PR Agent`

**Common fixes:**
```bash
# Test API key locally
export ANTHROPIC_API_KEY="your-key"
python3 -c "from anthropic import Anthropic; print(Anthropic(api_key='$ANTHROPIC_API_KEY').messages.create(model='claude-sonnet-4-20250514', max_tokens=10, messages=[{'role':'user','content':'test'}]))"
```

### API Rate Limits

If you hit rate limits:
1. Claude has generous rate limits (50 requests/min)
2. This repo typically makes 1-2 requests per PR
3. If needed, add delays in workflow

### Review Quality Issues

If Claude's reviews aren't helpful:
1. Check the diff size (very large PRs may need chunking)
2. Adjust focus areas in workflow config
3. Provide more context in PR descriptions

## 📚 Advanced Usage

### Batch Review Multiple PRs

```bash
# Label multiple PRs for re-review
gh pr list --label "needs-claude-review" | while read pr; do
  gh pr comment $pr --body "@claude review this"
done
```

### Custom Implementation Prompts

When creating issues for Claude to implement:

```markdown
Title: [Feature] Add monitoring metrics

Description:
**Context:** We need Prometheus metrics for GeoServer container

**Requirements:**
- Expose metrics on port 9090
- Include JVM metrics
- Include GeoServer-specific metrics
- Add to docker-compose for testing

**Constraints:**
- Must work with UBI9 base image
- No additional dependencies
- Follow enterprise security practices

Labels: [claude-implement, monitoring]
```

## 🔄 Updates

The Claude agent is automatically updated when you push changes to the workflow files.

**To update:**
```bash
# Pull latest changes
git pull origin fork

# Workflow files are at:
# - .github/workflows/claude-pr-agent.yml
# - .github/scripts/claude_review.py
# - .github/scripts/claude_implement.py
```

## 💡 Tips

1. **Be specific in PR descriptions** - helps Claude provide better reviews
2. **Use labels effectively** - `automerge`, `manual-review`, `claude-implement`
3. **Review Claude's feedback** - Claude can make mistakes, always verify
4. **Iterate with @claude** - Have a conversation in PR comments
5. **Monitor costs** - Check your Anthropic console monthly

## 🆘 Support

**Issues with Claude Agent:**
- Check logs: `Actions → Claude PR Agent`
- Review setup: Follow steps 1-3 above
- Test API key: See troubleshooting section

**Issues with Anthropic API:**
- Visit: https://support.anthropic.com/
- Check status: https://status.anthropic.com/

**Feature Requests:**
- Open an issue with label: `claude-enhancement`

## 🎓 Learn More

- **Claude API Docs**: https://docs.anthropic.com/
- **Best Practices**: https://www.anthropic.com/engineering/claude-code-best-practices
- **Model Details**: https://www.anthropic.com/claude

---

## ✅ Quick Checklist

Before first use, make sure you:
- [ ] Created Anthropic API account
- [ ] Generated API key
- [ ] Added `ANTHROPIC_API_KEY` to GitHub Secrets
- [ ] Enabled workflow permissions (read/write + PR creation)
- [ ] Pushed the workflow files to your repo
- [ ] Tested with a sample PR

**Ready to go!** Open a test PR and watch Claude review it automatically. 🚀
