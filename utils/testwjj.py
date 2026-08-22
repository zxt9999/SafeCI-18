import os
from PIL import Image

# ====================== 【只改这里】 ======================
# 改成你的图片文件夹路径
FOLDER_PATH = r"E:\data\testimgs\04-Physical_Harm"
# ==========================================================

# 自动创建输出文件夹
OUT_FOLDER = os.path.join(FOLDER_PATH, "已转PNG_原图不动")
os.makedirs(OUT_FOLDER, exist_ok=True)

# 遍历所有文件
for filename in os.listdir(FOLDER_PATH):
    # 只处理 .jpg / .jpeg
    if filename.lower().endswith((".jpg", ".jpeg")):
        old_path = os.path.join(FOLDER_PATH, filename)

        # 新文件名：把后缀改成 .png
        new_name = os.path.splitext(filename)[0] + ".png"
        new_path = os.path.join(OUT_FOLDER, new_name)

        # 转换并保存
        with Image.open(old_path) as img:
            img.save(new_path, "PNG")

        print(f"✅ 已转换：{filename} → {new_name}")

print("\n🎉 全部转换完成！")
print(f"📂 新文件在：{OUT_FOLDER}")
print(f"✅ 你的所有原图 100% 没动、没删、没覆盖！")