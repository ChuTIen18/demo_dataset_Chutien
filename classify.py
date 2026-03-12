import os
import random
import shutil
import csv
import json

# thư mục dataset gốc
base_dir = "C:/TASK_123/MENTOR_TASK/PYTHON_COURSE/DEmo/demo_dataset_Chutien"

# thư mục chứa ảnh ban đầu
source_dir = os.path.join(base_dir, "dataset/input_images")

# thư mục output sau khi split
train_dir = os.path.join(base_dir, "dataset/images/train")
val_dir = os.path.join(base_dir, "dataset/images/val")
test_dir = os.path.join(base_dir, "dataset/images/test")

split_ratio = (0.7, 0.15, 0.15)

metadata = []

for class_name in os.listdir(source_dir):

    class_path = os.path.join(source_dir, class_name)

    if not os.path.isdir(class_path):
        continue

    images = [f for f in os.listdir(class_path)
              if f.lower().endswith((".jpg",".jpeg",".png"))]

    random.shuffle(images)

    total = len(images)

    train_end = int(split_ratio[0] * total)
    val_end = train_end + int(split_ratio[1] * total)

    train_images = images[:train_end]
    val_images = images[train_end:val_end]
    test_images = images[val_end:]

    os.makedirs(os.path.join(train_dir, class_name), exist_ok=True)
    os.makedirs(os.path.join(val_dir, class_name), exist_ok=True)
    os.makedirs(os.path.join(test_dir, class_name), exist_ok=True)

    # TRAIN
    for img in train_images:
        src = os.path.join(class_path, img)
        dst = os.path.join(train_dir, class_name, img)
        shutil.copy(src, dst)

        metadata.append({
            "filename": img,
            "label": class_name,
            "split": "train",
            "path": dst
        })

    # VAL
    for img in val_images:
        src = os.path.join(class_path, img)
        dst = os.path.join(val_dir, class_name, img)
        shutil.copy(src, dst)

        metadata.append({
            "filename": img,
            "label": class_name,
            "split": "val",
            "path": dst
        })

    # TEST
    for img in test_images:
        src = os.path.join(class_path, img)
        dst = os.path.join(test_dir, class_name, img)
        shutil.copy(src, dst)

        metadata.append({
            "filename": img,
            "label": class_name,
            "split": "test",
            "path": dst
        })

# export CSV
csv_path = os.path.join(base_dir, "metadata.csv")

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["filename","label","split","path"])
    for item in metadata:
        writer.writerow([item["filename"], item["label"], item["split"], item["path"]])

# export JSON
json_path = os.path.join(base_dir, "metadata.json")

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=4)

print("Dataset split completed")
print("CSV:", csv_path)
print("JSON:", json_path)