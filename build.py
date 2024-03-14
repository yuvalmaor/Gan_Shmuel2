import subprocess

def build_docker_compose(folders):
    for folder in folders:
        print(f"Building Docker Compose for {folder}...")
        subprocess.run(["docker-compose", "-f", f"{folder}/docker-compose.yml", "build"], check=True)

if __name__ == "__main__":
    folders = ["weight", "billing"]
    build_docker_compose(folders)
