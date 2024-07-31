import os

def count_files_by_prefix(directory, prefix, extension):
    count = 0
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.startswith(prefix) and filename.lower().endswith(extension):
                count += 1
    return count

# 경로 설정 (여기에 원하는 경로를 입력하세요)
target_directory = "D:\Git\SNCT_DATASET\Data of False Positive"

# 파일 확장자 설정 (예: jpg)
file_extension = ".jpg"

# 원하는 접두사 설정 (예: "01", "02", ...)
prefixes = ["01", "02", "03", "04"]

for prefix in prefixes:
    file_count = count_files_by_prefix(target_directory, prefix, file_extension)
    print(f"{prefix}로 시작하는 {file_extension} 파일 수: {file_count}개")

# 결과 출력 후 필요한 작업을 추가로 수행하시면 됩니다.
