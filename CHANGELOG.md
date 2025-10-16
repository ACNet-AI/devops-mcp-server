# Changelog

All notable changes to devops-mcp-server will be documented in this file.

## [0.3.2] - 2025-10-16

### 🔧 Code Quality & Refactoring

#### Architecture Improvements
- **Renamed deployment tools** from MCP-specific to universal
  - `clone_mcp_server()` → `clone_from_git()` (generic for any project)
  - `install_mcp_dependencies()` → `install_dependencies()` (auto-detect project type)
  - Updated all documentation to reflect universal nature
- **File organization**: `mcp_deploy.py` → `deploy.py` (better naming)

#### Code Quality Fixes
- ✅ Fixed all 261 linter errors using `ruff`
- ✅ Formatted 13 files with consistent style
- ✅ Updated type annotations to modern Python 3.10+ syntax (`X | None`)
- ✅ Removed unused imports and trailing whitespace
- ✅ Cleaned up blank lines and code formatting

#### Design Philosophy
- **Generic-first approach**: Tools work for any application type (web servers, databases, MCP servers)
- **Smart detection**: Auto-detect project type and use appropriate package managers
- **No backward compatibility burden**: Clean API without legacy aliases

**Result**: Zero linter errors, production-ready code quality! 🎉

## [0.3.0] - 2025-10-16

### 🚀 Major Update: Multi-Platform Deployment Support

#### 📦 Universal Deployment System (8 tools) - Generic, not MCP-specific

**Architecture Change**: Renamed from "MCP deployment" to "Universal deployment"
- These tools work for **any application type** (web servers, APIs, databases, MCP servers)
- Generic naming reflects their true nature

**Generic Deployment Tools:**
- `clone_from_git` - Clone any Git repo (GitHub/GitLab/Gitea/Bitbucket)
- `deploy_from_docker` - Deploy any containerized app (Nginx, PostgreSQL, MCP servers)
- `deploy_from_pypi` - Install any Python package (FastAPI, Django, MCP servers)
- `deploy_from_npm` - Install any Node.js package (Express, Next.js, MCP servers)
- `deploy_from_local` - Deploy from local directory (any project type)
- `install_dependencies` - Auto-detect project type and install deps
- `deploy_mcp_server` - High-level MCP-specific automation workflow
- `check_mcp_server_health` - MCP-specific health checking

**Key improvements:**
- **Generic-first design**: Don't limit deployment to MCP servers
- Support for multiple deployment sources (Git, Docker, PyPI, NPM, local)
- Flexible Git options (branch, shallow clone, SSH)
- Docker image deployment with port/volume mapping
- Package manager integration (PyPI, NPM)
- Local development workflow (symlink support)
- Auto-detect project type and dependencies

#### 🚂 PaaS Platform Integration (22 tools)

**Railway Deployment (8 tools)**
- `railway_login` - Authenticate with Railway
- `railway_init` - Initialize new Railway project
- `railway_link` - Link to existing Railway project
- `railway_deploy` - Deploy application to Railway
- `railway_status` - Check deployment status
- `railway_logs` - View application logs
- `railway_env_set` - Set environment variables
- `railway_env_list` - List environment variables

**Render Deployment (6 tools)**
- `render_login` - Authenticate with Render
- `render_create_service` - Create new Render service
- `render_deploy` - Deploy or redeploy service
- `render_logs` - View service logs
- `render_env_set` - Set environment variables
- `render_list_services` - List all services

**Fly.io Deployment (8 tools)**
- `flyio_auth_login` - Authenticate with Fly.io
- `flyio_launch` - Initialize new Fly.io application
- `flyio_deploy` - Deploy application to Fly.io
- `flyio_status` - Check application status
- `flyio_logs` - View application logs
- `flyio_scale` - Scale instances or VM size
- `flyio_secrets_set` - Set secrets (environment variables)
- `flyio_secrets_list` - List all secrets

#### 📦 Container Registry Operations (7 tools)

**Docker Hub Integration**
- `docker_login` - Login to Docker Hub or private registry
- `docker_build_image` - Build Docker image from Dockerfile
- `docker_tag_image` - Tag image with new name/version
- `docker_push_image` - Push image to Docker Hub
- `docker_build_and_push` - Build and push in one command (multi-platform support)
- `docker_list_local_images` - List local Docker images
- `docker_remove_image` - Remove local Docker image

### 💡 New Capabilities

- **One-Command Deployment**: Deploy to Railway, Render, or Fly.io through conversation
- **Multi-Platform Support**: Build and push AMD64/ARM64 images
- **Complete CI/CD**: From code to production in minutes
- **Environment Management**: Set secrets and variables across all platforms
- **Deployment Monitoring**: Check status and view logs for all deployments

### 📊 Statistics

**Total: 52 DevOps tools** (19 existing + 33 new)
- Docker & Compose: 12 tools
- Process Monitoring: 3 tools
- **Universal Deployment: 8 tools** (generic for any app type)
- Railway: 8 tools
- Render: 6 tools
- Fly.io: 8 tools
- Docker Registry: 7 tools

### 📚 Documentation

- Updated README with PaaS deployment examples
- Added usage examples for all new tools
- Enhanced project structure documentation

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
