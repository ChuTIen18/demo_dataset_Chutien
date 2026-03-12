import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
from pathlib import Path

from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

class FlowerClassifier:
    def __init__(self, n_components=128):
        self.pca = PCA(n_components=n_components, random_state=42)
        self.svm_model = SVC(kernel='rbf', C=1.0, probability=True, random_state=42)
        
        self.target_names = [
            "apricot_blossom", "daisy", "dandelion", "hibiscus", "hydrangea", 
            "orchid", "peach_blossom", "rose", "sunflower", "tulip"
        ]

    def load_feature(self, root_dir):
        dir_path = Path(root_dir)
        print(f"-> Đang tải dữ liệu từ gốc: {dir_path.absolute()}")
        
        try:
            features = np.load(dir_path / "features.npy")
            splits = np.load(dir_path / "splits.npy")
            paths = np.load(dir_path / "image_paths.npy", allow_pickle=True)
        except FileNotFoundError as e:
            print(f"[LỖI CỐT LÕI] Thiếu file dữ liệu: {e}")
            return None

        # TỰ SINH NHÃN TỪ PATH
        labels_list = []
        label_map = {name: idx for idx, name in enumerate(self.target_names)}
        
        for i, img_path in enumerate(paths):
            normalized_path = str(img_path).replace('\\', '/')
            class_name = Path(normalized_path).parent.name 
            label_idx = label_map.get(class_name, -1) 
            labels_list.append(label_idx)
            if i < 3:
                print(f"   * Debug Path {i}: {normalized_path} -> Class trích xuất: '{class_name}' -> Label ID: {label_idx}")
            
        labels = np.array(labels_list)

        valid_mask = (labels != -1)
        features = features[valid_mask]
        splits = splits[valid_mask]
        labels = labels[valid_mask]
        paths = paths[valid_mask]

        train_mask = (splits == "train")
        val_mask = (splits == "val")
        test_mask = (splits == "test")

        data = {
            "train": (features[train_mask], labels[train_mask]),
            "val": (features[val_mask], labels[val_mask]),
            "test": (features[test_mask], labels[test_mask])
        }
        
        print(f"Tập Train: {len(data['train'][0])} mẫu")
        print(f"Tập Validation: {len(data['val'][0])} mẫu")
        print(f"Tập Test: {len(data['test'][0])} mẫu")
        
        return data

    def run_pipeline(self, data_dict, root_dir):
        X_train, y_train = data_dict["train"]
        X_val, y_val = data_dict["val"]
        X_test, y_test = data_dict["test"]

        # ÉP CHIỀU BẰNG PCA
        print("\n-> Đang ép chiều dữ liệu bằng PCA (2048D -> 128D)...")
        X_train_pca = self.pca.fit_transform(X_train)
        X_val_pca = self.pca.transform(X_val)
        X_test_pca = self.pca.transform(X_test)
        
        artifacts_dir = Path(root_dir) / "artifacts"
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.pca, artifacts_dir / "pca_transformer.pkl")

        # HUẤN LUYỆN SVM 
        self.svm_model.fit(X_train_pca, y_train)
        
        val_acc = accuracy_score(y_val, self.svm_model.predict(X_val_pca))
        print(f"-> Validation Accuracy: {val_acc:.4f}")

        y_pred_test = self.svm_model.predict(X_test_pca)
        test_acc = accuracy_score(y_test, y_pred_test)
        print(f"-> Test Accuracy: {test_acc:.4f}")
        
        print("\nBản kiểm điểm trên tập Test:")
        print(classification_report(y_test, y_pred_test, target_names=self.target_names, zero_division=0))

        joblib.dump(self.svm_model, artifacts_dir / "classifier_svm.pkl")

if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    classifier = FlowerClassifier(n_components=128)
    dataset = classifier.load_feature(root_dir=PROJECT_ROOT)
    
    if dataset is not None:
        classifier.run_pipeline(dataset, root_dir=PROJECT_ROOT)