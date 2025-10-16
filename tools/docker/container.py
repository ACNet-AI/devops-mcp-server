"""Docker container management tools."""

import subprocess


def docker_ps(all_containers: bool = False) -> dict:
    """List Docker containers.

    Args:
        all_containers: Show all containers including stopped ones (default: False)

    Returns:
        dict: Container list and status

    """
    cmd = ["docker", "ps"]
    if all_containers:
        cmd.append("-a")

    try:
        result = subprocess.run(cmd, check=False, capture_output=True, text=True, timeout=30)

        return {"success": True, "output": result.stdout, "containers": result.stdout}
    except FileNotFoundError:
        return {
            "success": False,
            "error": "docker command not found. Please install Docker.",
        }
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {e!s}"}


def docker_logs(
    container: str, follow: bool = False, tail: int = 100, since: str | None = None,
) -> dict:
    """View Docker container logs.

    Args:
        container: Container name or ID
        follow: Follow log output (default: False)
        tail: Number of lines to show from end (default: 100)
        since: Show logs since timestamp (e.g., "2023-01-01", "1h")

    Returns:
        dict: Container logs

    """
    cmd = ["docker", "logs", f"--tail={tail}"]

    if follow:
        cmd.append("-f")
    if since:
        cmd.extend(["--since", since])

    cmd.append(container)

    try:
        result = subprocess.run(
            cmd, check=False, capture_output=True, text=True, timeout=30 if not follow else None,
        )

        return {
            "success": True,
            "container": container,
            "logs": result.stdout,
            "errors": result.stderr,
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "docker command not found. Please install Docker.",
        }
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {e!s}"}


def docker_stop(container: str, timeout: int = 10) -> dict:
    """Stop a Docker container.

    Args:
        container: Container name or ID
        timeout: Seconds to wait before killing (default: 10)

    Returns:
        dict: Operation result

    """
    try:
        result = subprocess.run(
            ["docker", "stop", "-t", str(timeout), container],
            check=False, capture_output=True,
            text=True,
            timeout=timeout + 30,
        )

        return {
            "success": result.returncode == 0,
            "container": container,
            "message": f"Container {container} stopped successfully"
            if result.returncode == 0
            else f"Failed to stop container {container}",
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "docker command not found. Please install Docker.",
        }
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {e!s}"}


def docker_start(container: str) -> dict:
    """Start a Docker container.

    Args:
        container: Container name or ID

    Returns:
        dict: Operation result

    """
    try:
        result = subprocess.run(
            ["docker", "start", container], check=False, capture_output=True, text=True, timeout=30,
        )

        return {
            "success": result.returncode == 0,
            "container": container,
            "message": f"Container {container} started successfully"
            if result.returncode == 0
            else f"Failed to start container {container}",
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "docker command not found. Please install Docker.",
        }
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {e!s}"}


def docker_restart(container: str, timeout: int = 10) -> dict:
    """Restart a Docker container.

    Args:
        container: Container name or ID
        timeout: Seconds to wait before killing (default: 10)

    Returns:
        dict: Operation result

    """
    try:
        result = subprocess.run(
            ["docker", "restart", "-t", str(timeout), container],
            check=False, capture_output=True,
            text=True,
            timeout=timeout + 30,
        )

        return {
            "success": result.returncode == 0,
            "container": container,
            "message": f"Container {container} restarted successfully"
            if result.returncode == 0
            else f"Failed to restart container {container}",
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "docker command not found. Please install Docker.",
        }
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {e!s}"}


def docker_inspect(container: str) -> dict:
    """Get detailed information about a Docker container.

    Args:
        container: Container name or ID

    Returns:
        dict: Container information

    """
    try:
        result = subprocess.run(
            ["docker", "inspect", container], check=False, capture_output=True, text=True, timeout=30,
        )

        return {
            "success": result.returncode == 0,
            "container": container,
            "info": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "docker command not found. Please install Docker.",
        }
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {e!s}"}


def docker_stats(container: str | None = None, no_stream: bool = True) -> dict:
    """Display resource usage statistics for Docker containers.

    Args:
        container: Container name or ID (optional, shows all if not specified)
        no_stream: Return stats once instead of streaming (default: True)

    Returns:
        dict: Container statistics

    """
    cmd = ["docker", "stats"]
    if no_stream:
        cmd.append("--no-stream")
    if container:
        cmd.append(container)

    try:
        result = subprocess.run(cmd, check=False, capture_output=True, text=True, timeout=30)

        return {
            "success": True,
            "stats": result.stdout,
            "container": container or "all containers",
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "docker command not found. Please install Docker.",
        }
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {e!s}"}


__all__ = [
    "docker_inspect",
    "docker_logs",
    "docker_ps",
    "docker_restart",
    "docker_start",
    "docker_stats",
    "docker_stop",
]
