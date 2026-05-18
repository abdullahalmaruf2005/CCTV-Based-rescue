"""
Fire & Smoke Detection - YOLOv8 Training Script

This script trains a YOLOv8 model for fire and smoke detection.
Run this on your local PC with a GPU for best performance.

Usage:
    python train_fire_model.py

Or use the YOLOv8 CLI directly:
    yolo detect train data=data.yaml model=yolov8n.pt epochs=50 imgsz=640

Prerequisites:
    pip install ultralytics
"""

import os
import sys


def create_data_yaml(dataset_path: str) -> str:
    """Create the data.yaml configuration file for YOLOv8 training."""
    yaml_content = f"""# Fire & Smoke Detection Dataset Configuration
# Place this file in your dataset root directory

path: {dataset_path}
train: images/train
val: images/val

# Number of classes
nc: 2

# Class names
names:
  0: fire
  1: smoke
"""
    yaml_path = os.path.join(dataset_path, "data.yaml")
    with open(yaml_path, "w") as f:
        f.write(yaml_content)
    print(f"Created data.yaml at: {yaml_path}")
    return yaml_path


def train(
    data_yaml: str = "data.yaml",
    model: str = "yolov8n.pt",
    epochs: int = 50,
    imgsz: int = 640,
    batch: int = 16,
    project: str = "runs/fire_detection",
    name: str = "train",
):
    """
    Train YOLOv8 model for fire/smoke detection.

    Args:
        data_yaml: Path to data.yaml configuration
        model: Base model to fine-tune (yolov8n.pt recommended for speed)
        epochs: Number of training epochs
        imgsz: Image size for training
        batch: Batch size (reduce if GPU runs out of memory)
        project: Output directory for training runs
        name: Name for this training run
    """
    from ultralytics import YOLO

    print("=" * 60)
    print("  FIRE & SMOKE DETECTION - YOLOv8 TRAINING")
    print("=" * 60)
    print(f"  Model:    {model}")
    print(f"  Dataset:  {data_yaml}")
    print(f"  Epochs:   {epochs}")
    print(f"  Img Size: {imgsz}")
    print(f"  Batch:    {batch}")
    print("=" * 60)

    # Load pretrained YOLOv8 model
    yolo_model = YOLO(model)

    # Train the model
    results = yolo_model.train(
        data=data_yaml,
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        project=project,
        name=name,
        patience=10,       # Early stopping patience
        save=True,          # Save checkpoints
        save_period=10,     # Save every 10 epochs
        plots=True,         # Generate training plots
        verbose=True,
    )

    print("\n" + "=" * 60)
    print("  TRAINING COMPLETE!")
    print("=" * 60)
    print(f"  Best model saved to: {project}/{name}/weights/best.pt")
    print(f"  Last model saved to: {project}/{name}/weights/last.pt")
    print("\n  To use this model in the surveillance system:")
    print(f"  1. Copy best.pt to backend/models/fire_best.pt")
    print(f"  2. Or set FIRE_MODEL_PATH environment variable")
    print("=" * 60)

    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Train YOLOv8 Fire Detection Model")
    parser.add_argument("--data", default="data.yaml", help="Path to data.yaml")
    parser.add_argument("--model", default="yolov8n.pt", help="Base model")
    parser.add_argument("--epochs", type=int, default=50, help="Training epochs")
    parser.add_argument("--imgsz", type=int, default=640, help="Image size")
    parser.add_argument("--batch", type=int, default=16, help="Batch size")
    parser.add_argument("--create-yaml", type=str, help="Create data.yaml for given dataset path")

    args = parser.parse_args()

    if args.create_yaml:
        create_data_yaml(args.create_yaml)
        sys.exit(0)

    train(
        data_yaml=args.data,
        model=args.model,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
    )
