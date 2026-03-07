import os
import shutil
import random
import json
import pandas as pd
from PIL import Image
from pathlib import Path

# ===== CONFIG =====

INPUT_DIR = "input_images"
OUTPUT_DIR = "dataset"

TRAIN_RATIO = 0.7
VAL_RATIO = 0.2
TEST_RATIO = 0.1

random.seed(42)

# ===== CREATE STRUCTURE =====

splits = ["train", "val", "test"]

for split in splits:
    Path(f"{OUTPUT_DIR}/images/{split}").mkdir(parents=True, exist_ok=True)

Path(f"{OUTPUT_DIR}/metadata").mkdir(parents=True, exist_ok=True)

# ===== READ LABEL FOLDERS =====

labels = os.listdir(INPUT_DIR)

dataset_rows = []
metadata_list = []

image_counter = 0

for label in labels:

    label_path = os.path.join(INPUT_DIR, label)
    if not os.path.isdir(label_path):
        continue

    IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".tiff")
    images = [
    f for f in os.listdir(label_path)
    if f.lower().endswith(IMAGE_EXTS)
]
    random.shuffle(images)

    n = len(images)

    train_end = int(n * TRAIN_RATIO)
    val_end = train_end + int(n * VAL_RATIO)

    splits_map = {
        "train": images[:train_end],
        "val": images[train_end:val_end],
        "test": images[val_end:]
    }

    for split, files in splits_map.items():

        for img_file in files:

            src = os.path.join(label_path, img_file)

            dst_dir = f"{OUTPUT_DIR}/images/{split}/{label}"
            Path(dst_dir).mkdir(parents=True, exist_ok=True)

            dst = os.path.join(dst_dir, img_file)

            shutil.copy2(src, dst)

            # read image size
            img = Image.open(dst)
            width, height = img.size

            image_id = f"img_{image_counter:06d}"

            dataset_rows.append({
                "image_id": image_id,
                "file_path": dst,
                "label": label,
                "width": width,
                "height": height,
                "split": split
            })

            metadata_list.append({
                "image_id": image_id,
                "file_name": img_file,
                "label": label,
                "width": width,
                "height": height,
                "split": split,
                "path": dst
            })

            image_counter += 1

# ===== SAVE CSV =====

df = pd.DataFrame(dataset_rows)
df.to_csv(f"{OUTPUT_DIR}/dataset_index.csv", index=False)

# ===== SAVE IMAGE METADATA =====

with open(f"{OUTPUT_DIR}/metadata/images_metadata.json", "w") as f:
    json.dump(metadata_list, f, indent=2)

# ===== DATASET METADATA =====

dataset_metadata = {
    "dataset_name": "image_dataset_v1",
    "total_images": len(dataset_rows),
    "labels": labels,
    "splits": {
        "train": TRAIN_RATIO,
        "val": VAL_RATIO,
        "test": TEST_RATIO
    }
}

with open(f"{OUTPUT_DIR}/metadata/dataset_metadata.json", "w") as f:
    json.dump(dataset_metadata, f, indent=2)

print("Dataset integration completed!")
print("Total images:", len(dataset_rows))