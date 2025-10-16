"""Docker Hub registry tools.

Provides tools to build, tag, and push Docker images to Docker Hub.
"""

import subprocess


def docker_login(username: str, password: str, registry: str = "docker.io") -> str:
    """Login to Docker registry (Docker Hub or private registry).

    Args:
        username: Docker Hub username or registry username
        password: Docker Hub password or access token
        registry: Registry URL (default: docker.io for Docker Hub)

    Returns:
        Login status

    """
    try:
        result = subprocess.run(
            ["docker", "login", registry, "-u", username, "--password-stdin"],
            check=False, input=password.encode(),
            capture_output=True,
            text=False,
            timeout=30,
        )

        if result.returncode == 0:
            return f"✅ Successfully logged in to {registry}"
        error = result.stderr.decode() if result.stderr else "Unknown error"
        return f"❌ Login failed: {error}"

    except FileNotFoundError:
        return "❌ Docker not found. Please install Docker first."
    except Exception as e:
        return f"❌ Error during login: {e!s}"


def docker_build_image(
    directory: str,
    image_name: str,
    tag: str = "latest",
    dockerfile: str = "Dockerfile",
    build_args: dict | None = None,
) -> str:
    """Build Docker image from Dockerfile.

    Args:
        directory: Build context directory
        image_name: Image name (e.g., 'username/myapp')
        tag: Image tag (default: 'latest')
        dockerfile: Dockerfile name (default: 'Dockerfile')
        build_args: Optional build arguments as dict

    Returns:
        Build status and image ID

    """
    try:
        full_image = f"{image_name}:{tag}"
        cmd = ["docker", "build", "-t", full_image, "-f", dockerfile]

        # Add build args if provided
        if build_args:
            for key, value in build_args.items():
                cmd.extend(["--build-arg", f"{key}={value}"])

        cmd.append(directory)

        result = subprocess.run(
            cmd,
            check=False, capture_output=True,
            text=True,
            timeout=600,  # Building can take time
        )

        if result.returncode == 0:
            return f"✅ Image '{full_image}' built successfully\n{result.stdout[-500:]}"  # Last 500 chars
        return (
            f"❌ Build failed:\n{result.stderr[-1000:]}"  # Last 1000 chars of error
        )

    except FileNotFoundError:
        return "❌ Docker not found"
    except subprocess.TimeoutExpired:
        return "⏱️ Build timeout after 10 minutes"
    except Exception as e:
        return f"❌ Error during build: {e!s}"


def docker_tag_image(source_image: str, target_image: str) -> str:
    """Tag Docker image with new name/tag.

    Args:
        source_image: Source image (e.g., 'myapp:latest')
        target_image: Target image (e.g., 'username/myapp:v1.0')

    Returns:
        Tagging status

    """
    try:
        result = subprocess.run(
            ["docker", "tag", source_image, target_image],
            check=False, capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            return f"✅ Tagged '{source_image}' as '{target_image}'"
        return f"❌ Tagging failed: {result.stderr}"

    except FileNotFoundError:
        return "❌ Docker not found"
    except Exception as e:
        return f"❌ Error: {e!s}"


def docker_push_image(image_name: str, tag: str = "latest") -> str:
    """Push Docker image to registry (Docker Hub or private).

    Args:
        image_name: Full image name (e.g., 'username/myapp')
        tag: Image tag (default: 'latest')

    Returns:
        Push status and registry URL

    """
    try:
        full_image = f"{image_name}:{tag}"
        result = subprocess.run(
            ["docker", "push", full_image],
            check=False, capture_output=True,
            text=True,
            timeout=600,  # Pushing can take time
        )

        if result.returncode == 0:
            return f"✅ Image '{full_image}' pushed successfully\n{result.stdout}"
        return f"❌ Push failed: {result.stderr}"

    except FileNotFoundError:
        return "❌ Docker not found"
    except subprocess.TimeoutExpired:
        return "⏱️ Push timeout after 10 minutes"
    except Exception as e:
        return f"❌ Error during push: {e!s}"


def docker_build_and_push(
    directory: str,
    image_name: str,
    tag: str = "latest",
    dockerfile: str = "Dockerfile",
    platforms: str | None = None,
) -> str:
    """Build and push Docker image in one command (uses buildx for multi-platform).

    Args:
        directory: Build context directory
        image_name: Full image name (e.g., 'username/myapp')
        tag: Image tag (default: 'latest')
        dockerfile: Dockerfile name
        platforms: Comma-separated platforms (e.g., 'linux/amd64,linux/arm64')

    Returns:
        Build and push status

    """
    try:
        full_image = f"{image_name}:{tag}"
        cmd = [
            "docker",
            "buildx",
            "build",
            "-t",
            full_image,
            "-f",
            dockerfile,
            "--push",
        ]

        if platforms:
            cmd.extend(["--platform", platforms])

        cmd.append(directory)

        result = subprocess.run(
            cmd,
            check=False, capture_output=True,
            text=True,
            timeout=900,  # 15 minutes for multi-platform builds
        )

        if result.returncode == 0:
            return f"✅ Image '{full_image}' built and pushed successfully\n{result.stdout[-500:]}"
        return f"❌ Build and push failed:\n{result.stderr[-1000:]}"

    except FileNotFoundError:
        return "❌ Docker buildx not found. Use: docker buildx create --use"
    except subprocess.TimeoutExpired:
        return "⏱️ Operation timeout after 15 minutes"
    except Exception as e:
        return f"❌ Error: {e!s}"


def docker_list_local_images(filter_name: str | None = None) -> str:
    """List local Docker images.

    Args:
        filter_name: Optional filter by image name

    Returns:
        List of Docker images with size and created date

    """
    try:
        cmd = ["docker", "images"]
        if filter_name:
            cmd.append(filter_name)

        result = subprocess.run(cmd, check=False, capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            return result.stdout if result.stdout else "No images found"
        return f"❌ Failed to list images: {result.stderr}"

    except FileNotFoundError:
        return "❌ Docker not found"
    except Exception as e:
        return f"❌ Error: {e!s}"


def docker_remove_image(image_name: str, force: bool = False) -> str:
    """Remove Docker image from local system.

    Args:
        image_name: Image name with optional tag (e.g., 'myapp:latest')
        force: Force removal even if image is in use

    Returns:
        Removal status

    """
    try:
        cmd = ["docker", "rmi", image_name]
        if force:
            cmd.append("-f")

        result = subprocess.run(cmd, check=False, capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            return f"✅ Image '{image_name}' removed successfully"
        return f"❌ Removal failed: {result.stderr}"

    except FileNotFoundError:
        return "❌ Docker not found"
    except Exception as e:
        return f"❌ Error: {e!s}"
