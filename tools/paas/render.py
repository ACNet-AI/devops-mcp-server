"""Render deployment tools for MCP servers.

Provides tools to deploy applications to Render platform through conversation.
"""

import subprocess


def render_login(api_key: str) -> str:
    """Authenticate with Render using API key.

    Args:
        api_key: Render API key (from https://dashboard.render.com/u/settings#api-keys)

    Returns:
        Authentication status

    """
    try:
        # Set API key as environment variable
        result = subprocess.run(
            ["render", "config", "set", "--api-key", api_key],
            check=False, capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            return "✅ Successfully authenticated with Render"
        return f"❌ Authentication failed: {result.stderr}"

    except FileNotFoundError:
        return "❌ Render CLI not found. Install it with: npm install -g render-cli"
    except Exception as e:
        return f"❌ Error: {e!s}"


def render_create_service(
    name: str,
    repo_url: str,
    service_type: str = "web",
    branch: str = "main",
    region: str = "oregon",
) -> str:
    """Create a new service on Render.

    Args:
        name: Service name
        repo_url: GitHub repository URL
        service_type: Type of service (web/worker/cron/static)
        branch: Git branch to deploy
        region: Render region (oregon/frankfurt/singapore)

    Returns:
        Service creation status

    """
    try:
        cmd = [
            "render",
            "services",
            "create",
            "--name",
            name,
            "--repo",
            repo_url,
            "--type",
            service_type,
            "--branch",
            branch,
            "--region",
            region,
        ]

        result = subprocess.run(cmd, check=False, capture_output=True, text=True, timeout=60)

        if result.returncode == 0:
            return f"✅ Service '{name}' created successfully\n{result.stdout}"
        return f"❌ Failed to create service: {result.stderr}"

    except FileNotFoundError:
        return "❌ Render CLI not found"
    except Exception as e:
        return f"❌ Error: {e!s}"


def render_deploy(service_id: str, clear_cache: bool = False) -> str:
    """Deploy or redeploy a Render service.

    Args:
        service_id: Render service ID or name
        clear_cache: Clear build cache before deploying

    Returns:
        Deployment status

    """
    try:
        cmd = ["render", "services", "deploy", service_id]
        if clear_cache:
            cmd.append("--clear-cache")

        result = subprocess.run(cmd, check=False, capture_output=True, text=True, timeout=300)

        if result.returncode == 0:
            return f"✅ Deployment initiated for {service_id}\n{result.stdout}"
        return f"❌ Deployment failed: {result.stderr}"

    except FileNotFoundError:
        return "❌ Render CLI not found"
    except subprocess.TimeoutExpired:
        return "⏱️ Deployment timeout. Check Render dashboard."
    except Exception as e:
        return f"❌ Error: {e!s}"


def render_logs(service_id: str, lines: int = 100, follow: bool = False) -> str:
    """View Render service logs.

    Args:
        service_id: Render service ID or name
        lines: Number of log lines to fetch
        follow: Stream logs in real-time (not recommended for MCP)

    Returns:
        Service logs

    """
    try:
        cmd = ["render", "services", "logs", service_id, "--lines", str(lines)]
        if follow:
            cmd.append("--follow")

        result = subprocess.run(
            cmd, check=False, capture_output=True, text=True, timeout=30 if not follow else None,
        )

        if result.returncode == 0:
            return result.stdout if result.stdout else "No logs available"
        return f"❌ Failed to fetch logs: {result.stderr}"

    except FileNotFoundError:
        return "❌ Render CLI not found"
    except Exception as e:
        return f"❌ Error: {e!s}"


def render_env_set(service_id: str, key: str, value: str) -> str:
    """Set environment variable on Render service.

    Args:
        service_id: Render service ID or name
        key: Environment variable name
        value: Environment variable value

    Returns:
        Operation status

    """
    try:
        result = subprocess.run(
            ["render", "services", "env", "set", service_id, f"{key}={value}"],
            check=False, capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            return f"✅ Environment variable '{key}' set for {service_id}"
        return f"❌ Failed to set variable: {result.stderr}"

    except FileNotFoundError:
        return "❌ Render CLI not found"
    except Exception as e:
        return f"❌ Error: {e!s}"


def render_list_services() -> str:
    """List all Render services.

    Returns:
        List of services with their status

    """
    try:
        result = subprocess.run(
            ["render", "services", "list"], check=False, capture_output=True, text=True, timeout=30,
        )

        if result.returncode == 0:
            return result.stdout if result.stdout else "No services found"
        return f"❌ Failed to list services: {result.stderr}"

    except FileNotFoundError:
        return "❌ Render CLI not found"
    except Exception as e:
        return f"❌ Error: {e!s}"
