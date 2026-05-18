# Fire & Smoke Detection - Local Training Guide

Complete step-by-step guide to train your own YOLOv8 fire/smoke detection model locally.

---

## Prerequisites

```bash
# Install Python 3.8+ and pip, then install ultralytics
pip install ultralytics

# Verify GPU is available (optional but recommended)
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
```

---

## Step 1: Dataset Collection

### Option A: Download from Roboflow (Recommended)

1. Go to [Roboflow Universe](https://universe.roboflow.com/)
2. Search for "fire detection" or "fire and smoke"
3. Recommended datasets:
   - [Fire Detection Dataset](https://universe.roboflow.com/search?q=fire+detection)
   - [Fire and Smoke Dataset](https://universe.roboflow.com/search?q=fire+smoke+detection)
4. Click **Download** → Select **YOLOv8** format → Download ZIP
5. Extract to a folder (e.g., `fire_dataset/`)

### Option B: Collect Your Own Images

1. Gather 200-500+ images containing fire and/or smoke
2. Include diverse scenarios:
   - Indoor/outdoor fires
   - Different lighting conditions
   - Various fire sizes (small flames to large fires)
   - Smoke of different densities
3. Also include 100+ negative images (no fire/smoke) to reduce false positives

### Option C: Public Datasets

- [Kaggle Fire Detection](https://www.kaggle.com/datasets/phylake1337/fire-dataset)
- [FIRESENSE Dataset](https://zenodo.org/record/836749)
- [BoWFire Dataset](https://bitbucket.org/gbdi/bowfire-dataset)

---

## Step 2: Image Annotation

### Using Roboflow (Easiest)

1. Create a free account at [roboflow.com](https://roboflow.com)
2. Create a new project → Object Detection
3. Upload your images
4. Draw bounding boxes around fire and smoke
5. Label classes as: `fire`, `smoke`
6. Export in **YOLOv8** format

### Using LabelImg (Free Desktop Tool)

```bash
pip install labelImg
labelImg
```

1. Open your image directory
2. Set save format to **YOLO**
3. Draw bounding boxes around fire and smoke
4. Save annotations (creates .txt files alongside images)

### Annotation Tips

- Draw tight bounding boxes around flames and smoke
- Label even small fires/smoke
- Be consistent with class names
- Annotate at least 200 images for decent results

---

## Step 3: Dataset Structure

Your dataset must follow this structure:

```
fire_dataset/
├── data.yaml
├── images/
│   ├── train/
│   │   ├── img001.jpg
│   │   ├── img002.jpg
│   │   └── ...
│   └── val/
│       ├── img050.jpg
│       ├── img051.jpg
│       └── ...
└── labels/
    ├── train/
    │   ├── img001.txt
    │   ├── img002.txt
    │   └── ...
    └── val/
        ├── img050.txt
        ├── img051.txt
        └── ...
```

**Split ratio:** 80% train, 20% validation

Each `.txt` label file contains one line per object:
```
<class_id> <x_center> <y_center> <width> <height>
```
Where all values are normalized (0-1). Example:
```
0 0.45 0.52 0.30 0.40
1 0.70 0.35 0.25 0.50
```
- `0` = fire
- `1` = smoke

---

## Step 4: data.yaml Configuration

Create `data.yaml` in your dataset root:

```yaml
# Fire & Smoke Detection Dataset Configuration
path: /full/path/to/fire_dataset
train: images/train
val: images/val

# Number of classes
nc: 2

# Class names
names:
  0: fire
  1: smoke
```

Or generate it automatically:
```bash
python train_fire_model.py --create-yaml /path/to/fire_dataset
```

---

## Step 5: Training

### Option A: Using the training script

```bash
cd backend/training
python train_fire_model.py --data /path/to/data.yaml --epochs 50 --batch 16
```

### Option B: Using YOLOv8 CLI directly

```bash
yolo detect train data=/path/to/data.yaml model=yolov8n.pt epochs=50 imgsz=640 batch=16
```

### Option C: Using Python

```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # Load pretrained model
model.train(
    data="/path/to/data.yaml",
    epochs=50,
    imgsz=640,
    batch=16,
    patience=10,
)
```

### Training Parameters Guide

| Parameter | Default | Description |
|-----------|---------|-------------|
| `model`   | yolov8n.pt | Base model (n=nano, s=small, m=medium) |
| `epochs`  | 50      | Training epochs (more = better, but slower) |
| `imgsz`   | 640     | Image size (640 is standard) |
| `batch`   | 16      | Batch size (reduce to 8 or 4 if GPU OOM) |
| `patience`| 10      | Early stopping patience |
| `lr0`     | 0.01    | Initial learning rate |

### GPU vs CPU Training

- **With GPU:** Training takes ~30-60 minutes for 50 epochs
- **Without GPU:** Training takes ~4-8 hours for 50 epochs
- Reduce batch size if you get CUDA out-of-memory errors

---

## Step 6: Connect Model to Surveillance System

After training completes, the best model is saved at:
```
runs/fire_detection/train/weights/best.pt
```

### Method 1: Copy the model file

```bash
cp runs/fire_detection/train/weights/best.pt ../models/fire_best.pt
```

### Method 2: Set environment variable

```bash
export FIRE_MODEL_PATH=/full/path/to/best.pt
```

### Method 3: Update .env file

Add to `backend/.env`:
```
FIRE_MODEL_PATH=/full/path/to/best.pt
```

Then restart the backend server. The fire detection will automatically activate!

---

## Step 7: Validate the Model

```bash
# Run validation
yolo detect val model=runs/fire_detection/train/weights/best.pt data=/path/to/data.yaml

# Test on a single image
yolo detect predict model=runs/fire_detection/train/weights/best.pt source=test_image.jpg

# Test on a video
yolo detect predict model=runs/fire_detection/train/weights/best.pt source=test_video.mp4
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| CUDA out of memory | Reduce `batch` to 8 or 4 |
| Low accuracy | Add more training data, increase epochs |
| Too many false positives | Add more negative (no-fire) images |
| Model not loading | Check file path, ensure .pt file exists |
| Training too slow | Use smaller model (yolov8n.pt), reduce imgsz to 416 |

---

## Model Performance Tips

1. **More data = better results** - Aim for 500+ annotated images
2. **Data augmentation** - YOLOv8 does this automatically
3. **Class balance** - Have roughly equal fire and smoke images
4. **Quality annotations** - Tight, accurate bounding boxes matter
5. **Fine-tune threshold** - Adjust `FIRE_CONFIDENCE_THRESHOLD` in production
