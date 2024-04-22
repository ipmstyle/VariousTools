#!/bin/python3
# author : ipmstyle <ipmstyle@gmail.com>

import os
import cv2
import io
import schedule, time
from datetime import datetime

from minio import Minio
from minio.error import InvalidResponseError
from minio.commonconfig import Tags

from DatabaseManager import DatabaseManager
from webcam_logger import Logger
from dotenv import load_dotenv


logger = Logger()

load_dotenv()
MINIO_HOST = os.getenv("MINIO_HOST", default=None)
MINIO_PORT = os.getenv("MINIO_PORT", default=None)
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", default=None)
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", default=None)
MINIO_BUCKET = os.getenv("MINIO_BUCKET", default=None)

def get_current_time():
    datetime_str = datetime.now().strftime("%Y%m%d%H%M%S")

    return datetime_str

def insert_DB(data, now_datetime):
    now_date = now_datetime[:8]
    now_time = now_datetime[8:]
    now_hour = now_datetime[8:10]

    conn = DatabaseManager()

    query = f"""INSERT INTO job_mst 
                (detect_dt, detect_time, detect_datetime)
                VALUES 
                ('{now_date}', '{now_time}', '{now_datetime}');
                """
    conn.execute_query(query)

    query = f"""INSERT INTO job_det 
                (detect_dt, detect_time, img_seq, img_nm, detect_datetime)
                VALUES 
                ('{now_date}', '{now_time}', 1, '{data.object_name}', '{now_datetime}');
                """
    conn.execute_query(query)

    conn.disconnect()

    logger.log_info(f'{data.object_name} to MySQL')


def upload_minio(minio_client, bucket_name, object_name, data, tags=None):
    try:
        result = minio_client.put_object(
                                    bucket_name, object_name, data, len(data.getvalue()), 
                                    content_type="image/jpg", 
                                    metadata={"project": "snct"},
                                    tags=tags)
        return result
    except InvalidResponseError as err:
        logger.log_error(f'Error: {err}')
        return None


def put_object(object_bytesIO):

    now_datetime = get_current_time()
    now_date = now_datetime[:8]
    now_hour = now_datetime[8:10]

    object_year = now_date[:4]
    object_month = now_date[4:6]
    object_day = now_date[6:8]

    minio_server = f'{MINIO_HOST}:{MINIO_PORT}'
    minio_access_key = MINIO_ACCESS_KEY
    minio_secret_key = MINIO_SECRET_KEY
    minio_bucket_name = MINIO_BUCKET
    minio_object_name = f'{now_datetime}.jpg'

    minio_object_path = f'/tech-lab/{object_year}/{object_month}/{object_day}/'

    minio_tags = Tags(for_object=True)
    minio_tags['location'] = 'GURO'
    minio_tags['site'] = 'ohkyung'
    minio_tags['area'] = 'tech-lab'
    minio_tags['zone'] = 'test server display'
    minio_tags['device'] = 'webcam'
    minio_tags['datetime'] = now_datetime
    minio_tags['date'] = now_date
    minio_tags['hour'] = now_hour

    minio_client = Minio(minio_server,
        access_key=minio_access_key,
        secret_key=minio_secret_key,
        secure=False
    )

    result = upload_minio(minio_client, minio_bucket_name, minio_object_path+minio_object_name, object_bytesIO, tags=minio_tags)
    if result is not None:
        msg = f'created {result.object_name} object; etag: {result.etag}, version-id: {result.version_id}'
        logger.log_info(f'{msg} to min.io')
    else:
        logger.log_error(f'{result.object_name} is None')

    return result, now_datetime


def get_object_info(info):
    minio_server = f'{MINIO_HOST}:{MINIO_PORT}'
    minio_access_key = MINIO_ACCESS_KEY
    minio_secret_key = MINIO_SECRET_KEY
    minio_bucket_name = MINIO_BUCKET

    minio_client = Minio(minio_server,
        access_key=minio_access_key,
        secret_key=minio_secret_key,
        secure=False
    )

    result = minio_client.stat_object(minio_bucket_name, info.object_name)

    return result

def get_image(camera_index=0):
    cam = cv2.VideoCapture(camera_index)

    if not cam.isOpened():
        logger.log_error('Error: web cam is not opened.')
        return

    ret, frame = cam.read()

    if ret:
        _, buffer = cv2.imencode('.jpg', frame)
        image_bytesio = io.BytesIO(buffer.tobytes())
        logger.log_info('get image')
    else:
        logger.log_error('Error: Failed to capture an image.')

        return False

    cam.release()
    return image_bytesio


def main():
    webcam_index = 0

    # Get data from webcam
    image_bytesIO = get_image(webcam_index)

    if image_bytesIO:
        # Data input to min.io 
        result, now_datetime = put_object(image_bytesIO)

        # Data input to MySQL
        insert_DB(result, now_datetime)

        # Date verify from min.io
        object_info = get_object_info(result)
        if object_info is not None:
            logger.log_info(f'object_stat : {object_info.last_modified}')
        else:
            logger.log_error(f'{result.object_name}')

if __name__ == "__main__":
    schedule.every(1).minutes.do(main)
    # schedule.every(1).seconds.do(main)

    while True:
        schedule.run_pending()
        time.sleep(5)
