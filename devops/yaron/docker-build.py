import docker
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def try_build_docker_image(dockerfile_dir, image_tag):
    client = docker.from_env()

    dockerfile_dir = '/path/to/your/dockerfile_directory'
    image_tag = 'latest '

    # Define the build parameters
    build_params = {
      'path': dockerfile_dir,
      'dockerfile': 'Dockerfile',  # Name of your Dockerfile
      'tag': 'your_image_tag',  # Tag for your Docker image
      'rm': True,  # Remove intermediate containers after a successful build
    } 

    try:
        logger.info(f"Building Docker image '{image_tag}' from '{dockerfile_dir}'")
        with client.build(**build_params) as response:
            for line in response:
                logger.info(line.decode('utf-8').strip())

        logger.info("Build completed successfully.")
        return True
    
    except docker.errors.BuildError as e:
        logger.error(f"Build failed: {e}")
    except Exception as e:
        logger.error(f"An error occurred during the build: {e}")
    
    return False