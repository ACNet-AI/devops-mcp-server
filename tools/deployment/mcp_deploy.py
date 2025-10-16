"""
MCP Server deployment automation tools
"""
import subprocess
from pathlib import Path


def clone_mcp_server(repo_url: str, target_dir: str) -> dict:
    """
    Clone an MCP server repository
    
    Args:
        repo_url: Git repository URL (e.g., "https://github.com/user/repo.git")
        target_dir: Target directory to clone into
    
    Returns:
        dict: Operation result
    """
    target_path = Path(target_dir)
    
    # Check if directory already exists
    if target_path.exists():
        return {
            "success": False,
            "error": f"Directory {target_dir} already exists"
        }
    
    try:
        result = subprocess.run(
            ["git", "clone", repo_url, target_dir],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        return {
            "success": result.returncode == 0,
            "path": target_dir,
            "message": "Repository cloned successfully" if result.returncode == 0 else "Failed to clone repository",
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Clone operation timed out after 5 minutes"
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "git command not found. Please install Git."
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }


def install_mcp_dependencies(project_path: str) -> dict:
    """
    Install dependencies for an MCP server project
    
    Args:
        project_path: Path to MCP server project
    
    Returns:
        dict: Operation result
    """
    project_dir = Path(project_path).resolve()
    
    if not project_dir.exists():
        return {
            "success": False,
            "error": f"Project directory {project_path} does not exist"
        }
    
    # Check for pyproject.toml
    pyproject = project_dir / "pyproject.toml"
    if not pyproject.exists():
        return {
            "success": False,
            "error": "pyproject.toml not found. Is this a Python MCP server?"
        }
    
    try:
        # Try uv sync first (faster)
        result = subprocess.run(
            ["uv", "sync"],
            cwd=str(project_dir),
            capture_output=True,
            text=True,
            timeout=600
        )
        
        return {
            "success": result.returncode == 0,
            "message": "Dependencies installed successfully" if result.returncode == 0 else "Failed to install dependencies",
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None
        }
    except FileNotFoundError:
        # Fallback to pip install
        try:
            result = subprocess.run(
                ["pip", "install", "-e", "."],
                cwd=str(project_dir),
                capture_output=True,
                text=True,
                timeout=600
            )
            
            return {
                "success": result.returncode == 0,
                "message": "Dependencies installed with pip" if result.returncode == 0 else "Failed to install dependencies",
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to install dependencies: {str(e)}"
            }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Installation timed out after 10 minutes"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }


def deploy_mcp_server(
    repo_url: str,
    target_dir: str,
    start_after_install: bool = False
) -> dict:
    """
    Complete deployment workflow for an MCP server
    
    Args:
        repo_url: Git repository URL
        target_dir: Target directory for deployment
        start_after_install: Start the server after installation
    
    Returns:
        dict: Deployment result with detailed steps
    """
    steps = []
    
    # Step 1: Clone repository
    steps.append({"step": "clone", "status": "running"})
    clone_result = clone_mcp_server(repo_url, target_dir)
    steps[-1]["status"] = "success" if clone_result["success"] else "failed"
    steps[-1]["result"] = clone_result
    
    if not clone_result["success"]:
        return {
            "success": False,
            "message": "Deployment failed at clone step",
            "steps": steps
        }
    
    # Step 2: Install dependencies
    steps.append({"step": "install_dependencies", "status": "running"})
    install_result = install_mcp_dependencies(target_dir)
    steps[-1]["status"] = "success" if install_result["success"] else "failed"
    steps[-1]["result"] = install_result
    
    if not install_result["success"]:
        return {
            "success": False,
            "message": "Deployment failed at dependency installation",
            "steps": steps
        }
    
    # Step 3: Start server (if requested)
    if start_after_install:
        steps.append({"step": "start_server", "status": "running"})
        project_path = Path(target_dir)
        
        # Check for docker-compose.yml
        if (project_path / "docker-compose.yml").exists():
            # Import docker compose tools
            try:
                from ..docker.compose import docker_compose_up
                start_result = docker_compose_up(target_dir)
                steps[-1]["status"] = "success" if start_result["success"] else "failed"
                steps[-1]["result"] = start_result
            except Exception as e:
                steps[-1]["status"] = "failed"
                steps[-1]["result"] = {"error": str(e)}
        else:
            steps[-1]["status"] = "skipped"
            steps[-1]["result"] = {"message": "No docker-compose.yml found, manual start required"}
    
    return {
        "success": True,
        "message": "MCP server deployed successfully",
        "project_path": target_dir,
        "steps": steps,
        "next_steps": [
            "1. Configure the server in config.yaml if needed",
            "2. Add to Claude Desktop config",
            f"3. Start server: cd {target_dir} && uv run python server.py"
        ]
    }


def check_mcp_server_health(project_path: str) -> dict:
    """
    Check if an MCP server is running and healthy
    
    Args:
        project_path: Path to MCP server project
    
    Returns:
        dict: Health check result
    """
    project_dir = Path(project_path).resolve()
    
    if not project_dir.exists():
        return {
            "success": False,
            "healthy": False,
            "error": f"Project directory {project_path} does not exist"
        }
    
    # Check if docker-compose is running
    if (project_dir / "docker-compose.yml").exists():
        try:
            from ..docker.compose import docker_compose_ps
            status_result = docker_compose_ps(project_path)
            
            return {
                "success": True,
                "healthy": "running" in status_result.get("output", "").lower(),
                "deployment_type": "docker-compose",
                "status": status_result
            }
        except Exception as e:
            return {
                "success": False,
                "healthy": False,
                "error": f"Failed to check docker-compose status: {str(e)}"
            }
    
    # Check for running process
    try:
        from ..process.monitor import check_service_status
        server_name = project_dir.name
        process_result = check_service_status(server_name)
        
        return {
            "success": True,
            "healthy": process_result.get("running", False),
            "deployment_type": "process",
            "status": process_result
        }
    except Exception as e:
        return {
            "success": False,
            "healthy": False,
            "error": f"Failed to check process status: {str(e)}"
        }


__all__ = [
    "clone_mcp_server",
    "install_mcp_dependencies",
    "deploy_mcp_server",
    "check_mcp_server_health",
]

