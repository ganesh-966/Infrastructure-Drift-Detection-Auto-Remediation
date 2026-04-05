import logging
import subprocess
import os

# Logger setup
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def run_command(command, cwd=None):
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True,
        cwd=cwd
    )

    stdout, stderr = process.communicate()

    if process.returncode != 0:
        logger.error(stderr)
        raise Exception(stderr)

    logger.info(stdout)
    return stdout


def lambda_handler(event, context):
    try:
        logger.info("Starting Terraform Drift Detection")

        # Copy terraform to /tmp
        terraform_src = "/var/task/terraform"
        terraform_dest = "/tmp/terraform"

        if not os.path.exists(terraform_dest):
            run_command(f"cp {terraform_src} {terraform_dest}")
            run_command(f"chmod +x {terraform_dest}")

        # Run terraform
        output = run_command("/tmp/terraform version", cwd="/tmp")

        return {
            "statusCode": 200,
            "body": output
        }

    except Exception as e:
        logger.error(f"Execution failed: {str(e)}")

        return {
            "statusCode": 500,
            "body": str(e)
        }
