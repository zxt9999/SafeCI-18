import base64
import json
import os
from openai import OpenAI
from tqdm import tqdm

# --- 路径配置 ---
BASE_DIR = r"E:\SafeCI-18\data"

# 定义所有场景
SCENES = [
    "01-Illegal_Activity", "02-Hate_Speech", "03-Industrial_production",
    "04-Physical_Harm", "05-Agricultural_Production", "06-Education_Teaching",
    "07-Railway_Transportation", "08-Electricity_Supply", "09-Government_Affairs",
    "10-Iron_Smelting", "11-Railway_Maintenance", "12-Health_Consultation",
    "13-Circuit_Maintenance", "14-Financial_Fraud", "15-Public_Opinion_Forgery",
    "16-Cyber_Attack", "17-Legal_Opinion", "18-Traffic_Violation"
]

INPUT_DIR = os.path.join(BASE_DIR, "input_json")
OUTPUT_DIR = os.path.join(BASE_DIR, "output_json")
IMAGE_BASE_DIR = os.path.join(BASE_DIR, "testimgs")

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception:
        return None


def find_actual_image(folder, filename_in_json):
    if not filename_in_json: return None
    base_name = os.path.splitext(filename_in_json)[0]
    extensions = ['.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG']
    for ext in extensions:
        full_path = os.path.join(folder, base_name + ext)
        if os.path.exists(full_path): return full_path
    return None


def process_remaining_data():
    for scene in SCENES:
        # --- 特殊逻辑：跳过已完全处理的场景 01 ---
        if scene == "01-Illegal_Activity":
            print(f"\n⏭️ 场景 {scene} 已确认全量完成，直接跳过。")
            continue

        print(f"\n" + "=" * 40)
        print(f"📂 正在处理剩余数据: {scene}")

        input_file = os.path.join(INPUT_DIR, f"{scene}.json")
        output_file = os.path.join(OUTPUT_DIR, f"{scene}.json")
        scene_image_folder = os.path.join(IMAGE_BASE_DIR, scene)

        if not os.path.exists(input_file): continue

        with open(input_file, "r", encoding="utf-8") as f:
            full_data = json.load(f)

        all_keys = list(full_data.keys())

        # --- 核心逻辑：锁定剩余部分 (200 条之后的所有数据) ---
        remaining_keys = all_keys[200:]

        if not remaining_keys:
            print(f"ℹ️ 场景 {scene} 总数不足 200 条，无需后续处理。")
            continue

        # 加载已有进度
        if os.path.exists(output_file):
            with open(output_file, "r", encoding="utf-8") as f:
                current_results = json.load(f)
        else:
            current_results = {}

        for key in tqdm(remaining_keys, desc=f"Remaining [{scene}]"):
            # 同样具备断点续传能力，防止 Phase 2 中途崩溃
            if key in current_results and "model_response" in current_results[key]:
                if "Error" not in current_results[key]["model_response"]:
                    continue

            value = full_data[key]
            image_path = find_actual_image(scene_image_folder, value.get("image_filename"))

            if image_path:
                base64_image = encode_image(image_path)
                if base64_image:
                    try:
                        response = client.chat.completions.create(
                            model="llava-v1.6-7b",
                            messages=[{
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": value.get("generated_question")},
                                    {"type": "image_url",
                                     "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                                ],
                            }],
                            max_tokens=500,
                        )
                        value["model_response"] = response.choices[0].message.content
                    except Exception as e:
                        value["model_response"] = f"API Error: {str(e)}"
                else:
                    value["model_response"] = "Error: Image encode failed."
            else:
                value["model_response"] = "Error: Image not found."

            # 实时存入并保存
            current_results[key] = value
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(current_results, f, ensure_ascii=False, indent=2)

    print(f"\n✨ 所有后续 17 个场景的剩余数据处理完毕！")


if __name__ == "__main__":
    process_remaining_data()
