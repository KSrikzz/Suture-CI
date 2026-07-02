import docker
import os
import sys
from core.orchestrator import SutureBrain
from dotenv import load_dotenv

class DockerWatcher:
    def __init__(self):
        load_dotenv()
        try:
            self.client = docker.from_env()
        except Exception as e:
            print(f"[-] Error: Could not initialize Docker client (is Docker running?): {e}", file=sys.stderr)
            sys.exit(1)
        
        try:
            self.brain = SutureBrain()
        except Exception as e:
            print(f"[-] Error: Could not initialize SutureBrain: {e}", file=sys.stderr)
            sys.exit(1)

    def start_monitoring(self):
        print("[*] Suture_CI Watcher active. Monitoring all container exits...")

        try:
            for event in self.client.events(decode=True):
                if event.get('Action') in ['die', 'oom']:
                    actor = event.get('Actor', {})
                    attrs = actor.get('Attributes', {})
                    
                    container_name = attrs.get('name', 'unknown')
                    exit_code = int(attrs.get('exitCode', 0))

                    if exit_code != 0:
                        print(f"\n[!] CRASH DETECTED: {container_name} (Code: {exit_code})")
                        
                        try:
                            container_id = event['id']
                            container = self.client.containers.get(container_id)
                            raw_logs = container.logs().decode('utf-8')
                        except Exception as e:
                            print(f"[!] Error fetching logs for container {container_name}: {e}")
                            continue

                        print("[*] Extracting error context and sending to Brain...")
                        try:
                            self.brain.run_healing_cycle(raw_logs, "tests/app.py")
                        except Exception as e:
                            print(f"[!] Error during healing cycle: {e}")
        except KeyboardInterrupt:
            print("\n[*] Stopping Watcher...")
            sys.exit(0)
        except Exception as e:
            print(f"[-] Critical watcher error: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    watcher = DockerWatcher()
    watcher.start_monitoring()