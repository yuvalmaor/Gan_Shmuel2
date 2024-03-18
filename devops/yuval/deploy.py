import subprocess

def deploy_docker_compose(folders):
    results = []
    for folder in folders:
        print(f"Deploying Docker Compose for {folder}...")
        try:
            # Run the subprocess and capture output and errors
            completed_process = subprocess.run(
                ["docker","compose", "-f", f"{folder}/docker-compose.yml", "up"],
                check=True,
                text=True,  # Ensure the output and errors are captured as strings
                capture_output=True
            )
            # If the command was successful, append stdout to results
            results.append({"folder": folder, "output": completed_process.stdout, "error": None})
        except subprocess.CalledProcessError as e:
            # If an error occurs, append the error message to results
            results.append({"folder": folder, "output": e.stdout, "error": e.stderr})
    print(results)
    return results
if __name__ == "__main__":
    folders = [ "billing"]
    deploy_docker_compose(folders)
