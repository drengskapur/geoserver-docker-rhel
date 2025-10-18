# Automated PR Management

This repository uses AI-powered automation to handle dependency updates and security patches automatically.

## 🤖 What's Automated

### Renovate Bot
Automatically creates PRs for:
- **Security updates** (CRITICAL/HIGH) - Auto-merged immediately after tests pass
- **Minor/patch updates** - Auto-merged after 3 days stability period
- **GitHub Actions updates** - Auto-merged for minor/patch versions
- **Docker image updates** - Auto-merged for digest/minor/patch versions

### Auto-Merge Workflow
GitHub Actions workflow (`.github/workflows/renovate-automerge.yml`) that:
1. Detects Renovate PRs
2. Waits for all status checks to pass
3. Auto-approves safe updates
4. Auto-merges PRs with `automerge` label
5. Flags major updates for manual review

## 📋 GitHub Repository Setup

To enable auto-merge, configure these settings in your repository:

### 1. Enable Auto-Merge Feature
**Settings → General → Pull Requests**
- ✅ Check "Allow auto-merge"

### 2. Branch Protection (Optional but Recommended)
**Settings → Branches → Add rule for `fork` and `master`**

Recommended settings:
- ✅ Require status checks to pass before merging
- ✅ Require branches to be up to date before merging
- ✅ Required status checks:
  - `Trivy Security Scan`
  - `Scan Published Images` (if applicable)

**For auto-merge without approvals:**
- Under "Allow specified actors to bypass required pull requests"
- Add: `renovate[bot]` and `github-actions[bot]`

### 3. GitHub Actions Permissions
**Settings → Actions → General → Workflow permissions**
- ✅ Select "Read and write permissions"
- ✅ Check "Allow GitHub Actions to create and approve pull requests"

## 🔄 How It Works

### Critical Security Updates
```
Renovate detects CVE
    ↓
Creates PR with labels: security, critical, automerge
    ↓
Security scans run
    ↓
Auto-approve workflow waits for checks
    ↓
✅ Auto-approved and merged immediately
```

### Minor/Patch Updates
```
Renovate detects update
    ↓
Creates PR with label: automerge, minor-patch
    ↓
Waits 3 days for stability
    ↓
Tests run
    ↓
✅ Auto-approved and merged
```

### Major Updates
```
Renovate detects major version
    ↓
Creates PR with labels: major-update, manual-review
    ↓
Bot adds comment: "Manual review required"
    ↓
⚠️ Waits for human review and merge
```

## 🎯 Auto-Merge Rules

| Update Type | Auto-Merge | Stability Period | Example |
|-------------|------------|------------------|---------|
| **Security (Critical)** | ✅ Yes | 0 days | CVE fixes |
| **Security (High)** | ✅ Yes | 0 days | Security patches |
| **Minor/Patch** | ✅ Yes | 3 days | 1.2.3 → 1.2.4 |
| **GitHub Actions (minor)** | ✅ Yes | 3 days | v3.1 → v3.2 |
| **Docker digest** | ✅ Yes | 3 days | sha256:abc → sha256:xyz |
| **Major versions** | ❌ No | 14 days | 1.x → 2.x |
| **GeoServer updates** | ❌ No | 14 days | Needs testing |
| **Iron Bank images** | ❌ No | 7 days | Enterprise critical |

## 🔍 Monitoring

### Check Auto-Merge Status
```bash
# List recent Renovate PRs
gh pr list --author renovate[bot]

# View auto-merge workflow runs
gh run list --workflow=renovate-automerge.yml

# Check a specific PR
gh pr view <PR_NUMBER>
```

### View Automation Logs
Navigate to: **Actions → Renovate Auto-Merge → Select run**

### Disable Auto-Merge Temporarily
Comment on any Renovate PR:
```
@renovate ignore
```

## 🛡️ Safety Features

1. **Status checks required** - Won't merge if tests fail
2. **Stability period** - Waits for package to stabilize
3. **Label-based control** - Only merges PRs with `automerge` label
4. **Major version protection** - Always requires manual review
5. **Manual override** - Can always close/ignore PRs manually

## 📊 Advanced Configuration

### Customize Auto-Merge Rules
Edit `.github/renovate.json` to modify:
- `stabilityDays` - How long to wait before merging
- `automerge` - Enable/disable for specific packages
- `labels` - Control which PRs get auto-merged

### Disable Auto-Merge for Specific Packages
Add to `.github/renovate.json`:
```json
{
  "packageRules": [
    {
      "matchPackageNames": ["package-name"],
      "automerge": false
    }
  ]
}
```

## 🤝 Alternative: CodeRabbit AI

For even more advanced automation, consider **CodeRabbit**:
- AI-powered code review
- Intelligent merge decisions
- Bug detection
- $12-24/month per developer

Install: https://www.coderabbit.ai/

## 📞 Support

**If automation fails:**
1. Check workflow logs in Actions tab
2. Verify repository settings match requirements above
3. Ensure GitHub Actions has proper permissions
4. PRs can always be merged manually if needed

**To pause automation:**
- Disable the workflow: `.github/workflows/renovate-automerge.yml`
- Or set `"automerge": false` in `.github/renovate.json`
