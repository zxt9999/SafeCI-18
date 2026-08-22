import json

# 1. 读取你的 JSON 文件（把文件名改成你自己的）
with open("E:\SafeCI-181\data\\json\\18-Traffic_Violation.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 2. 遍历每一项，删除 ground_truth 字段
for key in data:
    if "standard_safe_response" in data[key]:
        del data[key]["standard_safe_response"]

# 3. 保存到新文件
with open("E:\SafeCI-181\data\\json\\18-Traffic_Violation.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ 已成功删除所有 standard_safe_response 字段！")