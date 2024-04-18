#!/bin/python3
# author : ipmstyle <ipmstyle@gmail.com>

import os, sys
import schedule, time
from datetime import datetime

from minio import Minio
from minio.error import InvalidResponseError
from minio.commonconfig import Tags

from DatabaseManager import DatabaseManager
from find_logger import Logger


logger = Logger()

def get_current_time():
    datetime_str = datetime.now().strftime("%Y%m%d%H%M%S")

    return datetime_str

def get_last_one_from_DB():
    conn = DatabaseManager()

    query = f"""
            SELECT img_nm 
            FROM cds_snct.job_det 
            WHERE detect_datetime > now() - INTERVAL 1 DAY 
            ORDER BY detect_datetime DESC
            LIMIT 1;
            """
    result = conn.execute_return_result(query)
    # print(result[0][0])

    conn.disconnect()

    return result[0][0]


def get_object_info(info):
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

def get_object(info):
    minio_server = '125.7.128.33:9101'
    minio_access_key = 'wCfC4WyUmThpuaWlEevH'
    minio_secret_key = 'krDNbreeiNdqoYwiRIzvllVqFGXJm7kpBz1eImDj'
    minio_bucket_name = 'snct-data'

    minio_client = Minio(minio_server,
        access_key=minio_access_key,
        secret_key=minio_secret_key,
        secure=False
    )

    filename = info.split('\'')[-1]
    try:
        response = minio_client.get_object(minio_bucket_name, filename)
        with open(filename, "wb") as file:
            for data in response.stream(32 * 1024):
                file.write(data)
        print("이미지 다운로드 완료: downloaded_image.jpg")
    except Exception as e:
        print(f"오류 발생: {e}")


def main():
    object = get_last_one_from_DB()
    result = get_object_info(object)
    print(result.last_modified, result.size)

    get_object(object)

if __name__ == "__main__":
    main()
