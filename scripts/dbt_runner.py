import os
import subprocess

def main():
    project_dir = "/tmp/project"
    profiles_dir = "/tmp/profiles"

    # Download dbt project from S3
    os.system(f"aws s3 cp s3://vigia-data-lake-dl-artifacts-dbt-dev-a14b31t/dbt_project/ {project_dir} --recursive")

    # Run dbt
    subprocess.run(
        ["dbt", "run", "--profiles-dir", profiles_dir, "--project-dir", project_dir],
        check=True
    )