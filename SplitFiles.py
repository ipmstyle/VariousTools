import os
import shutil

INIT_NUM = 0

# 현재 디렉토리에서 jpg 파일 찾기
jpg_files = [f for f in os.listdir('.') if os.path.isfile(f) and f.lower().endswith('.jpg')]

# 폴더 생성 및 파일 이동
for i, jpg_file in enumerate(jpg_files, start=1):
    folder_num = (i - 1) // 1000 + 1  # 폴더 번호 계산
    folder_num = folder_num + INIT_NUM
    #folder_name = str(folder_num).zfill(4)  # 폴더 번호를 네 자리 숫자로 변환
    folder_name = str(folder_num)

    # 폴더가 존재하지 않으면 생성
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # 파일 이동
    shutil.move(jpg_file, os.path.join(folder_name, jpg_file))

    # 1,000개씩 파일을 옮겼으면 새로운 폴더를 생성
    if i % 1000 == 0:
        folder_num += 1

print("작업 완료")
