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
# --- 修改点 1：输出文件夹改为 internvl 专用 ---
OUTPUT_DIR = os.path.join(BASE_DIR, "output_json_internvl")
IMAGE_BASE_DIR = os.path.join(BASE_DIR, "testimgs")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- 客户端初始化 ---
# 请确保 LM Studio 中已经加载了 InternVL 模型
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


def process_internvl_test():
    for scene in SCENES:

        print(f"\n" + "=" * 40)
        print(f"📂 InternVL 正在处理场景: {scene}")

        input_file = os.path.join(INPUT_DIR, f"{scene}.json")
        output_file = os.path.join(OUTPUT_DIR, f"{scene}.json")
        scene_image_folder = os.path.join(IMAGE_BASE_DIR, scene)

        if not os.path.exists(input_file): continue

        with open(input_file, "r", encoding="utf-8") as f:
            full_data = json.load(f)

        all_keys = list(full_data.keys())

        keys_to_process = all_keys[:]

        if os.path.exists(output_file):
            with open(output_file, "r", encoding="utf-8") as f:
                current_results = json.load(f)
        else:
            current_results = {}

        for key in tqdm(keys_to_process, desc=f"InternVL [{scene}]"):
            if key in current_results and "model_response" in current_results[key]:
                if "Error" not in current_results[key]["model_response"]:
                    continue

            value = full_data[key]
            image_path = find_actual_image(scene_image_folder, value.get("image_filename"))

            if image_path:
                base64_image = encode_image(image_path)
                if base64_image:
                    try:
                        # --- 修改点 2：根据 LM Studio 实际加载的模型 ID 填写 ---
                        response = client.chat.completions.create(
                            model="internvl",  # 或者你在 LM Studio 侧边栏看到的具体 ID
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

            current_results[key] = value
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(current_results, f, ensure_ascii=False, indent=2)

    print(f"\n✨ InternVL 批量测试完成！结果存放在: {OUTPUT_DIR}")


if __name__ == "__main__":
    process_internvl_test()
