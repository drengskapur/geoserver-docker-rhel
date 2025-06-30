# Contributing to GeoServer Docker RHEL Image

Thank you for your interest in contributing! This is a **fork** of the official GeoServer Docker project with a focus on **enterprise RHEL9-based deployments**.

## About This Fork

This repository provides:

- **RHEL9-based** GeoServer images for enterprise environments
- **Hardened security** configurations
- **Registry1/Iron Bank** base image support
- **Automated upstream sync** with the main GeoServer project

## Quick Start

1. **Fork** this repository
2. **Clone** your fork: `git clone https://github.com/your-username/geoserver-docker-rhel.git`
3. **Create** a feature branch: `git checkout -b feature/your-feature`
4. **Make** your changes (focus on RHEL9/enterprise specific improvements)
5. **Test** your changes
6. **Submit** a pull request

## What to Contribute

### ✅ Good Contributions for This Fork

- **RHEL9/UBI9** specific optimizations
- **Enterprise security** enhancements
- **Performance tuning** for production environments
- **Documentation** for enterprise deployments
- **CI/CD improvements** for this fork's workflow
- **Registry1/Iron Bank** compatibility fixes

### ❌ Avoid These Contributions

- **Core GeoServer features** → Contribute to [upstream](https://github.com/geoserver/docker) instead
- **General Docker improvements** → Better suited for upstream
- **Breaking changes** to compatibility with upstream

## Development

### Prerequisites

- Docker 20.10+
- Access to Registry1 (for RHEL9 builds)
- Git

### Building

```bash
# Build RHEL9 variant (this fork's specialty)
docker build -f Dockerfile.rhel9 -t geoserver:rhel9-dev .

# Build standard variant (inherited from upstream)
docker build -t geoserver:dev .

# Test the build
docker run --rm -p 8080:8080 geoserver:rhel9-dev
```

## Upstream Relationship

- **Automatic sync**: This fork automatically syncs with upstream daily
- **Merge conflicts**: May require manual resolution during sync
- **Feature requests**: Consider if they belong upstream or in this fork

## Guidelines

### Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```text
feat(rhel9): optimize UBI9 base image layers
fix(security): update Registry1 image to patch CVE-2023-xxxx
docs(deploy): add enterprise deployment examples
ci(sync): improve upstream merge conflict handling
```

### Pull Requests

- **Focus**: RHEL9/enterprise specific changes
- **Upstream compatibility**: Ensure changes don't break upstream sync
- **Testing**: Test on RHEL9/enterprise environments when possible

## Issues

### For This Fork

- RHEL9/UBI9 specific issues
- Enterprise deployment problems
- Fork-specific CI/CD issues

### For Upstream

- Core GeoServer functionality
- General Docker improvements
- Feature requests for all users

Report upstream issues at: [geoserver/docker](https://github.com/geoserver/docker/issues)

## Security

- **Enterprise focus**: Security issues may affect enterprise deployments differently
- **Registry1 images**: Report issues with base images to appropriate channels
- **Responsible disclosure**: Follow both this repo's and upstream's security policies

## Questions?

- **Fork-specific**: [GitHub Issues](https://github.com/drengskapur/geoserver-docker-rhel/issues)
- **General GeoServer**: [Upstream Issues](https://github.com/geoserver/docker/issues)
- **Discussions**: [GitHub Discussions](https://github.com/drengskapur/geoserver-docker-rhel/discussions)

---

By contributing, you agree that your contributions will be licensed under the GPL-2.0 License.
