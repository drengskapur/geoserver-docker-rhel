# Security Policy

## About This Fork

This is a **fork** of the official GeoServer Docker project with focus on **enterprise RHEL9 deployments**. Security considerations include both upstream GeoServer security and enterprise-specific concerns.

## Supported Versions

| Version | Supported | Notes |
|---------|-----------|-------|
| `latest` | ✅ | Current RHEL9-based release |
| `2.25.x` | ✅ | Specific GeoServer versions |
| `main` | ⚠️ | Development - use with caution |

## Reporting Vulnerabilities

### For This Fork (RHEL9/Enterprise specific)

- **GitHub Security**: Use the [Security tab](https://github.com/drengskapur/geoserver-docker-rhel/security) for private reporting
- **Email**: Security issues affecting enterprise deployments
- **Response time**: We aim to respond within 48 hours

### For Core GeoServer Issues

- **Upstream first**: Report core GeoServer vulnerabilities to the [main project](https://github.com/geoserver/docker/security)
- **Coordination**: We'll coordinate with upstream for fixes affecting both projects

## Security Considerations

### Enterprise Environment Factors

- **Base Images**: Using hardened RHEL9/UBI9 base images
- **Registry1**: Enterprise image registry with additional security scanning
- **Network Policies**: Consider firewall and network segmentation
- **Secrets Management**: Never commit credentials or certificates

### Container Security

- **Non-root execution**: Run containers with `--user` when possible
- **Read-only filesystems**: Use `--read-only` with appropriate tmpfs mounts
- **Resource limits**: Set memory and CPU limits
- **Network isolation**: Use Docker networks for service isolation

### Example Secure Deployment

```bash
docker run -d \
  --name geoserver \
  --user 1001:1001 \
  --read-only \
  --tmpfs /tmp \
  --tmpfs /opt/geoserver_data/logs \
  -p 127.0.0.1:8080:8080 \
  -v geoserver-data:/opt/geoserver_data:Z \
  -e JAVA_OPTS="-Xms2G -Xmx4G" \
  drengskapur/geoserver:latest
```

## Security Updates

### Automated Updates

- **Base images**: Automatically rebuilt when RHEL9/UBI9 updates
- **Upstream sync**: Daily sync brings in upstream security fixes
- **CI scanning**: Automated vulnerability scanning in CI/CD pipeline

### Manual Updates

- **Critical CVEs**: Emergency rebuilds for critical vulnerabilities
- **Security patches**: Regular security patch incorporation
- **Notifications**: Security advisories posted as GitHub releases

## Best Practices

### Deployment

- **Change default passwords** immediately
- **Use HTTPS** with proper certificates
- **Regular updates** to latest secure versions
- **Monitor logs** for suspicious activity
- **Backup configurations** securely

### Development

- **Secrets scanning** in CI/CD
- **Dependency scanning** for known vulnerabilities
- **Static analysis** of Dockerfiles
- **Regular base image updates**

## Responsible Disclosure

1. **Do not** disclose vulnerabilities publicly until fixes are available
2. **Provide** clear reproduction steps and impact assessment
3. **Allow** reasonable time for fixes (typically 90 days)
4. **Coordinate** with both this fork and upstream project when applicable

## Security Contacts

- **Fork maintainer**: [@drengskapur](https://github.com/drengskapur)
- **Upstream project**: [GeoServer Security](https://github.com/geoserver/docker/security)

---

**Note**: This fork inherits security policies from the upstream GeoServer project while adding enterprise-specific security considerations.
