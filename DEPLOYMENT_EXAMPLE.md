# 🚀 Deploying Other MCP Servers - Complete Example

This guide demonstrates how agents can use devops-mcp-server to deploy and manage other MCP servers.

## 🎯 Scenario: Deploying a New MCP Server

**Goal**: Deploy `awesome-mcp-server` from GitHub and integrate it with Claude Desktop.

## 💬 Agent Conversation Flow

### Step 1: Deploy the MCP Server

```
You: "Help me deploy awesome-mcp-server from GitHub"

Agent: "I'll deploy it for you. What's the repository URL?"

You: "https://github.com/user/awesome-mcp-server.git"

Agent: [Uses deploy_mcp_server tool]
      ✅ Cloning repository...
      ✅ Installing dependencies with uv...
      ✅ Checking for docker-compose...
      
      "Deployment complete! Server installed at:
      /Users/you/awesome-mcp-server
      
      Next steps:
      1. The server is ready to start
      2. I can help you configure it
      3. We'll add it to Claude Desktop config"
```

### Step 2: Verify Deployment

```
You: "Is it running?"

Agent: [Uses check_mcp_server_health tool]
      "Checking health status...
      
      Status: Not running yet (expected for new deployment)
      Type: docker-compose detected
      
      Would you like me to start it?"

You: "Yes, start it"

Agent: [Uses docker_compose_up tool]
      ✅ Starting services...
      ✅ Container 'awesome-mcp-server' is running
      ✅ Port 8000 is open
      
      "Server is now running!"
```

### Step 3: Monitor and Verify

```
You: "Show me the logs"

Agent: [Uses docker_logs tool]
      "Server logs (last 50 lines):
      
      [INFO] Server starting...
      [INFO] Loading tools...
      [INFO] MCP server ready on port 8000
      [INFO] Waiting for connections...
      
      Everything looks healthy! ✅"
```

### Step 4: Integration Guidance

```
You: "How do I add it to Claude Desktop?"

Agent: "To integrate awesome-mcp-server with Claude Desktop,
       add this to your claude_desktop_config.json:
       
       {
         \"mcpServers\": {
           \"awesome\": {
             \"command\": \"uv\",
             \"args\": [\"run\", \"python\", \"server.py\"],
             \"cwd\": \"/Users/you/awesome-mcp-server\"
           }
         }
       }
       
       Then restart Claude Desktop.
       
       Would you like me to help with anything else?"
```

## 📋 Complete Workflow Examples

### Example 1: Deploy Multiple MCP Servers

```
You: "I need to deploy 3 MCP servers for my project"

Agent: "Sure! Give me the repository URLs"

You: 
"1. https://github.com/org/database-mcp-server
 2. https://github.com/org/api-mcp-server  
 3. https://github.com/org/monitoring-mcp-server"

Agent: [Deploys each server sequentially]
      
      ✅ database-mcp-server deployed to /Users/you/database-mcp-server
      ✅ api-mcp-server deployed to /Users/you/api-mcp-server
      ✅ monitoring-mcp-server deployed to /Users/you/monitoring-mcp-server
      
      [Starts all servers using docker-compose]
      
      "All 3 servers are now running! Here's the status:
      
      1. database-mcp-server: Running (port 5432)
      2. api-mcp-server: Running (port 8000)
      3. monitoring-mcp-server: Running (port 9090)
      
      All healthy ✅"
```

### Example 2: Update and Redeploy

```
You: "awesome-mcp-server has an update, can you redeploy it?"

Agent: [Checks current status]
      "Current version running. I'll update it:
      
      1. Stopping current instance..."
      [Uses docker_compose_down]
      
      "2. Pulling latest changes..."
      [Executes git pull in the project directory]
      
      "3. Reinstalling dependencies..."
      [Uses install_mcp_dependencies]
      
      "4. Restarting server..."
      [Uses docker_compose_up]
      
      ✅ "awesome-mcp-server updated and restarted!
      
      Checking logs for any issues..."
      [Uses docker_logs]
      
      "Everything looks good! ✅"
```

### Example 3: Troubleshooting Deployment

```
You: "The server I just deployed isn't working"

Agent: "Let me help you troubleshoot. Which server?"

You: "awesome-mcp-server"

Agent: [Comprehensive diagnosis]
      
      "Running diagnostics...
      
      1. Checking if container is running..."
      [Uses docker_ps]
      ❌ Container is not running
      
      "2. Checking recent logs..."
      [Uses docker_logs]
      "Found error: Port 8000 already in use
      
      3. Checking what's using port 8000..."
      [Uses list_ports_in_use]
      "Process 'node' is using port 8000
      
      Issue identified: Port conflict
      
      Solutions:
      1. Stop the node process
      2. Change awesome-mcp-server to use a different port
      
      Which would you prefer?"
```

