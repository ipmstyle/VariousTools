import os
import pandas as pd
import shutil

# 엑셀 파일 읽기
file_path = 'data.xlsx'
df = pd.read_excel(file_path)

# Y/N 열 추가 (이미 존재하면 생략 가능)
if 'Y/N' not in df.columns:
    df['Y/N'] = ''

# data 폴더가 존재하지 않으면 생성
if not os.path.exists('data'):
    os.makedirs('data')

# img_nm 열의 파일 경로를 확인하고 파일 복사
for index, row in df.iterrows():
    img_path = row['img_nm']
    if os.path.exists(img_path):
        df.at[index, 'Y/N'] = 'O'
        # 파일이 존재하면 data 폴더로 복사
        shutil.copy(img_path, 'data/')
    else:
        df.at[index, 'Y/N'] = 'X'

# 엑셀 파일 업데이트
df.to_excel(file_path, index=False)

print("작업이 완료되었습니다.")
