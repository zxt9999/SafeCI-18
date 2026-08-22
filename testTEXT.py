import json
import os
from openai import OpenAI
from tqdm import tqdm

# --- 路径配置 ---
BASE_DIR = r"E:\MM-SafetyBench-main\data"

SCENES = [
    "01-Illegal_Activity", "02-Hate_Speech", "03-Industrial_production",
    "04-Physical_Harm", "05-Agricultural_Production", "06-Education_Teaching",
    "07-Railway_Transportation", "08-Electricity_Supply", "09-Government_Affairs",
    "10-Iron_Smelting", "11-Railway_Maintenance", "12-Health_Consultation",
    "13-Circuit_Maintenance", "14-Financial_Fraud", "15-Public_Opinion_Forgery",
    "16-Cyber_Attack", "17-Legal_Opinion", "18-Traffic_Violation"
]

INPUT_DIR = os.path.join(BASE_DIR, "input_json")
OUTPUT_DIR = os.path.join(BASE_DIR, "output_json_text_only")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


def run_processing(scene, keys_to_process, desc_prefix):
    """提取出的通用处理逻辑"""
    input_file = os.path.join(INPUT_DIR, f"{scene}.json")
    output_file = os.path.join(OUTPUT_DIR, f"{scene}.json")

    if not os.path.exists(input_file):
        return

    with open(input_file, "r", encoding="utf-8") as f:
        full_data = json.load(f)

    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            current_results = json.load(f)
    else:
        current_results = {}

    for key in tqdm(keys_to_process, desc=f"{desc_prefix} {scene}"):
        # 跳过已存在且非错误的回答
        if key in current_results and "text_only_response" in current_results[key]:
            if "Error" not in current_results[key]["text_only_response"]:
                continue

        # 确保 key 在原始数据中存在
        if key not in full_data:
            continue

        value = full_data[key]
        question = value.get("generated_question")

        try:
            response = client.chat.completions.create(
                model="llava-v1.6-7b",
                messages=[{"role": "user", "content": question}],
                max_tokens=500,
            )
            value["text_only_response"] = response.choices[0].message.content
        except Exception as e:
            value["text_only_response"] = f"API Error: {str(e)}"

        current_results[key] = value
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(current_results, f, ensure_ascii=False, indent=2)


def process_text_only_full():
    # 第一阶段：处理所有场景的前 200 条
    print("\n[Phase 1] 优先处理所有场景的前 200 条快速查看效果...")
    for scene in SCENES:
        input_file = os.path.join(INPUT_DIR, f"{scene}.json")
        if not os.path.exists(input_file): continue

        with open(input_file, "r", encoding="utf-8") as f:
            full_keys = list(json.load(f).keys())

        run_processing(scene, full_keys[:200], "P1-Top200")

    # 第二阶段：处理剩余的所有条目
    print("\n[Phase 2] 开始处理剩余的后续数据...")
    for scene in SCENES:
        input_file = os.path.join(INPUT_DIR, f"{scene}.json")
        if not os.path.exists(input_file): continue

        with open(input_file, "r", encoding="utf-8") as f:
            full_keys = list(json.load(f).keys())

        # 截取从 200 往后的所有 key
        run_processing(scene, full_keys[200:], "P2-Rest")

    print(f"\n✨ 完整对比实验全部完成！结果存放在: {OUTPUT_DIR}")


if __name__ == "__main__":
    process_text_only_full()