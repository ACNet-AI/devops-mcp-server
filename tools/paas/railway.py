"""Railway deployment tools for MCP servers.

Provides tools to deploy applications to Railway platform through conversation.
"""

import subprocess


def railway_login(token: str | None = None) -> str:
    """Login to Railway using API token or interactive browser flow.

    Args:
        token: Optional Railway API token (from https://railway.app/account/tokens)
               If not provided, opens browser for OAuth login

    Returns:
        Login status and instructions

    """
    try:
        if token:
            # Use token login
            result = subprocess.run(
                ["railway", "login", "--browserless"],
                check=False, input=token.encode(),
                capture_output=True,
                text=False,
                timeout=30,
            )
        else:
            # Interactive browser login
            result = subprocess.run(
                ["railway", "login"], check=False, capture_output=True, text=True, timeout=60,
            )

        if result.returncode == 0:
            return "✅ Successfully logged in to Railway"
        error = result.stderr if result.stderr else result.stdout
        return f"❌ Login failed: {error}"

    except FileNotFoundError:
        return "❌ Railway CLI not found. Install it with: npm install -g @railway/cli"
    except subprocess.TimeoutExpired:
        return "⏱️ Login timeout. Please try again."
    except Exception as e:
        return f"❌ Error during login: {e!s}"


def railway_init(project_name: str, directory: str = ".") -> str:
    """Initialize a new Railway project or link to existing one.

    Args:
        project_name: Name of the Railway project
        directory: Project directory (default: current directory)

    Returns:
        Initialization status and project info

    """
    try:
        # Initialize new project
        result = subprocess.run(
            ["railway", "init", "--name", project_name],
            check=False, cwd=directory,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            return f"✅ Railway project '{project_name}' initialized\n{result.stdout}"
        return f"❌ Initialization failed: {result.stderr}"

    except FileNotFoundError:
        return "❌ Railway CLI not found. Install it with: npm install -g @railway/cli"
    except subprocess.TimeoutExpired:
        return "⏱️ Initialization timeout"
    except Exception as e:
        return f"❌ Error during initialization: {e!s}"


def railway_link(project_id: str, directory: str = ".") -> str:
    """Link current directory to an existing Railway project.

    Args:
        project_id: Railway project ID or name
        directory: Project directory (default: current directory)

    Returns:
        Link status

    """
    try:
        result = subprocess.run(
            ["railway", "link", project_id],
            check=False, cwd=directory,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            return f"✅ Linked to Railway project: {project_id}\n{result.stdout}"
        return f"❌ Link failed: {result.stderr}"

    except FileNotFoundError:
        return "❌ Railway CLI not found"
    except Exception as e:
        return f"❌ Error: {e!s}"


def railway_deploy(
    directory: str = ".", environment: str = "production", detach: bool = True,
) -> str:
    """Deploy application to Railway.

    Args:
        directory: Project directory to deploy
        environment: Railway environment (production/staging/development)
        detach: If True, don't wait for deployment to complete

    Returns:
        Deployment status and URL

    """
    try:
        cmd = ["railway", "up", "--environment", environment]
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
            output = result.stdout
            return f"✅ Deployment initiated\n{output}"
        return f"❌ Deployment failed: {result.stderr}"

    except FileNotFoundError:
        return "❌ Railway CLI not found"
    except subprocess.TimeoutExpired:
        return "⏱️ Deployment timeout. Check Railway dashboard for status."
    except Exception as e:
        return f"❌ Error during deployment: {e!s}"


def railway_status(directory: str = ".", environment: str = "production") -> str:
    """Check Railway deployment status.

    Args:
        directory: Project directory
        environment: Railway environment

    Returns:
        Deployment status information

    """
    try:
        result = subprocess.run(
            ["railway", "status", "--environment", environment],
            check=False, cwd=directory,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            return result.stdout
        return f"❌ Failed to get status: {result.stderr}"

    except FileNotFoundError:
        return "❌ Railway CLI not found"
    except Exception as e:
        return f"❌ Error: {e!s}"


def railway_logs(
    directory: str = ".", environment: str = "production", lines: int = 100,
) -> str:
    """View Railway application logs.

    Args:
        directory: Project directory
        environment: Railway environment
        lines: Number of log lines to fetch (default: 100)

    Returns:
        Application logs

    """
    try:
        result = subprocess.run(
            ["railway", "logs", "--environment", environment, "--lines", str(lines)],
            check=False, cwd=directory,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            return result.stdout if result.stdout else "No logs available"
        return f"❌ Failed to fetch logs: {result.stderr}"

    except FileNotFoundError:
        return "❌ Railway CLI not found"
    except Exception as e:
        return f"❌ Error: {e!s}"


def railway_env_set(
    key: str, value: str, directory: str = ".", environment: str = "production",
) -> str:
    """Set environment variable on Railway.

    Args:
        key: Environment variable name
        value: Environment variable value
        directory: Project directory
        environment: Railway environment

    Returns:
        Operation status

    """
    try:
        result = subprocess.run(
            [
                "railway",
                "variables",
                "--set",
                f"{key}={value}",
                "--environment",
                environment,
            ],
            check=False, cwd=directory,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            return f"✅ Environment variable '{key}' set successfully"
        return f"❌ Failed to set variable: {result.stderr}"

    except FileNotFoundError:
        return "❌ Railway CLI not found"
    except Exception as e:
        return f"❌ Error: {e!s}"


def railway_env_list(directory: str = ".", environment: str = "production") -> str:
    """List all environment variables on Railway.

    Args:
        directory: Project directory
        environment: Railway environment

    Returns:
        List of environment variables

    """
    try:
        result = subprocess.run(
            ["railway", "variables", "--environment", environment],
            check=False, cwd=directory,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            return result.stdout if result.stdout else "No environment variables set"
        return f"❌ Failed to list variables: {result.stderr}"

    except FileNotFoundError:
        return "❌ Railway CLI not found"
    except Exception as e:
        return f"❌ Error: {e!s}"
