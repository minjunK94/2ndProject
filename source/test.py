import os
import json
import zipfile
import pandas as pd

# 데이터 폴더 설정
base_folder = r"F:\건강관리를 위한 음식 이미지"

# 1️⃣ ZIP 파일 압축 해제
zip_files = []
for folder in ["Training", "Validation"]:
    folder_path = os.path.join(base_folder, folder)
    if os.path.exists(folder_path):
        zip_files.extend(
            [(folder, os.path.join(folder_path, f)) for f in os.listdir(folder_path) if f.endswith(".zip")])

total_files = len(zip_files)
if total_files == 0:
    print("🔍 압축 파일이 없습니다. 작업을 종료합니다.")
else:
    print(f"📦 총 {total_files}개의 ZIP 파일을 처리합니다.")

for idx, (folder, zip_path) in enumerate(zip_files, start=1):
    extract_folder = os.path.join(base_folder, folder, "Extracted")
    os.makedirs(extract_folder, exist_ok=True)

    zip_name = os.path.basename(zip_path)
    print(f"[{idx}/{total_files}] ⏳ {zip_name} 압축 해제 중...")

    if not zipfile.is_zipfile(zip_path):
        print(f"⚠️ {zip_name} 은(는) 손상된 ZIP 파일입니다. 건너뜁니다.")
        continue

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for member in zip_ref.namelist():
            try:
                safe_path = os.path.normpath(os.path.join(extract_folder, member))
                if not safe_path.startswith(extract_folder):
                    print(f"🚨 경고: 위험한 경로 탐지 {member}")
                    continue
                zip_ref.extract(member, extract_folder)
            except OSError as e:
                print(f"⚠️ 파일 추출 중 오류 발생: {e}")
                continue
        print(f"✅ {zip_name} 압축 해제 완료 → {extract_folder}")

print("📂 모든 ZIP 파일 해제 및 정리 완료!")

# 2️⃣ JSON → CSV 변환
json_files = []
for folder in ["Training", "Validation"]:
    extract_folder = os.path.join(base_folder, folder, "Extracted")
    for root, _, files in os.walk(extract_folder):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))

print(f"🔍 총 {len(json_files)}개의 JSON 파일을 찾았습니다.")

all_data = []
for json_path in json_files:
    with open(json_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    for item in json_data:
        filtered_item = {
            "Name": item.get("Name", "").strip(),
            "Serving Size": item.get("Serving Size", ""),
            "당류(g)": item.get("당류(g)", "")
        }
        all_data.append(filtered_item)

    os.remove(json_path)  # 변환 후 원본 JSON 삭제

# CSV 저장
json_csv_path = os.path.join(base_folder, "json_food_data.csv")
df_json = pd.DataFrame(all_data)
df_json.to_csv(json_csv_path, index=False, encoding="utf-8-sig")
print(f"✅ JSON 데이터를 CSV로 저장 완료: {json_csv_path}")