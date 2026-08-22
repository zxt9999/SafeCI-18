import os
import hashlib
import shutil
from collections import defaultdict

# 删除重复图片
# ====================== 改成你的文件夹路径 ======================
FOLDER = r"C:\Users\Administrator\Desktop\03-Industrial_production"
# =================================================================

# 重复文件会移动到这里
DUPLICATE_FOLDER = os.path.join(FOLDER, "重复图片_已隔离")
os.makedirs(DUPLICATE_FOLDER, exist_ok=True)

def get_file_md5(filepath):
    hash_obj = hashlib.md5()
    with open(filepath, "rb") as f:
        while chunk := f.read(1024 * 1024):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

# 按MD5分组
hash_groups = defaultdict(list)
exts = (".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG")

for name in os.listdir(FOLDER):
    path = os.path.join(FOLDER, name)
    if os.path.isfile(path) and name.lower().endswith(exts):
        f_hash = get_file_md5(path)
        hash_groups[f_hash].append(path)

# 找出重复并移动
moved = []
for h, paths in hash_groups.items():
    if len(paths) > 1:
        # 保留第一个，其余移走
        keep = paths[0]
        for dup_path in paths[1:]:
            fname = os.path.basename(dup_path)
            target = os.path.join(DUPLICATE_FOLDER, fname)

            # 重名处理
            counter = 1
            while os.path.exists(target):
                base, ext = os.path.splitext(fname)
                target = os.path.join(DUPLICATE_FOLDER, f"{base}_{counter}{ext}")
                counter += 1

            shutil.move(dup_path, target)
            moved.append((dup_path, target))
            print(f"已隔离重复：{fname}")

print("\n=== 完成 ===")
print(f"共隔离重复图片：{len(moved)} 张")
print(f"全部在文件夹：{DUPLICATE_FOLDER}")
print("确认没问题后，你可以直接删除这个文件夹。")