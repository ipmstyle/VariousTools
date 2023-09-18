import os

def get_jpg_and_txt_counts(directory):
    jpg_txt_counts = {}
    jpg_only_paths = []
    txt_only_paths = []
    txt_only_files = []

    for root, dirs, files in os.walk(directory):
        jpg_files = [file for file in files if file.lower().endswith(".jpg")]
        txt_files = [file for file in files if file.lower().endswith(".txt")]

        for jpg_file in jpg_files:
            txt_file = jpg_file[:-4] + ".txt"
            txt_path = os.path.join(root, txt_file)

            if os.path.isfile(txt_path):
                if root not in jpg_txt_counts:
                    jpg_txt_counts[root] = 1
                else:
                    jpg_txt_counts[root] += 1
            else:
                jpg_only_paths.append(os.path.join(root, jpg_file))

        for txt_file in txt_files:
            jpg_file = txt_file[:-4] + ".jpg"
            jpg_path = os.path.join(root, jpg_file)

            if not os.path.isfile(jpg_path):
                txt_only_paths.append(os.path.join(root, txt_file))
                txt_only_files.append(txt_file)

    return jpg_txt_counts, jpg_only_paths, txt_only_paths, txt_only_files

directory = os.getcwd()
jpg_txt_counts, jpg_only_paths, txt_only_paths, txt_only_files = get_jpg_and_txt_counts(directory)

print(f"각 폴더별로 같은 이름의 jpg와 txt 파일이 있는 경우:")
for folder, count in jpg_txt_counts.items():
    print(f"폴더 '{folder}' 에서 {count} 개의 쌍을 찾았습니다.")

print("\njpg 파일만 있는 경우:", len(jpg_only_paths))
for path in jpg_only_paths:
    print(path)

print("\ntxt 파일만 있는 경우:", len(txt_only_paths))
for path in txt_only_paths:
    print(path)
for file in txt_only_files:
    os.system("del %s" % file)
