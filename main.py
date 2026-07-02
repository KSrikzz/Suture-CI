import os
import sys
from dotenv import load_dotenv
from monitor.watcher import DockerWatcher

if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPO")
    
    missing_vars = []
    if not token:
        missing_vars.append("GITHUB_TOKEN")
    if not repo:
        missing_vars.append("GITHUB_REPO")
        
    if missing_vars:
        print(f"[-] ERROR: Required environment variable(s) {', '.join(missing_vars)} missing on startup!", file=sys.stderr)
        print("[-] Please ensure they are defined in your environment or a .env file.", file=sys.stderr)
        sys.exit(1)
        
    agent = DockerWatcher()
    agent.start_monitoring()