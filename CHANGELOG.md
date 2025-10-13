# Changelog

All notable changes to devops-mcp-server will be documented in this file.

## [0.1.0] - 2025-10-13

### 🎉 Initial Release

#### 🐳 Docker Support (12 tools)
- **Docker Compose Management**
  - Start/stop services with `docker_compose_up` and `docker_compose_down`
  - View logs with `docker_compose_logs`
  - Check service status with `docker_compose_ps`
  - Restart services with `docker_compose_restart`

- **Container Management**
  - List containers with `docker_ps`
  - View container logs with `docker_logs`
  - Start/stop/restart containers
  - Inspect container details with `docker_inspect`
  - Monitor resource usage with `docker_stats`

#### 📊 Process Monitoring (3 tools)
- Check service status by name
- Get system information (memory, disk, uptime)
- List ports in use

#### ✨ Features
- Natural language interaction through MCP protocol
- Auto-discovery of tools from project structure
- Complete documentation and usage examples
- Docker deployment ready (Dockerfile + docker-compose.yml)
- Production-ready error handling

**Total: 15 DevOps tools**
