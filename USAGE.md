# 📖 DevOps MCP Server - User Guide

Complete guide for using devops-mcp-server with Claude Desktop.

## 🎯 What is this?

**devops-mcp-server** is an MCP (Model Context Protocol) server that lets you manage Docker containers, docker-compose projects, and system processes through natural language conversations with Claude.

Instead of typing commands like `docker ps`, `docker logs`, etc., you can simply ask Claude:
- "Show me running containers"
- "Restart the nginx container"
- "What's using port 8080?"

## 🚀 Quick Start

### Step 1: Get the Project

```bash
# Clone from GitHub
git clone https://github.com/ACNet-AI/devops-mcp-server.git
cd devops-mcp-server
```

### Step 2: Install Dependencies

```bash
# Install uv (if you don't have it)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv sync
```

### Step 3: Configure Claude Desktop

**Locate your config file:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

**Add this configuration:**

```json
{
  "mcpServers": {
    "devops": {
      "command": "uv",
      "args": ["run", "python", "server.py"],
      "cwd": "/absolute/path/to/devops-mcp-server"
    }
  }
}
```

⚠️ **Important**: Replace `/absolute/path/to/devops-mcp-server` with your actual project path!

**Example paths:**
- macOS: `/Users/john/devops-mcp-server`
- Windows: `C:\\Users\\john\\devops-mcp-server`
- Linux: `/home/john/devops-mcp-server`

### Step 4: Restart Claude Desktop

Close and reopen Claude Desktop. The devops-mcp-server will start automatically.

### Step 5: Verify Installation

In Claude, try:
```
You: "List running Docker containers"
Claude: [calls docker_ps tool] → Shows your containers
```

If you see container information, it's working! 🎉

## 💬 How to Use

### Basic Container Management

**List containers:**
```
"Show me all Docker containers"
"What containers are running?"
"List all containers including stopped ones"
```

**View logs:**
```
"Show logs for nginx container"
"View the last 50 lines of web container logs"
"Show me logs from the database container"
```

**Start/Stop/Restart:**
```
"Start the postgres container"
"Stop the redis container"
"Restart my web application"
```

**Container details:**
```
"Show details about the nginx container"
"What's the status of my-app container?"
"Get resource usage for all containers"
```

### Docker Compose Management

**Start services:**
```
"Start my docker-compose services at /path/to/project"
"Bring up the application stack"
"Start services in detached mode"
```

**Check status:**
```
"What's the status of my docker-compose services?"
"Show me which services are running"
```

**View logs:**
```
"Show logs for the web service"
"View all service logs"
```

**Stop services:**
```
"Stop my docker-compose services"
"Bring down the application stack"
```

### System Monitoring

**Check processes:**
```
"Is nginx running?"
"Check if postgres is running"
"What processes are using port 8080?"
```

**System info:**
```
"Show me system resource usage"
"How much memory is available?"
"What's the disk usage?"
```

**Port management:**
```
"What's using port 3000?"
"Show me all ports in use"
"List all listening ports"
```

## 🌐 Managing Remote Servers

### Setup SSH Access

```bash
# 1. Create Docker context for remote server
docker context create production \
  --docker "host=ssh://user@your-server.com"

# 2. Switch to remote context
docker context use production

# 3. Now Claude operates on the remote server!
```

### Remote Management Examples

```
"Show containers on the production server"
"Restart the web service on production"
"View logs from the remote nginx container"
```

### Switch Between Servers

```bash
# List contexts
docker context ls

# Switch to production
docker context use production

# Switch back to local
docker context use default
```

## 🎓 Example Workflows

### Workflow 1: Start Development Environment

```
You: "I want to start my development environment"
Claude: "Where is your project located?"
You: "/Users/me/my-project"
Claude: [executes docker-compose up -d]
      ✅ Services started:
      - web (port 3000)
      - postgres (port 5432)
      - redis (port 6379)
```

### Workflow 2: Troubleshooting

```
You: "My app is not responding, help me debug"
Claude: [checks running containers]
      "I see your web container is running but restarting frequently.
       Let me check the logs..."
      [views container logs]
      "Found the issue: Database connection failed.
       Let me check the database container..."
      [checks postgres container]
      "The postgres container is stopped. Should I start it?"
You: "Yes please"
Claude: [starts postgres container]
      ✅ Database started. Your app should work now.
```

### Workflow 3: Resource Cleanup

```
You: "Clean up unused Docker resources"
Claude: [lists stopped containers]
      "Found 5 stopped containers taking up 1.2GB.
       Delete them?"
You: "Yes"
Claude: [removes containers]
      ✅ Cleaned up 5 containers, freed 1.2GB
```

## 🔧 Advanced Configuration

### Enable Debug Mode

Edit `config.yaml`:
```yaml
transport:
  log_level: DEBUG
```

### Custom Tool Prefix

If you have multiple MCP servers and want to avoid name conflicts, you can add a prefix in `config.yaml`.

### Environment Variables

Create a `.env` file for sensitive information:
```bash
DOCKER_HOST=ssh://user@server.com
DOCKER_CERT_PATH=/path/to/certs
```

## ❓ Troubleshooting

### devops-mcp-server not appearing in Claude

1. **Check config file path**: Ensure you edited the correct `claude_desktop_config.json`
2. **Verify JSON syntax**: Use a JSON validator to check for syntax errors
3. **Check absolute path**: The `cwd` must be an absolute path, not relative
4. **Restart Claude**: Fully quit and restart Claude Desktop

### "Command not found: uv"

Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### "No such file or directory"

1. Check the `cwd` path in your config
2. Make sure the path exists: `ls /path/to/devops-mcp-server`
3. Use absolute paths, not `~` or relative paths

### Docker commands not working

1. **Check Docker is running**: `docker ps`
2. **Check permissions**: Ensure your user can run Docker commands
3. **macOS**: Docker Desktop must be running
4. **Linux**: Your user must be in the `docker` group

### Can't access remote server

1. **Test SSH**: `ssh user@server.com docker ps`
2. **Check Docker context**: `docker context ls`
3. **Verify Docker is installed on remote server**

## 🆘 Getting Help

- **GitHub Issues**: [Report bugs or request features](https://github.com/ACNet-AI/devops-mcp-server/issues)
- **Documentation**: [Full documentation](https://github.com/ACNet-AI/devops-mcp-server/blob/main/README.md)
- **MCP Protocol**: [Learn about MCP](https://modelcontextprotocol.io)

## 🎯 Tips for Best Results

1. **Be specific**: "Restart the web container" is better than "restart something"
2. **Provide paths**: When managing docker-compose, always provide the project path
3. **Use natural language**: Claude understands context, you don't need exact commands
4. **Ask for help**: If something fails, Claude can help troubleshoot

## 🔐 Security Notes

- **Local only by default**: devops-mcp-server runs locally and only you can access it
- **Docker socket access**: The server needs access to Docker socket (`/var/run/docker.sock`)
- **SSH keys**: For remote access, use SSH key authentication, not passwords
- **Network isolation**: By default, operates through stdio, no network exposure

## 📚 What's Next?

After you're comfortable with basic usage:
- Explore all 15 available tools
- Set up remote server management via SSH
- Create your own automation workflows
- Integrate with your CI/CD pipeline

---

**Enjoy managing your infrastructure through conversation!** 🚀

*Generated by [MCP Factory](https://github.com/ACNet-AI/mcp-factory)*

