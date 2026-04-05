import logging
import subprocess
import os
import shutil

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
        logger.info("Starting Drift Detection")

        # Paths
        terraform_src = "/var/task/terraform"
        terraform_dest = "/tmp/terraform"
        working_dir = "/tmp/tf"

        # Copy terraform binary
        if not os.path.exists(terraform_dest):
            shutil.copy(terraform_src, terraform_dest)
            os.chmod(terraform_dest, 0o755)

        # Prepare working directory
        if os.path.exists(working_dir):
            shutil.rmtree(working_dir)

        shutil.copytree("/var/task", working_dir)

        # Terraform commands
        run_command(f"{terraform_dest} init -input=false", cwd=working_dir)

        plan_output = run_command(f"{terraform_dest} plan -no-color", cwd=working_dir)

        # Check drift
        if "No changes" in plan_output:
            logger.info("No Drift Detected ✅")

            return {
                "statusCode": 200,
                "body": "No drift detected"
            }

        else:
            logger.info("Drift Detected ⚠️ → Applying Fix")

            apply_output = run_command(
                f"{terraform_dest} apply -auto-approve -input=false",
                cwd=working_dir
            )

            return {
                "statusCode": 200,
                "body": "Drift detected and remediated"
            }

    except Exception as e:
        logger.error(f"Error: {str(e)}")

        return {
            "statusCode": 500,
            "body": str(e)
        }
