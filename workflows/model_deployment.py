import os
import typing
import subprocess

from aws_logger import logger
from data_pull import data_pull


def deployment():
    logger.info(f"Model approved, start deployment")

    # deploy by seldon (This is only support on local excution)
    current_dir = os.path.dirname(__file__)
    script_path = os.path.join(current_dir, "..", "seldon_deployment.sh")
    subprocess.run(["sh", script_path])


def discard() -> int:
    logger.info(f"Model not approved, will not trigger deployment")
    return -1


def deployment_check(accuracy:float) -> bool:
    if accuracy > 0.6:
        return True
    else:
        return False


# if __name__=="__main__":
