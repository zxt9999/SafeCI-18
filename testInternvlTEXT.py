import json
import os
from openai import OpenAI
from tqdm import tqdm

# --- 路径配置 ---
BASE_DIR = r"E:\MM-SafetyBench-main\data"

# 定义所有场景
SCENES = [
    "06-Education_Teaching",
    "07-Railway_Transportation", "08-Electricity_Supply", "09-Government_Affairs",
    "10-Iron_Smelting", "11-Railway_Maintenance", "12-Health_Consultation",
    "13-Circuit_Maintenance", "14-Financial_Fraud", "15-Public_Opinion_Forgery",
    "16-Cyber_Attack", "17-Legal_Opinion", "18-Traffic_Violation"
]

INPUT_DIR = os.path.join(BASE_DIR, "input_json")
# 修改输出文件夹，明确标注为 internvl 的纯文本结果
OUTPUT_DIR = os.path.join(BASE_DIR, "output_json_internvl14_text_only")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- 客户端初始化 ---
# 确保 LM Studio 中已经加载了 InternVL 模型，并开启了本地服务器
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


def process_internvl_text_only():
    for scene in SCENES:
        print(f"\n" + "=" * 40)
        print(f"📝 InternVL (纯文本模式) 正在处理场景: {scene}")

        input_file = os.path.join(INPUT_DIR, f"{scene}.json")
        output_file = os.path.join(OUTPUT_DIR, f"{scene}.json")

        if not os.path.exists(input_file):
            print(f"⚠️ 跳过：找不到输入文件 {input_file}")
            continue

        # 1. 读取原始 JSON 数据
        with open(input_file, "r", encoding="utf-8") as f:
            full_data = json.load(f)

        all_keys = list(full_data.keys())
        # 全量测试所有条目
        keys_to_process = all_keys[:]

        # 2. 加载已有进度（断点续传）
        if os.path.exists(output_file):
            with open(output_file, "r", encoding="utf-8") as f:
                current_results = json.load(f)
        else:
            current_results = {}

        # 3. 循环处理每一个问题
        for key in tqdm(keys_to_process, desc=f"InternVL-Text [{scene}]"):
            # 检查新的字段名是否存在且有效
            if key in current_results and "internvl_text_only_response" in current_results[key]:
                if "Error" not in current_results[key]["internvl_text_only_response"]:
                    continue

            value = full_data[key]
            question = value.get("generated_question")

            try:
                # --- 核心改动：只发送文本消息给 InternVL ---
                response = client.chat.completions.create(
                    model="internvl",  # 确保此 ID 与 LM Studio 中显示的匹配
                    messages=[
                        {
                            "role": "user",
                            "content": question
                        }
                    ],
                    max_tokens=500,
                )

                # 使用专属字段名保存结果
                answer = response.choices[0].message.content
                value["internvl_text_only_response"] = answer

            except Exception as e:
                value["internvl_text_only_response"] = f"API Error: {str(e)}"

            # 4. 实时更新结果并保存
            current_results[key] = value
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(current_results, f, ensure_ascii=False, indent=2)

    print(f"\n✨ InternVL 纯文本批量测试完成！")
    print(f"📂 结果路径: {OUTPUT_DIR}")


if __name__ == "__main__":
    process_internvl_text_only()