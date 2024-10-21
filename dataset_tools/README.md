# VariousTools

## dataset_tools

### countDataset_per_sites.py

  - 데이터셋의 Site 별 jpg 파일 숫자 세기
  - line 12 폴더명 수정 후 실행

### countFiles.py

  - 데이터셋 쌍(jpg+txt)이 있는지 확인

### file2move.py

  - 파일 분류
    - C : 컨테이너용 이미지
    - D : 콘 감지용 이미지
    - T : 콘 감지된 이미지 (결과)
    - O : OCT 이미지 (결과)

### move2cd.pt

  - 파일 분류
    - C : 컨테이너용 이미지
    - D : 콘 감지용 이미지

### SplitFiles.py

  - jpg 파일을 1,000개씩 폴더로 나눔

### copyFile.py

  - `data.xlsx` 파일에서 `img_nm` 경로의 파일을 현재 위치 `data` 폴더로 복사
  - `data.xlsx` 에 `Y/N` 열이 있으면, O/X 로 파일 복사 결과 출력