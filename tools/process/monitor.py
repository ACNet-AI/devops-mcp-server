"""Process monitoring tools."""

import subprocess


def check_service_status(service_name: str) -> dict:
    """Check if a service/process is running.

    Args:
        service_name: Name or pattern to search for in process list

    Returns:
        dict: Service status information

    """
    try:
        # Use ps to check if process is running
        result = subprocess.run(
            ["ps", "aux"], check=False, capture_output=True, text=True, timeout=10,
        )

        # Filter processes containing service_name
        matching_processes = [
            line
            for line in result.stdout.splitlines()
            if service_name.lower() in line.lower()
        ]

        return {
            "success": True,
            "service": service_name,
            "running": len(matching_processes) > 0,
            "process_count": len(matching_processes),
            "processes": matching_processes[:10],  # Limit to first 10
        }
    except Exception as e:
        return {"success": False, "error": f"Failed to check service status: {e!s}"}


def get_system_info() -> dict:
    """Get basic system information.

    Returns:
        dict: System information including memory, CPU, disk usage

    """
    info = {}

    # Get memory info (macOS/Linux)
    try:
        if subprocess.run(["which", "free"], check=False, capture_output=True).returncode == 0:
            # Linux
            result = subprocess.run(
                ["free", "-h"], check=False, capture_output=True, text=True, timeout=10,
            )
            info["memory"] = result.stdout
        else:
            # macOS
            result = subprocess.run(
                ["vm_stat"], check=False, capture_output=True, text=True, timeout=10,
            )
            info["memory"] = result.stdout
    except Exception as e:
        info["memory"] = f"Could not retrieve memory info: {e!s}"

    # Get disk usage
    try:
        result = subprocess.run(
            ["df", "-h"], check=False, capture_output=True, text=True, timeout=10,
        )
        info["disk"] = result.stdout
    except Exception as e:
        info["disk"] = f"Could not retrieve disk info: {e!s}"

    # Get uptime
    try:
        result = subprocess.run(["uptime"], check=False, capture_output=True, text=True, timeout=10)
        info["uptime"] = result.stdout.strip()
    except Exception as e:
        info["uptime"] = f"Could not retrieve uptime: {e!s}"

    return {"success": True, "system_info": info}


def list_ports_in_use(port: int | None = None) -> dict:
    """List ports in use by processes.

    Args:
        port: Specific port number to check (optional)

    Returns:
        dict: Port usage information

    """
    try:
        if port:
            # Check specific port
            result = subprocess.run(
                ["lsof", "-i", f":{port}"], check=False, capture_output=True, text=True, timeout=10,
            )
        else:
            # List all listening ports
            result = subprocess.run(
                ["lsof", "-i", "-P", "-n"], check=False, capture_output=True, text=True, timeout=10,
            )

        return {
            "success": True,
            "port": port,
            "output": result.stdout,
            "in_use": bool(result.stdout.strip()) if port else None,
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "lsof command not found. This feature may not be available on your system.",
        }
    except Exception as e:
        return {"success": False, "error": f"Failed to check ports: {e!s}"}


__all__ = [
    "check_service_status",
    "get_system_info",
    "list_ports_in_use",
]
