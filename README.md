# 🚀 DevOps MCP Server

Universal DevOps automation through conversation. Deploy, monitor, and manage applications using natural language with AI assistants.

## ✨ Features

### 🐳 Docker & Docker Compose
- **Container Management** - Start, stop, restart, and monitor containers
- **Compose Operations** - Manage multi-container applications  
- **Log Viewing** - Stream and search container logs
- **Resource Monitoring** - Track CPU, memory, and network usage

### 📊 Process Monitoring
- **Service Status** - Check if services are running
- **System Info** - View memory, disk, and CPU usage
- **Port Management** - List and check port usage

### 🚂 PaaS Platform Deployment
- **Railway** - Deploy to Railway with one command
- **Render** - Deploy web services and databases to Render
- **Fly.io** - Deploy to edge locations worldwide

### 📦 Container Registry
- **Docker Hub** - Build, tag, and push images to Docker Hub
- **Multi-platform builds** - Build for AMD64 and ARM64

### 🎯 Available Tools

#### Docker Compose (5 tools)
- `docker_compose_up` - Start services
- `docker_compose_down` - Stop and remove services
- `docker_compose_logs` - View service logs
- `docker_compose_ps` - List service status
- `docker_compose_restart` - Restart services

#### Docker Containers (7 tools)
- `docker_ps` - List containers
- `docker_logs` - View container logs
- `docker_start` - Start a container
- `docker_stop` - Stop a container
- `docker_restart` - Restart a container
- `docker_inspect` - Get container details
- `docker_stats` - View resource usage

#### Process Monitoring (3 tools)
- `check_service_status` - Check if a service is running
- `get_system_info` - Get system information
- `list_ports_in_use` - List ports in use

#### Universal Deployment (8 tools) - Works for any application
- `clone_from_git` - Clone from Git (GitHub/GitLab/Gitea/Bitbucket)
- `deploy_from_docker` - Deploy from Docker image (any containerized app)
- `deploy_from_pypi` - Install from PyPI (Python applications)
- `deploy_from_npm` - Install from NPM (Node.js applications)
- `deploy_from_local` - Deploy from local directory
- `install_dependencies` - Auto-detect and install dependencies
- `deploy_mcp_server` - Automated MCP deployment workflow
- `check_mcp_server_health` - Verify MCP server health

#### Railway Deployment (8 tools) 🆕
- `railway_login` - Authenticate with Railway
- `railway_init` - Initialize new project
- `railway_link` - Link to existing project
- `railway_deploy` - Deploy to Railway
- `railway_status` - Check deployment status
- `railway_logs` - View application logs
- `railway_env_set` - Set environment variables
- `railway_env_list` - List environment variables

#### Render Deployment (6 tools) 🆕
- `render_login` - Authenticate with Render
- `render_create_service` - Create new service
- `render_deploy` - Deploy or redeploy service
- `render_logs` - View service logs
- `render_env_set` - Set environment variables
- `render_list_services` - List all services

#### Fly.io Deployment (8 tools) 🆕
- `flyio_auth_login` - Authenticate with Fly.io
- `flyio_launch` - Initialize new application
- `flyio_deploy` - Deploy application
- `flyio_status` - Check application status
- `flyio_logs` - View application logs
- `flyio_scale` - Scale instances or VM size
- `flyio_secrets_set` - Set secrets (env vars)
- `flyio_secrets_list` - List all secrets

#### Docker Registry (7 tools) 🆕
- `docker_login` - Login to Docker Hub or registry
- `docker_build_image` - Build image from Dockerfile
- `docker_tag_image` - Tag image with new name
- `docker_push_image` - Push image to registry
- `docker_build_and_push` - Build and push in one command
- `docker_list_local_images` - List local images
- `docker_remove_image` - Remove local image

**Total: 52 DevOps tools ready to use!**

**Key Architecture:**
- 🎯 **Generic First**: Most tools work for any application (web servers, databases, MCP)
- 🔌 **Smart Detection**: Auto-detect project type and use appropriate tools
- 🌍 **Platform Agnostic**: Deploy anywhere (local, remote, PaaS, containers)

## Quick Start

```bash
# Install dependencies
uv sync

# Start server
uv run python server.py
```

## Configuration

Add to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "devops-mcp-server": {
      "command": "uv",
      "args": ["run", "python", "server.py"],
      "cwd": "/path/to/devops-mcp-server"
    }
  }
}
```

## Project Structure

```
devops-mcp-server/
├── config.yaml          # Server configuration
├── pyproject.toml       # Python project configuration
├── server.py            # Server entry file
├── README.md            # Documentation
├── CHANGELOG.md         # Version change log
├── .env                 # Environment variables configuration
├── .gitignore           # Git ignore file
├── Dockerfile           # Docker container configuration
├── .dockerignore        # Docker build ignore file
├── docker-compose.yml   # Docker Compose orchestration
├── tools/               # Tools implementation directory
├── resources/           # Resources implementation directory
└── prompts/             # Prompt template directory
```

## 💬 Usage Examples

Once connected to Claude Desktop or another MCP client, you can interact naturally:

**Container Management:**
- "Start my docker compose services"
- "Show me the logs for my-app container"
- "What containers are currently running?"
- "Restart the database container"

**Monitoring:**
- "Is nginx running?"
- "What's using port 8080?"
- "Show me system resource usage"

**Docker Compose:**
- "Bring up my application stack"
- "Show me the status of all services"
- "View the logs for the web service"

**PaaS Deployment:**
- "Deploy my app to Railway"
- "Check the status of my Railway deployment"
- "Push this Docker image to Docker Hub"
- "Deploy my MCP server to Fly.io"

**Container Registry:**
- "Build and push my-app:v1.0 to Docker Hub"
- "Show me all my local Docker images"
- "Tag my image for production"

## 🛠️ Development

The server automatically discovers tools from the `tools/` directory structure:

```
tools/
├── docker/
│   ├── compose.py      # Docker Compose tools
│   └── container.py    # Container management tools
├── process/
│   └── monitor.py      # Process monitoring tools
├── deployment/
│   └── mcp_deploy.py   # MCP server deployment
├── paas/
│   ├── railway.py      # Railway deployment
│   ├── render.py       # Render deployment
│   └── flyio.py        # Fly.io deployment
└── registry/
    └── dockerhub.py    # Docker Hub operations
```

To add new tools, create Python files in the appropriate directory with functions decorated with `@tool()`

## Deployment

### Docker Deployment (Recommended)

#### Using docker-compose (Easiest)

```bash
# 1. Start the service
docker-compose up -d

# 2. View logs
docker-compose logs -f

# 3. Stop the service
docker-compose down
```

#### Using Docker commands

```bash
# Build image
docker build -t devops-mcp-server .

# Run container
docker run -d \
  --name devops-mcp-server \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  devops-mcp-server
```

### Local Development

```bash
# Install dependencies
uv sync

# Run server
uv run python server.py
```

### Production Deployment

For production deployment, ensure you:
1. Configure environment variables in `.env`
2. Set up proper logging and monitoring
3. Use `restart: unless-stopped` in docker-compose (already configured)
4. Mount persistent volumes for data

### Health Check

```bash
# Check if container is running
docker ps | grep devops-mcp-server

# View container logs
docker logs devops-mcp-server

# Check service status with docker-compose
docker-compose ps
```

## Advanced Usage

For advanced features and examples, see the [examples directory](../examples/) in the mcp-factory repository.

---

*Generated by [MCP Factory](https://github.com/ACNet-AI/mcp-factory)*