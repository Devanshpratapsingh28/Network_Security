import os
import shlex
import subprocess


class s3sync():
    def sync_folder_to_s3(self, folder, aws_bucket_url):
        folder_path = os.path.abspath(folder)
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Local folder does not exist: {folder_path}")

        command = f"aws s3 sync {shlex.quote(folder_path)} {shlex.quote(aws_bucket_url)}"
        self._run_aws_command(command)

    def sync_folder_from_s3(self, folder, aws_bucket_url):
        folder_path = os.path.abspath(folder)
        os.makedirs(folder_path, exist_ok=True)

        command = f"aws s3 sync {shlex.quote(aws_bucket_url)} {shlex.quote(folder_path)}"
        self._run_aws_command(command)

    def _run_aws_command(self, command):
        completed = subprocess.run(command, shell=True, capture_output=True, text=True)
        if completed.returncode != 0:
            raise RuntimeError(
                f"AWS sync failed with exit code {completed.returncode}\n"
                f"Command: {command}\n"
                f"STDOUT: {completed.stdout}\n"
                f"STDERR: {completed.stderr}"
            )
