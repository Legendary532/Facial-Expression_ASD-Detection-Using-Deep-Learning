import torch
import torch.nn as nn
from torchvision import models
from django.conf import settings
import os

DEVICE = torch.device("cpu")   # Django me CPU safe hota hai

# =========================
# RESNET50
# =========================
def load_resnet50():
    model_path = os.path.join(settings.ML_MODELS_DIR, "resnet50_asd_final.pth")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"ResNet50 model not found: {model_path}")

    checkpoint = torch.load(model_path, map_location=DEVICE)

    model = models.resnet50(weights=None)

    in_features = model.fc.in_features

    model.fc = nn.Sequential(
        nn.Linear(in_features, 512),
        nn.BatchNorm1d(512),
        nn.ReLU(inplace=True),
        nn.Dropout(0.7),

        nn.Linear(512, 256),
        nn.BatchNorm1d(256),
        nn.ReLU(inplace=True),
        nn.Dropout(0.65),

        nn.Linear(256, 128),
        nn.BatchNorm1d(128),
        nn.ReLU(inplace=True),
        nn.Dropout(0.6),

        nn.Linear(128, 64),
        nn.BatchNorm1d(64),
        nn.ReLU(inplace=True),
        nn.Dropout(0.5),

        nn.Linear(64, 2)
    )

    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(DEVICE)
    model.eval()

    return model, checkpoint


# =========================
# RESNET34
# =========================
def load_resnet34():
    model_path = os.path.join(settings.ML_MODELS_DIR, "resnet34_asd_final.pth")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"ResNet34 model not found: {model_path}")

    checkpoint = torch.load(model_path, map_location=DEVICE)

    model = models.resnet34(weights=None)

    in_features = model.fc.in_features

    model.fc = nn.Sequential(
        nn.Linear(in_features, 256),
        nn.BatchNorm1d(256),
        nn.ReLU(inplace=True),
        nn.Dropout(0.7),

        nn.Linear(256, 128),
        nn.BatchNorm1d(128),
        nn.ReLU(inplace=True),
        nn.Dropout(0.6),

        nn.Linear(128, 64),
        nn.BatchNorm1d(64),
        nn.ReLU(inplace=True),
        nn.Dropout(0.5),

        nn.Linear(64, 2)
    )

    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(DEVICE)
    model.eval()

    return model, checkpoint


# =========================
# VGG19
# =========================
def load_vgg19():
    model_path = os.path.join(settings.ML_MODELS_DIR, "vgg19_final.pth")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"VGG19 model not found: {model_path}")

    checkpoint = torch.load(model_path, map_location=DEVICE)

    model = models.vgg19(weights=None)

    # SAME AS TRAINING
    model.classifier = nn.Sequential(
        nn.Linear(25088, 1024),
        nn.ReLU(),
        nn.Dropout(0.5),

        nn.Linear(1024, 512),
        nn.ReLU(),
        nn.Dropout(0.5),

        nn.Linear(512, 2)
    )

    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(DEVICE)
    model.eval()

    return model, checkpoint