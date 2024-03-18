import subprocess

def deploy_docker_compose(folders):
    for folder in folders:
        print(f"Deploying Docker Compose for {folder}...")
        subprocess.run(["docker-compose", "-f", f"{folder}/docker-compose.yml", "up", "-d"], check=True)

if __name__ == "__main__":
    folders = ["weight", "billing"]
    deploy_docker_compose(folders)
