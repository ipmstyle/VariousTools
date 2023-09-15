import os
import shutil

def classify_files_by_keyword(keyword, target_folder):
    # 현재 실행중인 스크립트의 경로를 가져옴
    script_path = os.path.dirname(os.path.abspath(__file__))
    # 분류할 폴더 이름 생성
    folder_name = os.path.join(script_path, target_folder)
    
    # 폴더가 존재하지 않으면 생성
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # 현재 폴더 내의 파일들을 탐색
    for filename in os.listdir(script_path):
        if os.path.isfile(filename):
            # 파일 이름에 특정 키워드가 포함되어 있다면 해당 폴더로 이동
            if keyword in filename:
                src_path = os.path.join(script_path, filename)
                dst_path = os.path.join(folder_name, filename)
                shutil.move(src_path, dst_path)

if __name__ == "__main__":
    # 'C' 폴더에 'C'가 들어간 파일을 분류
    classify_files_by_keyword("C", "C")

    # 'D' 폴더에 'D'가 들어간 파일을 분류
    classify_files_by_keyword("D", "D")