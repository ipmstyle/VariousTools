import os

def count_matching_files(directory):
    matching_count = 0
    jpg_only_count = 0
    txt_only_count = 0

    for root, dirs, files in os.walk(directory):
        jpg_found = False
        txt_found = False

        for file in files:
            if file.lower().endswith(".jpg"):
                jpg_found = True
                # 해당 jpg 파일의 이름과 같은 이름의 txt 파일이 있는지 확인
                txt_file = os.path.join(root, file[:-4] + ".txt")
                if os.path.isfile(txt_file):
                    txt_found = True

            if jpg_found and txt_found:
                matching_count += 1
            elif jpg_found and not txt_found:
                jpg_only_count += 1
            elif not jpg_found and txt_found:
                txt_only_count += 1

    return matching_count/2, jpg_only_count, txt_only_count

# 현재 디렉토리에서 검사 시작
matching_count, jpg_only_count, txt_only_count = count_matching_files(os.getcwd())

print(f"같은 이름의 jpg와 txt 파일이 있는 파일 수: {matching_count} 개")
print(f"jpg만 있는 파일 수: {jpg_only_count} 개")
print(f"txt만 있는 파일 수: {txt_only_count} 개")
