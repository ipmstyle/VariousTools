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


def get_current_time():
    datetime_str = datetime.now().strftime("%Y%m%d%H%M%S")
    current_time_file = f"{datetime_str}.jpg"

    return current_time_file

def upload_minio(minio_client, bucket_name, object_name, data, tags=None):
    try:
        # minio_client.put_object(bucket_name, object_name, data, len(data.getvalue()))
        minio_client.put_object(
                bucket_name, object_name, data, len(data.getvalue()), 
                content_type="image/jpg", 
                metadata={"project": "snct"},
                tags=tags)
    except InvalidResponseError as err:
        print(f"Error: {err}")

def put_image(object_bytesIO):
    minio_server = <IP:PORT>
    minio_access_key = <ACCESS KEY>
    minio_secret_key = <SECRET KEY>
    minio_bucket_name = <BUCKET>
    minio_object_name = get_current_time()

    minio_tags = Tags(for_object=True)
    minio_tags['location'] = 'GURO'
    minio_tags['site'] = 'ohkyung'
    minio_tags['area'] = 'tech-lab'
    minio_tags['zone'] = 'test server display'
    minio_tags['device'] = 'webcam'
    # minio_tags = {
    #     'location': 'GURO',
    #     'site': 'ohkyung',
    #     'area': 'tech-lab',
    #     'zone': 'test server display',
    #     'device': 'webcam'
    # }

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
