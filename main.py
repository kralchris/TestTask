"""
Test Task - synchronization of two folders

Implementation of a program that synchronizes two folders

@author: Kristijan <kristijan.sarin@gmail.com>
"""

import os
import shutil
import argparse
import hashlib
import time
from tools import Tools


# --------------------------------------------------------------------------------------------------------------
# improvement and error handling:
# --------------------------------------------------------------------------------------------------------------

class Operations:
    @staticmethod
    def md5(file_path):
        md5_hash = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()

    @staticmethod
    @Tools.io_retry(max_retries=3, delay=1)
    def robust_makedirs(path):
        os.makedirs(path, exist_ok=True)

    @staticmethod
    @Tools.io_retry(max_retries=3, delay=1)
    def robust_copy2(source, destination):
        shutil.copy2(source, destination)

    @staticmethod
    @Tools.io_retry(max_retries=5, delay=2)
    def robust_remove(path):
        os.remove(path)

    @staticmethod
    @Tools.io_retry(max_retries=5, delay=2)
    def robust_rmtree(path):
        shutil.rmtree(path)

    @staticmethod
    def sync_folders_logic(source, replica, logger):
        if not os.path.exists(replica):
            Operations.robust_makedirs(replica)
            logger.info(f"Created new directory: {replica}")

        source_files = set()

        for root, dirs, files in os.walk(source):
            relative_path = os.path.relpath(root, source)
            replica_root = os.path.normpath(
                os.path.join(replica, relative_path))

            if not os.path.exists(replica_root):
                Operations.robust_makedirs(replica_root)

            for file in files:
                source_file = os.path.normpath(os.path.join(root, file))
                replica_file = os.path.normpath(
                    os.path.join(replica_root, file))

                source_files.add(replica_file)

                if not os.path.exists(replica_file) or Operations.md5(source_file) != Operations.md5(replica_file):
                    Operations.robust_copy2(source_file, replica_file)
                    logger.info(
                        f"Copied file: {source_file} to {replica_file}")

        for root, dirs, files in os.walk(replica, topdown=False):
            for name in files:
                replica_file = os.path.normpath(os.path.join(root, name))
                if replica_file not in source_files:
                    Operations.robust_remove(replica_file)
                    logger.info(f"File deleted: {replica_file}")

            for name in dirs:
                replica_dir = os.path.normpath(os.path.join(root, name))
                if not os.path.exists(os.path.normpath(os.path.join(source, os.path.relpath(replica_dir, replica)))):
                    Operations.robust_rmtree(replica_dir)
                    logger.info(f"Directory deleted: {replica_dir}")


# --------------------------------------------------------------------------------------------------------------
# main:
# --------------------------------------------------------------------------------------------------------------

class MainApplication:
    @staticmethod
    def main():
        parser = argparse.ArgumentParser(
            description="Synchronize two folders.")
        parser.add_argument("source", help="Source path")
        parser.add_argument("replica", help="Replica path")
        parser.add_argument("interval", type=int, help="Interval in seconds")
        parser.add_argument("log_file", help="Log path")

        args = parser.parse_args()

        logger = Tools.setup_logger(args.log_file)
        logger.info("Starting sync process...")

        while True:
            Operations.sync_folders_logic(args.source, args.replica, logger)
            time.sleep(args.interval)


if __name__ == "__main__":
    MainApplication.main()
