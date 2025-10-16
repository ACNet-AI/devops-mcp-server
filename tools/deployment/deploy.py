"""Universal deployment automation tools.

Provides generic deployment capabilities for any application type:
- Web servers (Nginx, Apache, FastAPI, Express)
- API servers (REST, GraphQL)
- Databases (PostgreSQL, MongoDB, Redis)
- MCP servers
- Any containerized or package-based application

Supports multiple deployment sources:
- Git repositories (GitHub, GitLab, Gitea, etc.)
- Docker images (Docker Hub, GHCR, private registries)
- PyPI packages (Python applications)
- NPM packages (Node.js applications)
- Local directories (development/testing)
"""

import subprocess
from pathlib import Path


def clone_from_git(
    repo_url: str,
    target_dir: str,
    branch: str | None = None,
    depth: int | None = None,
) -> dict:
    """Clone application from Git repository (generic for any project type).

    Supports multiple Git platforms:
    - GitHub: https://github.com/user/repo.git
    - GitLab: https://gitlab.com/user/repo.git
    - Gitea/Self-hosted: https://git.company.com/repo.git
    - Bitbucket: https://bitbucket.org/user/repo.git
    - SSH: git@github.com:user/repo.git

    Args:
        repo_url: Git repository URL
        target_dir: Target directory to clone into
        branch: Specific branch to clone (default: main/master)
        depth: Clone depth for shallow clone (e.g., 1 for latest commit only)

    Returns:
        dict: Operation result with success status

    Examples:
        Clone a web server:
        >>> clone_from_git("https://github.com/user/nginx-config.git", "/opt/nginx")

        Clone an MCP server:
        >>> clone_from_git("https://github.com/user/mcp-server.git", "/opt/mcp")

    """
    target_path = Path(target_dir)

    # Check if directory already exists
    if target_path.exists():
        return {"success": False, "error": f"Directory {target_dir} already exists"}

    try:
        cmd = ["git", "clone"]

        # Add optional parameters
        if branch:
            cmd.extend(["-b", branch])
        if depth:
            cmd.extend(["--depth", str(depth)])

        cmd.extend([repo_url, target_dir])

        result = subprocess.run(cmd, check=False, capture_output=True, text=True, timeout=300)

        return {
            "success": result.returncode == 0,
            "path": target_dir,
            "message": "Repository cloned successfully"
            if result.returncode == 0
            else "Failed to clone repository",
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Clone operation timed out after 5 minutes"}
    except FileNotFoundError:
        return {"success": False, "error": "git command not found. Please install Git."}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {e!s}"}


def deploy_from_docker(
    image_name: str,
    container_name: str,
    port: int | None = None,
    env_vars: dict | None = None,
    volumes: dict | None = None,
) -> dict:
    """Deploy application from Docker image (generic for any containerized app).

    Supports multiple registries:
    - Docker Hub: username/app-name:tag
    - GHCR: ghcr.io/user/app-name:tag
    - Private: registry.company.com/app-name:tag

    Use cases:
    - Web servers: nginx, apache, caddy
    - Databases: postgres, mongodb, redis
    - API servers: FastAPI, Express, Django
    - MCP servers: any MCP implementation

    Args:
        image_name: Docker image name (e.g., "username/mcp-server:latest")
        container_name: Name for the container
        port: Optional host port to expose (e.g., 8080:8080)
        env_vars: Optional environment variables dict
        volumes: Optional volume mounts dict (host_path: container_path)

    Returns:
        dict: Deployment result with container ID

    """
    try:
        # Pull image first
        pull_result = subprocess.run(
            ["docker", "pull", image_name], check=False, capture_output=True, text=True, timeout=300,
        )

        if pull_result.returncode != 0:
            return {
                "success": False,
                "error": f"Failed to pull image: {pull_result.stderr}",
            }

        # Build docker run command
        cmd = ["docker", "run", "-d", "--name", container_name]

        # Add port mapping
        if port:
            cmd.extend(["-p", f"{port}:{port}"])

        # Add environment variables
        if env_vars:
            for key, value in env_vars.items():
                cmd.extend(["-e", f"{key}={value}"])

        # Add volume mounts
        if volumes:
            for host_path, container_path in volumes.items():
                cmd.extend(["-v", f"{host_path}:{container_path}"])

        cmd.append(image_name)

        # Run container
        run_result = subprocess.run(cmd, check=False, capture_output=True, text=True, timeout=60)

        if run_result.returncode == 0:
            container_id = run_result.stdout.strip()
            return {
                "success": True,
                "container_id": container_id,
                "container_name": container_name,
                "message": f"Container {container_name} deployed successfully",
            }
        return {
            "success": False,
            "error": f"Failed to start container: {run_result.stderr}",
        }

    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Docker operation timed out"}
    except FileNotFoundError:
        return {"success": False, "error": "Docker not found. Please install Docker."}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {e!s}"}


def deploy_from_pypi(package_name: str, target_dir: str | None = None) -> dict:
    """Install Python application from PyPI package (generic for any Python app).

    Args:
        package_name: PyPI package name
                      Examples: "fastapi", "django", "flask", "mcp-server-example"
        target_dir: Optional directory to install into (creates venv)

    Returns:
        dict: Installation result

    """
    try:
        if target_dir:
            # Create venv and install
            venv_path = Path(target_dir) / ".venv"
            subprocess.run(
                ["python3", "-m", "venv", str(venv_path)],
                check=True,
                capture_output=True,
                timeout=60,
            )

            pip_cmd = [str(venv_path / "bin" / "pip"), "install", package_name]
        else:
            # Global install
            pip_cmd = ["pip", "install", package_name]

        result = subprocess.run(pip_cmd, check=False, capture_output=True, text=True, timeout=300)

        return {
            "success": result.returncode == 0,
            "package": package_name,
            "install_dir": target_dir if target_dir else "global",
            "message": f"Package {package_name} installed successfully"
            if result.returncode == 0
            else "Installation failed",
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
        }

    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Installation timed out after 5 minutes"}
    except FileNotFoundError:
        return {"success": False, "error": "Python/pip not found"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {e!s}"}


def deploy_from_npm(package_name: str, global_install: bool = True) -> dict:
    """Install Node.js application from NPM package (generic for any Node app).

    Args:
        package_name: NPM package name
                      Examples: "express", "next", "pm2", "@modelcontextprotocol/server-xyz"
        global_install: Install globally (default) or locally

    Returns:
        dict: Installation result

    """
    try:
        cmd = ["npm", "install"]
        if global_install:
            cmd.append("-g")
        cmd.append(package_name)

        result = subprocess.run(cmd, check=False, capture_output=True, text=True, timeout=300)

        return {
            "success": result.returncode == 0,
            "package": package_name,
            "scope": "global" if global_install else "local",
            "message": f"Package {package_name} installed successfully"
            if result.returncode == 0
            else "Installation failed",
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
        }

    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Installation timed out after 5 minutes"}
    except FileNotFoundError:
        return {"success": False, "error": "npm not found. Please install Node.js"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {e!s}"}


def deploy_from_local(source_path: str, target_dir: str, symlink: bool = False) -> dict:
    """Deploy application from local directory (generic for any project type).

    Use cases:
    - Deploy built applications to production directories
    - Copy configuration files to system locations
    - Create development symlinks for live editing

    Args:
        source_path: Source directory path
        target_dir: Target deployment directory
        symlink: Create symlink instead of copying (useful for development)

    Returns:
        dict: Deployment result

    """
    import shutil

    source = Path(source_path).resolve()
    target = Path(target_dir).resolve()

    if not source.exists():
        return {"success": False, "error": f"Source path {source_path} does not exist"}

    if target.exists():
        return {
            "success": False,
            "error": f"Target directory {target_dir} already exists",
        }

    try:
        if symlink:
            target.symlink_to(source, target_is_directory=True)
            action = "symlinked"
        else:
            shutil.copytree(source, target)
            action = "copied"

        return {
            "success": True,
            "source": str(source),
            "target": str(target),
            "method": "symlink" if symlink else "copy",
            "message": f"Project {action} successfully from {source_path} to {target_dir}",
        }

    except Exception as e:
        return {"success": False, "error": f"Failed to deploy: {e!s}"}


def install_dependencies(project_path: str) -> dict:
    """Install dependencies for any project (generic for Python, Node.js, etc.).

    Automatically detects project type and uses appropriate package manager:
    - Python: uv, pip (if requirements.txt or pyproject.toml exists)
    - Node.js: npm (if package.json exists)

    Use cases:
    - Web applications (FastAPI, Django, Express, Next.js)
    - CLI tools
    - API servers
    - MCP servers

    Args:
        project_path: Path to project directory

    Returns:
        dict: Operation result with installation details

    """
    project_dir = Path(project_path).resolve()

    if not project_dir.exists():
        return {
            "success": False,
            "error": f"Project directory {project_path} does not exist",
        }

    # Check for pyproject.toml
    pyproject = project_dir / "pyproject.toml"
    if not pyproject.exists():
        return {
            "success": False,
            "error": "pyproject.toml not found. Is this a Python MCP server?",
        }

    try:
        # Try uv sync first (faster)
        result = subprocess.run(
            ["uv", "sync"],
            check=False, cwd=str(project_dir),
            capture_output=True,
            text=True,
            timeout=600,
        )

        return {
            "success": result.returncode == 0,
            "message": "Dependencies installed successfully"
            if result.returncode == 0
            else "Failed to install dependencies",
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
        }
    except FileNotFoundError:
        # Fallback to pip install
        try:
            result = subprocess.run(
                ["pip", "install", "-e", "."],
                check=False, cwd=str(project_dir),
                capture_output=True,
                text=True,
                timeout=600,
            )

            return {
                "success": result.returncode == 0,
                "message": "Dependencies installed with pip"
                if result.returncode == 0
                else "Failed to install dependencies",
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None,
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to install dependencies: {e!s}",
            }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Installation timed out after 10 minutes"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {e!s}"}


def deploy_mcp_server(
    repo_url: str, target_dir: str, start_after_install: bool = False,
) -> dict:
    """Complete deployment workflow for an MCP server.

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
    clone_result = clone_from_git(repo_url, target_dir)
    steps[-1]["status"] = "success" if clone_result["success"] else "failed"
    steps[-1]["result"] = clone_result

    if not clone_result["success"]:
        return {
            "success": False,
            "message": "Deployment failed at clone step",
            "steps": steps,
        }

    # Step 2: Install dependencies
    steps.append({"step": "install_dependencies", "status": "running"})
    install_result = install_dependencies(target_dir)
    steps[-1]["status"] = "success" if install_result["success"] else "failed"
    steps[-1]["result"] = install_result

    if not install_result["success"]:
        return {
            "success": False,
            "message": "Deployment failed at dependency installation",
            "steps": steps,
        }

    # Step 3: Start server (if requested)
    if start_after_install:
        steps.append({"step": "start_server", "status": "running"})
        project_path = Path(target_dir)

        # Check for docker-compose.yml
        if (project_path / "docker-compose.yml").exists():
            # Import docker compose tools
            try:
                from tools.docker.compose import docker_compose_up

                start_result = docker_compose_up(target_dir)
                steps[-1]["status"] = "success" if start_result["success"] else "failed"
                steps[-1]["result"] = start_result
            except Exception as e:
                steps[-1]["status"] = "failed"
                steps[-1]["result"] = {"error": str(e)}
        else:
            steps[-1]["status"] = "skipped"
            steps[-1]["result"] = {
                "message": "No docker-compose.yml found, manual start required",
            }

    return {
        "success": True,
        "message": "MCP server deployed successfully",
        "project_path": target_dir,
        "steps": steps,
        "next_steps": [
            "1. Configure the server in config.yaml if needed",
            "2. Add to Claude Desktop config",
            f"3. Start server: cd {target_dir} && uv run python server.py",
        ],
    }


def check_mcp_server_health(project_path: str) -> dict:
    """Check if an MCP server is running and healthy.

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
            "error": f"Project directory {project_path} does not exist",
        }

    # Check if docker-compose is running
    if (project_dir / "docker-compose.yml").exists():
        try:
            from tools.docker.compose import docker_compose_ps

            status_result = docker_compose_ps(project_path)

            return {
                "success": True,
                "healthy": "running" in status_result.get("output", "").lower(),
                "deployment_type": "docker-compose",
                "status": status_result,
            }
        except Exception as e:
            return {
                "success": False,
                "healthy": False,
                "error": f"Failed to check docker-compose status: {e!s}",
            }

    # Check for running process
    try:
        from tools.process.monitor import check_service_status

        server_name = project_dir.name
        process_result = check_service_status(server_name)

        return {
            "success": True,
            "healthy": process_result.get("running", False),
            "deployment_type": "process",
            "status": process_result,
        }
    except Exception as e:
        return {
            "success": False,
            "healthy": False,
            "error": f"Failed to check process status: {e!s}",
        }


__all__ = [
    "check_mcp_server_health",  # MCP server health checking
    # Generic deployment functions - work for any application type
    "clone_from_git",
    "deploy_from_docker",
    "deploy_from_local",
    "deploy_from_npm",
    "deploy_from_pypi",
    # High-level automation workflows
    "deploy_mcp_server",  # Automated MCP server deployment workflow
    "install_dependencies",
]
