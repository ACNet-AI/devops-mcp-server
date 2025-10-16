# Changelog

All notable changes to devops-mcp-server will be documented in this file.

## [0.2.0] - 2025-10-13

### 🚀 New Features

#### 🎯 MCP Server Deployment Automation (4 tools)
- **`clone_mcp_server`** - Clone MCP server repositories from Git
- **`install_mcp_dependencies`** - Install project dependencies (uv/pip)
- **`deploy_mcp_server`** - Complete deployment workflow (clone + install + start)
- **`check_mcp_server_health`** - Verify server is running and healthy

#### 💡 Capabilities
- Deploy any MCP server with one command
- Automated dependency installation
- Docker-compose integration for containerized servers
- Health monitoring for deployed servers
- Support for both local and remote deployments

**Total: 19 DevOps tools** (15 existing + 4 new)

### 📚 Documentation
- Added comprehensive USAGE.md guide
- Updated README with user onboarding
- Fixed linter warnings

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
