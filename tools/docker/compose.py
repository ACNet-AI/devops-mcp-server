"""Docker Compose management tools."""

import subprocess
from pathlib import Path


def docker_compose_up(
    project_path: str, detach: bool = True, build: bool = False,
) -> dict:
    """Start Docker Compose services.

    Args:
        project_path: Path to project directory containing docker-compose.yml
        detach: Run containers in background (default: True)
        build: Build images before starting (default: False)

    Returns:
        dict: Operation result with status and output

    """
    project_dir = Path(project_path).resolve()
    compose_file = project_dir / "docker-compose.yml"

    if not compose_file.exists():
        return {
            "success": False,
            "error": f"docker-compose.yml not found in {project_path}",
        }

    cmd = ["docker-compose", "up"]
    if detach:
        cmd.append("-d")
    if build:
        cmd.append("--build")

    try:
        result = subprocess.run(
            cmd, check=False, cwd=str(project_dir), capture_output=True, text=True, timeout=300,
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "message": "Services started successfully"
            if result.returncode == 0
            else "Failed to start services",
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Command timed out after 5 minutes"}
    except FileNotFoundError:
        return {
            "success": False,
            "error": "docker-compose command not found. Please install Docker Compose.",
        }
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {e!s}"}


def docker_compose_down(project_path: str, remove_volumes: bool = False) -> dict:
    """Stop and remove Docker Compose services.

    Args:
        project_path: Path to project directory containing docker-compose.yml
        remove_volumes: Remove named volumes (default: False)

    Returns:
        dict: Operation result with status and output

    """
    project_dir = Path(project_path).resolve()
    compose_file = project_dir / "docker-compose.yml"

    if not compose_file.exists():
        return {
            "success": False,
            "error": f"docker-compose.yml not found in {project_path}",
        }

    cmd = ["docker-compose", "down"]
    if remove_volumes:
        cmd.append("-v")

    try:
        result = subprocess.run(
            cmd, check=False, cwd=str(project_dir), capture_output=True, text=True, timeout=120,
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "message": "Services stopped successfully"
            if result.returncode == 0
            else "Failed to stop services",
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Command timed out after 2 minutes"}
    except FileNotFoundError:
        return {
            "success": False,
            "error": "docker-compose command not found. Please install Docker Compose.",
        }
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {e!s}"}


def docker_compose_logs(
    project_path: str, service: str | None = None, follow: bool = False, tail: int = 100,
) -> dict:
    """View Docker Compose service logs.

    Args:
        project_path: Path to project directory containing docker-compose.yml
        service: Specific service name (optional, shows all if not specified)
        follow: Follow log output (default: False)
        tail: Number of lines to show from end (default: 100)

    Returns:
        dict: Operation result with logs

    """
    project_dir = Path(project_path).resolve()
    compose_file = project_dir / "docker-compose.yml"

    if not compose_file.exists():
        return {
            "success": False,
            "error": f"docker-compose.yml not found in {project_path}",
        }

    cmd = ["docker-compose", "logs", f"--tail={tail}"]
    if follow:
        cmd.append("-f")
    if service:
        cmd.append(service)

    try:
        result = subprocess.run(
            cmd,
            check=False, cwd=str(project_dir),
            capture_output=True,
            text=True,
            timeout=30 if not follow else None,
        )

        return {
            "success": True,
            "logs": result.stdout,
            "service": service or "all services",
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Command timed out"}
    except FileNotFoundError:
        return {
            "success": False,
            "error": "docker-compose command not found. Please install Docker Compose.",
        }
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {e!s}"}


def docker_compose_ps(project_path: str) -> dict:
    """List Docker Compose services status.

    Args:
        project_path: Path to project directory containing docker-compose.yml

    Returns:
        dict: Service status information

    """
    project_dir = Path(project_path).resolve()
    compose_file = project_dir / "docker-compose.yml"

    if not compose_file.exists():
        return {
            "success": False,
            "error": f"docker-compose.yml not found in {project_path}",
        }

    try:
        result = subprocess.run(
            ["docker-compose", "ps"],
            check=False, cwd=str(project_dir),
            capture_output=True,
            text=True,
            timeout=30,
        )

        return {
            "success": True,
            "output": result.stdout,
            "services_info": result.stdout,
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "docker-compose command not found. Please install Docker Compose.",
        }
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {e!s}"}


def docker_compose_restart(project_path: str, service: str | None = None) -> dict:
    """Restart Docker Compose services.

    Args:
        project_path: Path to project directory containing docker-compose.yml
        service: Specific service name (optional, restarts all if not specified)

    Returns:
        dict: Operation result

    """
    project_dir = Path(project_path).resolve()
    compose_file = project_dir / "docker-compose.yml"

    if not compose_file.exists():
        return {
            "success": False,
            "error": f"docker-compose.yml not found in {project_path}",
        }

    cmd = ["docker-compose", "restart"]
    if service:
        cmd.append(service)

    try:
        result = subprocess.run(
            cmd, check=False, cwd=str(project_dir), capture_output=True, text=True, timeout=120,
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "message": f"{'Service' if service else 'Services'} restarted successfully"
            if result.returncode == 0
            else "Failed to restart",
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Command timed out after 2 minutes"}
    except FileNotFoundError:
        return {
            "success": False,
            "error": "docker-compose command not found. Please install Docker Compose.",
        }
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {e!s}"}


__all__ = [
    "docker_compose_down",
    "docker_compose_logs",
    "docker_compose_ps",
    "docker_compose_restart",
    "docker_compose_up",
]
