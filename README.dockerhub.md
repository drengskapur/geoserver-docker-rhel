# GeoServer Enterprise Docker Image (RHEL9/UBI9)

[![Docker Pulls](https://img.shields.io/docker/pulls/drengskapur/geoserver)](https://hub.docker.com/r/drengskapur/geoserver)
[![Docker Image Size](https://img.shields.io/docker/image-size/drengskapur/geoserver/latest-ubi9)](https://hub.docker.com/r/drengskapur/geoserver)
[![License](https://img.shields.io/badge/license-GPL--2.0-blue)](LICENSE)

> Enterprise-hardened GeoServer Docker image with RHEL9/UBI9 base for production deployments

## 🏢 Enterprise Features

- **Hardened Base**: Red Hat UBI9 from Iron Bank registry
- **Automated Updates**: Synced with upstream GeoServer releases

## Quick Start

Latest enterprise build

```bash
docker run -d -p 8080:8080 drengskapur/geoserver:latest-ubi9
```

Specific GeoServer version

```bash
docker run -d -p 8080:8080 drengskapur/geoserver:2.27.0-ubi9
```

**Access**: <http://localhost:8080/geoserver>  
**Default credentials**: `admin` / `geoserver`

📖 **Documentation**: [GeoServer User Manual](https://docs.geoserver.org/latest/en/user/)

## 🏷️ Tags

All tags include `-ubi9` suffix for enterprise identification:

- `latest-ubi9` - Latest stable release (RHEL9/UBI9)
- `2.27.0-ubi9` - Specific GeoServer version  
- `edge-ubi9` - Development build from fork branch
- `fork-{sha}-ubi9` - Specific commit builds

## Environment Variables

| Variable             | Default               | Description              |
| -------------------- | --------------------- | ------------------------ |
| `GEOSERVER_DATA_DIR` | `/opt/geoserver_data` | GeoServer data directory |
| `JAVA_OPTS`          | `-Xms1G -Xmx2G`       | JVM memory settings      |
| `EXTRA_JAVA_OPTS`    |                       | Additional JVM options   |

## Volumes

| Path                    | Description              |
| ----------------------- | ------------------------ |
| `/opt/geoserver_data`   | GeoServer data directory |
| `/opt/additional_libs`  | Additional plugins       |
| `/opt/additional_fonts` | Custom fonts             |

## Production Example

```bash
docker run -d \
  --name geoserver-enterprise \
  -p 8080:8080 \
  -v geoserver-data:/opt/geoserver_data \
  -v geoserver-libs:/opt/additional_libs \
  -e JAVA_OPTS="-Xms4G -Xmx8G" \
  -e EXTRA_JAVA_OPTS="-XX:+UseG1GC -XX:MaxGCPauseMillis=200" \
  --restart unless-stopped \
  drengskapur/geoserver:latest-ubi9
```

## Docker Compose

```yaml
version: '3.8'
services:
  geoserver:
    image: drengskapur/geoserver:latest-ubi9
    ports:
      - "8080:8080"
    volumes:
      - geoserver-data:/opt/geoserver_data
      - geoserver-libs:/opt/additional_libs
    environment:
      - JAVA_OPTS=-Xms4G -Xmx8G
      - EXTRA_JAVA_OPTS=-XX:+UseG1GC -XX:MaxGCPauseMillis=200
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/geoserver/web"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  geoserver-data:
  geoserver-libs:
```

## 🔒 Security

**⚠️ Change default password immediately**: <http://localhost:8080/geoserver/web>

- Based on hardened Red Hat UBI9 base image
- Regular security updates via automated upstream sync
- Minimal package installation for reduced attack surface
- Enterprise-grade base from Iron Bank registry

For security configuration: [GeoServer Security Guide](https://docs.geoserver.org/latest/en/user/security/index.html)

## 🔄 Automated Updates

This image automatically:

- Syncs with upstream GeoServer releases every 6 hours
- Rebuilds on UBI9 base image updates
- Updates dependencies via Renovate bot
- Maintains enterprise hardening standards

## Links

- **Documentation**: [GeoServer Docs](https://docs.geoserver.org/)
- **Extensions**: [Available Plugins](https://docs.geoserver.org/latest/en/user/extensions/index.html)
- **Source**: [GitHub Repository](https://github.com/drengskapur/geoserver-docker-rhel)
- **Issues**: [Report Issues](https://github.com/drengskapur/geoserver-docker-rhel/issues)

---

**Base**: Red Hat UBI9 | **Java**: OpenJDK 17 | **GeoServer**: Auto-synced | **Architecture**: AMD64, ARM64