## 🎯 Advanced Use Cases

### Use Case 1: Production Deployment

```
You: "Deploy awesome-mcp-server to production server"

Agent: "I'll deploy to the production server. Is Docker context configured?"

You: "Yes, context name is 'production'"

Agent: [Switches Docker context]
      "Switching to production context...
      
      [Deploys to remote server via SSH]
      ✅ Repository cloned on production
      ✅ Dependencies installed
      ✅ Server started with docker-compose
      ✅ Health check passed
      
      Production deployment complete!
      Server running at: production-server.com:8000"
```

### Use Case 2: Automated Testing

```
You: "Deploy the server, run tests, then tear it down"

Agent: "I'll set up a test environment:
      
      1. Deploying to /tmp/test-awesome-mcp-server..."
      [Uses deploy_mcp_server]
      
      "2. Starting server..."
      [Uses docker_compose_up]
      
      "3. Running health checks..."
      [Uses check_mcp_server_health]
      ✅ Server is healthy
      
      "4. Server is ready for testing
      
      When you're done testing, I can clean up
      with: docker-compose down -v"
```

### Use Case 3: Multi-Environment Management

```
You: "I have dev, staging, and prod environments. Help me manage them"

Agent: "I can help manage all three. Let's organize:
      
      Development:
      - Location: /Users/you/dev/awesome-mcp-server
      - Port: 8000
      - Status: Running ✅
      
      Staging:
      - Location: /Users/you/staging/awesome-mcp-server
      - Port: 8001  
      - Status: Stopped ⏸
      
      Production:
      - Server: production-server.com
      - Status: Running ✅
      - Uptime: 15 days
      
      What would you like to do?"
```

## 🛠️ Technical Details

### What happens during deployment?

```python
# When you say: "Deploy awesome-mcp-server"

# Agent calls: deploy_mcp_server(
#   repo_url="https://github.com/user/awesome-mcp-server.git",
#   target_dir="/Users/you/awesome-mcp-server",
#   start_after_install=True
# )

# Behind the scenes:
# 1. git clone <repo> <target_dir>
# 2. cd <target_dir> && uv sync
# 3. docker-compose up -d (if docker-compose.yml exists)
# 4. Health check
# 5. Return status report
```

### Supported deployment types

- **Python MCP Servers**: Using uv or pip
- **Docker-based MCP Servers**: Using docker-compose
- **Remote deployments**: Via Docker context / SSH
- **Manual deployments**: Clone + install only

### Requirements

- Git installed
- Python 3.10+ with uv or pip
- Docker (for containerized servers)
- SSH access (for remote deployments)

## 🎓 Best Practices

### 1. Directory Organization

```
~/mcp-servers/
├── database-server/
├── api-server/
├── monitoring-server/
└── custom-server/
```

### 2. Always Check Health

After deployment, always verify:
```
"Check if <server-name> is running"
"Show me the logs for <server-name>"
```

### 3. Use docker-compose for Production

Servers with docker-compose.yml are easier to manage:
- Automatic restart on failure
- Environment variable management
- Volume persistence
- Network isolation

### 4. Document Configuration

Keep track of which servers are deployed where:
```
"List all my deployed MCP servers"
"What ports are my MCP servers using?"
```

## ❓ FAQ

**Q: Can I deploy non-Python MCP servers?**
A: Yes, if they have docker-compose.yml. The deployment tools will use Docker instead of Python package managers.

**Q: What if the server needs configuration?**
A: After deployment, you can manually edit config files, or ask the agent to help you configure specific settings.

**Q: Can I deploy to multiple servers at once?**
A: Yes! You can deploy to different directories locally, or use different Docker contexts for remote servers.

**Q: How do I update a deployed server?**
A: Ask the agent to "pull updates and redeploy <server-name>". It will handle git pull, dependency updates, and restart.

**Q: What if deployment fails?**
A: The agent will show detailed error messages from each step (clone, install, start) to help troubleshoot.

## 🎉 Summary

With devops-mcp-server, agents can:

✅ **Deploy** any MCP server from Git
✅ **Install** dependencies automatically
✅ **Start** servers using docker-compose or directly
✅ **Monitor** health and logs
✅ **Manage** multiple servers across environments
✅ **Troubleshoot** issues with detailed diagnostics

**All through natural language conversation!** 🚀

---

*For more examples, see [USAGE.md](./USAGE.md)*

