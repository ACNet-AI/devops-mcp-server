"""Fly.io deployment tools for MCP servers.

Provides tools to deploy applications to Fly.io platform through conversation.
"""

import subprocess


def flyio_auth_login(token: str | None = None) -> str:
    """Authenticate with Fly.io.

    Args:
        token: Optional Fly.io API token (from https://fly.io/user/personal_access_tokens)
              If not provided, opens browser for interactive login

    Returns:
        Authentication status

    """
    try:
        if token:
            # Use token authentication
            result = subprocess.run(
                ["flyctl", "auth", "token", token],
                check=False, capture_output=True,
                text=True,
                timeout=30,
            )
        else:
            # Interactive login
            result = subprocess.run(
                ["flyctl", "auth", "login"], check=False, capture_output=True, text=True, timeout=60,
            )

        if result.returncode == 0:
            return "✅ Successfully authenticated with Fly.io"
        return f"❌ Authentication failed: {result.stderr}"

    except FileNotFoundError:
        return "❌ Fly.io CLI not found. Install it with: curl -L https://fly.io/install.sh | sh"
    except Exception as e:
        return f"❌ Error: {e!s}"


def flyio_launch(
    app_name: str, directory: str = ".", region: str = "sjc", org: str | None = None,
) -> str:
    """Initialize and configure a new Fly.io application.

    Args:
        app_name: Application name (must be unique across Fly.io)
        directory: Project directory
        region: Primary region (sjc/iad/fra/nrt/syd)
        org: Organization slug (optional)

    Returns:
        Launch status and fly.toml configuration info

    """
    try:
        cmd = [
            "flyctl",
            "launch",
            "--name",
            app_name,
            "--region",
            region,
            "--no-deploy",  # Don't deploy immediately
        ]

        if org:
            cmd.extend(["--org", org])

        result = subprocess.run(
            cmd, check=False, cwd=directory, capture_output=True, text=True, timeout=60,
        )

        if result.returncode == 0:
            return f"✅ Fly.io app '{app_name}' initialized\n{result.stdout}"
        return f"❌ Launch failed: {result.stderr}"

    except FileNotFoundError:
        return "❌ Fly.io CLI not found"
    except Exception as e:
        return f"❌ Error: {e!s}"


def flyio_deploy(
    directory: str = ".", remote_only: bool = False, detach: bool = True,
) -> str:
    """Deploy application to Fly.io.

    Args:
        directory: Project directory (must contain fly.toml)
        remote_only: Build on Fly.io servers instead of locally
        detach: Don't wait for deployment to complete

    Returns:
        Deployment status and URL

    """
    try:
        cmd = ["flyctl", "deploy"]

        if remote_only:
            cmd.append("--remote-only")

        if detach:
            cmd.append("--detach")

        result = subprocess.run(
            cmd,
            check=False, cwd=directory,
            capture_output=True,
            text=True,
            timeout=300 if not detach else 60,
        )

        if result.returncode == 0:
            return f"✅ Deployment successful\n{result.stdout}"
        return f"❌ Deployment failed: {result.stderr}"

    except FileNotFoundError:
        return "❌ Fly.io CLI not found"
    except subprocess.TimeoutExpired:
        return "⏱️ Deployment timeout. Check status with: flyctl status"
    except Exception as e:
        return f"❌ Error: {e!s}"


def flyio_status(app_name: str | None = None, directory: str = ".") -> str:
    """Check Fly.io application status.

    Args:
        app_name: Application name (optional if in app directory)
        directory: Project directory

    Returns:
        Application status and instance information

    """
    try:
        cmd = ["flyctl", "status"]
        if app_name:
            cmd.extend(["--app", app_name])

        result = subprocess.run(
            cmd, check=False, cwd=directory, capture_output=True, text=True, timeout=30,
        )

        if result.returncode == 0:
            return result.stdout
        return f"❌ Failed to get status: {result.stderr}"

    except FileNotFoundError:
        return "❌ Fly.io CLI not found"
    except Exception as e:
        return f"❌ Error: {e!s}"


def flyio_logs(
    app_name: str | None = None, directory: str = ".", lines: int = 100,
) -> str:
    """View Fly.io application logs.

    Args:
        app_name: Application name (optional if in app directory)
        directory: Project directory
        lines: Number of log lines to fetch

    Returns:
        Application logs

    """
    try:
        cmd = ["flyctl", "logs", "--lines", str(lines)]
        if app_name:
            cmd.extend(["--app", app_name])

        result = subprocess.run(
            cmd, check=False, cwd=directory, capture_output=True, text=True, timeout=30,
        )

        if result.returncode == 0:
            return result.stdout if result.stdout else "No logs available"
        return f"❌ Failed to fetch logs: {result.stderr}"

    except FileNotFoundError:
        return "❌ Fly.io CLI not found"
    except Exception as e:
        return f"❌ Error: {e!s}"


def flyio_scale(
    app_name: str | None = None,
    count: int | None = None,
    vm_size: str | None = None,
    directory: str = ".",
) -> str:
    """Scale Fly.io application instances or VM size.

    Args:
        app_name: Application name
        count: Number of instances (optional)
        vm_size: VM size (shared-cpu-1x/dedicated-cpu-1x/etc)
        directory: Project directory

    Returns:
        Scaling operation status

    """
    try:
        cmd = ["flyctl", "scale"]

        if count is not None:
            cmd.extend(["count", str(count)])

        if vm_size:
            cmd.extend(["vm", vm_size])

        if app_name:
            cmd.extend(["--app", app_name])

        result = subprocess.run(
            cmd, check=False, cwd=directory, capture_output=True, text=True, timeout=60,
        )

        if result.returncode == 0:
            return f"✅ Scaling completed\n{result.stdout}"
        return f"❌ Scaling failed: {result.stderr}"

    except FileNotFoundError:
        return "❌ Fly.io CLI not found"
    except Exception as e:
        return f"❌ Error: {e!s}"


def flyio_secrets_set(
    key: str, value: str, app_name: str | None = None, directory: str = ".",
) -> str:
    """Set secret (environment variable) on Fly.io.

    Args:
        key: Secret name
        value: Secret value
        app_name: Application name
        directory: Project directory

    Returns:
        Operation status

    """
    try:
        cmd = ["flyctl", "secrets", "set", f"{key}={value}"]
        if app_name:
            cmd.extend(["--app", app_name])

        result = subprocess.run(
            cmd, check=False, cwd=directory, capture_output=True, text=True, timeout=30,
        )

        if result.returncode == 0:
            return f"✅ Secret '{key}' set successfully"
        return f"❌ Failed to set secret: {result.stderr}"

    except FileNotFoundError:
        return "❌ Fly.io CLI not found"
    except Exception as e:
        return f"❌ Error: {e!s}"


def flyio_secrets_list(app_name: str | None = None, directory: str = ".") -> str:
    """List all secrets (environment variables) on Fly.io.

    Args:
        app_name: Application name
        directory: Project directory

    Returns:
        List of secret names (values are not shown for security)

    """
    try:
        cmd = ["flyctl", "secrets", "list"]
        if app_name:
            cmd.extend(["--app", app_name])

        result = subprocess.run(
            cmd, check=False, cwd=directory, capture_output=True, text=True, timeout=30,
        )

        if result.returncode == 0:
            return result.stdout if result.stdout else "No secrets set"
        return f"❌ Failed to list secrets: {result.stderr}"

    except FileNotFoundError:
        return "❌ Fly.io CLI not found"
    except Exception as e:
        return f"❌ Error: {e!s}"
