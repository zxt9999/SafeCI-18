import os

# ====================== 【只改这里】 ======================
# 你的【主文件夹】路径（里面包含18个子文件夹）
MAIN_FOLDER = r"E:\SafeCI-18\data\imgs"
# =================================================================

# 支持的图片格式（可自行增删）
IMAGE_FORMATS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp')

# 开始统计
print("=" * 60)
print("📊 子文件夹图片数量统计")
print("=" * 60)

total_images = 0
folder_count = 0

# 遍历主文件夹下所有子文件夹
for item in os.listdir(MAIN_FOLDER):
    sub_folder_path = os.path.join(MAIN_FOLDER, item)

    # 只统计文件夹，跳过文件
    if os.path.isdir(sub_folder_path):
        folder_count += 1
        img_count = 0

        # 统计当前文件夹里的图片数量
        for file in os.listdir(sub_folder_path):
            if file.lower().endswith(IMAGE_FORMATS):
                img_count += 1

        total_images += img_count
        print(f"📁 {item}  ->  图片数量：{img_count} 张")

print("-" * 60)
print(f"✅ 总计：扫描了 {folder_count} 个子文件夹")
print(f"✅ 总图片数量：{total_images} 张")
print("=" * 60)