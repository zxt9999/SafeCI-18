import json
import os

# --- 配置路径 ---
# 1. 原始包含 .jpg 的 JSON 文件路径
INPUT_JSON = r"E:\data\output_json\09-Government_Affairs.json"
# 2. 修改后保存的路径
OUTPUT_JSON = r"E:\data\output_json\09-Government_Affairs_fixed.json"

def batch_rename_suffix_in_json():
    # 读取原始数据
    if not os.path.exists(INPUT_JSON):
        print(f"❌ 找不到文件: {INPUT_JSON}")
        return

    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("❌ JSON 格式错误，请检查文件内容。")
            return

    count = 0
    # 遍历每个序号
    for key in data:
        item = data[key]
        if "image_filename" in item:
            old_name = item["image_filename"]
            # 检查是否以 .jpg 结尾（不区分大小写）
            if old_name.lower().endswith(".jpg"):
                # 获取文件名部分，然后强制拼接为 .png
                file_base = os.path.splitext(old_name)[0]
                item["image_filename"] = f"{file_base}.png"
                count += 1

    # 将修改后的数据写入新文件
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 处理完成！")
    print(f"📊 共修改了 {count} 个后缀。")
    print(f"💾 新文件保存至: {OUTPUT_JSON}")

if __name__ == "__main__":
    batch_rename_suffix_in_json()