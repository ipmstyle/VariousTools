#!/bin/python3
# author : ipmstyle <ipmstyle@gmail.com>

import os
import cv2
import io
import schedule, time
from datetime import datetime

from minio import Minio
from minio.error import InvalidResponseError


def get_current_time():
    datetime_str = datetime.now().strftime("%Y%m%d%H%M%S")
    current_time_file = f"{datetime_str}.jpg"

    return current_time_file

def upload_minio(minio_client, bucket_name, object_name, data, tags=None):
    try:
        minio_client.put_object(bucket_name, object_name, data, len(data.getvalue()))
    except InvalidResponseError as err:
        print(f"Error: {err}")

def put_image(object_bytesIO):
    minio_server = '125.7.128.33:9101'
    minio_access_key = 'X8y8Fs2XkhW9HbmNlaNg'
    minio_secret_key = 'WOi1okr4lOttWi76hza2Ub47PilMJ66Y4iwlDc2h'
    minio_bucket_name = 'snct-data'
    minio_object_name = get_current_time()

    minio_tags = {
        'location': 'ohkyung',
        'device': 'webcam'
    }

    minio_client = Minio(minio_server,
        access_key=minio_access_key,
        secret_key=minio_secret_key,
        secure=False
    )

    upload_minio(minio_client, minio_bucket_name, minio_object_name, object_bytesIO, tags=minio_tags)


def get_image(camera_index=0):
    cam = cv2.VideoCapture(camera_index)

    if not cam.isOpened():
        print("Error: web cam is not opened.")
        return

    ret, frame = cam.read()

    if ret:
        _, buffer = cv2.imencode('.jpg', frame)
        image_bytesio = io.BytesIO(buffer.tobytes())
    else:
        print("Error: Failed to capture an image.")

        return False

    cam.release()
    return image_bytesio

def main():
    webcam_index = 0

    image_bytesIO = get_image(webcam_index)

    if image_bytesIO:
        put_image(image_bytesIO)

if __name__ == "__main__":
    schedule.every(1).minutes.do(main)

    while True:
        schedule.run_pending()
        time.sleep(5)
