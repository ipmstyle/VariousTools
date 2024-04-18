#!/usr/bin/env python
# get_gif.py
# ===
# - min.io client test
# - Create a gif from the bucket object
#
# author : ipmstyle <ipmstyle@gmail.com>

import os
import time
from datetime import datetime
from dotenv import load_dotenv
from io import BytesIO
import imageio
from PIL import Image

from minio import Minio
from DatabaseManager import DatabaseManager

# SERVER = '127.0.0.1:9101'
# SERVER = '125.7.128.33:9101'
# ACCESS_KEY = 'wCfC4WyUmThpuaWlEevH'
# SECRET_KEY = 'krDNbreeiNdqoYwiRIzvllVqFGXJm7kpBz1eImDj'
# BUCKET = 'snct-data'

def img_compress(img):
    img =Image.fromarray(img)

    image_format = 'JPEG'
    output_img = BytesIO()
    img.save(output_img, format=image_format, quality=30)
    img.seek(0)

    output_img = imageio.imread(output_img)

    return output_img

def get_mysql(request_date):
    conn = DatabaseManager()

    query = f"""
                SELECT * FROM job_det WHERE detect_dt='{request_date}'
    """
    ## job_det
    #`detect_dt` VARCHAR(8) NOT NULL COLLATE 'utf8_general_ci',
	#`detect_time` VARCHAR(6) NOT NULL COLLATE 'utf8_general_ci',
	#`site_no` INT(2) NOT NULL,
	#`ch_num` INT(1) NOT NULL,
	#`ch_gbn` INT(1) NOT NULL,
	#`img_seq` INT(2) NOT NULL,
	#`yt_num` VARCHAR(3) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	#`detect_yn` INT(1) NULL DEFAULT NULL,
	#`img_nm` VARCHAR(65) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	#`det_img_nm` VARCHAR(65) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	#`ocr_img_nm` VARCHAR(65) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	#`send_yn` INT(1) NULL DEFAULT NULL,
	#`detect_datetime` DATETIME NULL DEFAULT NULL

    result = conn.execute_return_result(query)

    conn.disconnect()

    res_list = []

    for res in result:
        img_nm = res[8]
        res_list.append(img_nm)
    
    return res_list

def get_minio(obj_list):
    load_dotenv()

    HOST = os.getenv("S3_HOST", default=False)
    ACCESS_KEY = os.getenv("S3_ACCESS_KEY", default=False)
    SECRET_KEY = os.getenv("S3_SECRET_KEY", default=False)
    BUCKET = os.getenv("S3_NAME", default=False)

    init_time = time.time()

    client = Minio(HOST,
                access_key=ACCESS_KEY,
                secret_key=SECRET_KEY,
                secure=False
    )

    connect_time = time.time()

    minio_connection_time = connect_time - init_time

    images = []
    get_bucket_time, frame_to_byte_time, imgio_time, minio_time = [], [], [], []
    for obj_name in obj_list:
        img_byte = BytesIO()

        first_time = time.time()

        object = client.get_object(BUCKET, obj_name)

        second_time = time.time()

        for frame in object.stream(32*1024):
            img_byte.write(frame)

        third_time = time.time()

        img_byte.seek(0)
        image = imageio.imread(img_byte)

        fourth_time = time.time()

        get_bucket_time.append(second_time - first_time)
        frame_to_byte_time.append(third_time - second_time)
        imgio_time.append(fourth_time - third_time)
        minio_time.append(fourth_time - first_time)

        image = img_compress(image)
        images.append(image)
    gif_start_time = time.time()

    imageio.mimsave('output.gif', images, duration=0.01)

    gif_end_time = time.time()
    minio_processing_time = gif_start_time - connect_time
    gif_processing_time = gif_end_time - gif_start_time

    print(f'### Get images : {len(obj_list)}')
    print(f'min.io processing time : {minio_processing_time}')
    print(f'  - min.io connection time : {minio_connection_time}')
    print(f'  - Bucket Time : avg({ sum(get_bucket_time)/len(get_bucket_time) }), MAX({max(get_bucket_time)}), MIN({min(get_bucket_time)})')
    print(f'  - Frame to Byte Time : avg({ sum(frame_to_byte_time)/len(frame_to_byte_time) }), MAX({max(frame_to_byte_time)}), MIN({min(frame_to_byte_time)})')
    print(f'  - imgio Time : avg({ sum(imgio_time)/len(imgio_time) }), MAX({max(imgio_time)}), MIN({min(imgio_time)})')
    print(f'  - Min.io Time : avg({ sum(minio_time)/len(minio_time) }), MAX({max(minio_time)}), MIN({min(minio_time)})')
    print(f'gif processing time : {gif_processing_time}')


    # objects = client.list_objects(BUCKET, prefix='snct-data/2024/tech_lab/202403', recursive=True)
    # objects = client.list_objects(BUCKET, prefix='20240108', recursive=True)
    # for obj in objects:
    #     print(obj.object_name)

    # object = client.get_object(BUCKET, '/2024/tech-lab/20240306084806.jpg')
    # # print(object)
    # with open('test.jpg', 'wb') as f:
    #     for data in object:
    #         f.write(data)
    # f.close()
   
def main():
    now_date = datetime.now().strftime("%Y%m%d")

    start_time = time.time()
    obj_list = get_mysql(now_date)
    mid_time = time.time()

    get_minio(obj_list)
    end_time = time.time()

    processing_time = end_time - start_time
    mysql_time = mid_time - start_time
    minio_time = end_time - mid_time

    print(f'Total processing time : {processing_time}')
    print(f'   - MySQL time : {mysql_time}')
    print(f'   - minio time : {minio_time}')

if __name__ == "__main__":
   main()