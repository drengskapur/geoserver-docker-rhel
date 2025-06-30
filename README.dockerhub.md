# GeoServer Docker Image

[![Docker Pulls](https://img.shields.io/docker/pulls/drengskapur/geoserver)](https://hub.docker.com/r/drengskapur/geoserver)
[![Docker Image Size](https://img.shields.io/docker/image-size/drengskapur/geoserver/latest)](https://hub.docker.com/r/drengskapur/geoserver)
[![License](https://img.shields.io/badge/license-GPL--2.0-blue)](LICENSE)

> Production-ready GeoServer Docker image with hardened RHEL9 base

## Quick Start

```bash
docker run -d -p 8080:8080 drengskapur/geoserver:latest
```

**Access**: <http://localhost:8080/geoserver>  
**Default credentials**: `admin` / `geoserver`

📖 **Documentation**: [GeoServer User Manual](https://docs.geoserver.org/latest/en/user/)

## Tags

- `latest` - Latest stable release (RHEL9)
- `2.25.x` - Specific GeoServer version
- `main` - Development build

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GEOSERVER_DATA_DIR` | `/opt/geoserver_data` | GeoServer data directory |
| `JAVA_OPTS` | `-Xms1G -Xmx2G` | JVM memory settings |

## Volumes

| Path | Description |
|------|-------------|
| `/opt/geoserver_data` | GeoServer data directory |
| `/opt/additional_libs` | Additional plugins |

## Production Example

```bash
docker run -d \
  --name geoserver \
  -p 8080:8080 \
  -v geoserver-data:/opt/geoserver_data \
  -e JAVA_OPTS="-Xms2G -Xmx4G" \
  drengskapur/geoserver:latest
```

## Docker Compose

```yaml
version: '3.8'
services:
  geoserver:
    image: drengskapur/geoserver:latest
    ports:
      - "8080:8080"
    volumes:
      - geoserver-data:/opt/geoserver_data
    environment:
      - JAVA_OPTS=-Xms2G -Xmx4G

volumes:
  geoserver-data:
```

## Security

**⚠️ Change default password immediately**: <http://localhost:8080/geoserver/web>

For security configuration: [GeoServer Security Guide](https://docs.geoserver.org/latest/en/user/security/index.html)

## Links

- **Documentation**: [GeoServer Docs](https://docs.geoserver.org/)
- **Extensions**: [Available Plugins](https://docs.geoserver.org/latest/en/user/extensions/index.html)
- **Source**: [GitHub Repository](https://github.com/drengskapur/geoserver-docker-rhel)

---

**Base**: Red Hat UBI9 | **Java**: OpenJDK 17 | **GeoServer**: 2.25.x
