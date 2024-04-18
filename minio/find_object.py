#!/bin/python3
# author : ipmstyle <ipmstyle@gmail.com>

import os
import schedule, time
import argparse
from datetime import datetime

from minio import Minio
from minio.error import InvalidResponseError
from minio.commonconfig import Tags

from webcam_logger import Logger


logger = Logger()


def find_object(info):
    minio_server = '125.7.128.33:9101'
    minio_access_key = 'wCfC4WyUmThpuaWlEevH'
    minio_secret_key = 'krDNbreeiNdqoYwiRIzvllVqFGXJm7kpBz1eImDj'
    minio_bucket_name = 'snct-data'

    minio_client = Minio(minio_server,
        access_key=minio_access_key,
        secret_key=minio_secret_key,
        secure=False
    )

    result = minio_client.stat_object(minio_bucket_name, info)

    return result


def main():
    parser = argparse.ArgumentParser(description="Custom find function")
    parser.add_argument("-f", "--file", help="Specify a file to search in")
    parser.add_argument("-c", "--count", type=int, help="Number of retries if find_() response is None")

    args = parser.parse_args()

    if args.file and args.count:
        for _ in range(args.count):
            try:
                result = find_object(args.file)
            except:
                result = None

            if result is not None:
                print(f"Found: {result}")
                break
            else:
                print("No result found.")

            time.sleep(30)

    elif args.file:
        result = find_object(args.file)
        if result is not None:
            print(f"Found: {result}")
        else:
            print("No result found.")


if __name__ == "__main__":
    main()
