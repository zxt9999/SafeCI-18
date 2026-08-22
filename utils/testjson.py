import json

# ====================== 改成你的 JSON 文件路径 ======================
JSON_FILE = r"E:\data\output_json\05-Agricultural_Production.json"
# ==================================================================

# 读取 JSON
with open(JSON_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 提取所有数字键
existing_numbers = []
for key in data.keys():
    try:
        existing_numbers.append(int(key))
    except:
        pass

if not existing_numbers:
    print("未找到数字编号！")
    exit()

# 范围
min_num = min(existing_numbers)
max_num = max(existing_numbers)
total = len(existing_numbers)

# 找出缺失的编号
missing = []
for num in range(min_num, max_num + 1):
    if num not in existing_numbers:
        missing.append(num)

# 输出结果
print("=" * 70)
print(f"📊 JSON 编号统计结果")
print("=" * 70)
print(f"✅ 总数据条数：{total} 条")
print(f"🔢 最小编号：{min_num}")
print(f"🔢 最大编号：{max_num}")
print(f"❌ 缺失编号数量：{len(missing)} 个")
print("=" * 70)

if missing:
    print(f"📝 缺失的编号列表：")
    print(missing)
else:
    print("✅ 没有缺失任何编号！")
print("=" * 70)