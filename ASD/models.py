from django.db import models


# -----------------------------
# ML MODEL TABLE
# -----------------------------
class MLModel(models.Model):

    MODEL_TYPES = [
        ("resnet34", "ResNet34"),
        ("resnet50", "ResNet50"),
        ("vgg19", "VGG19"),
    ]

    name = models.CharField(max_length=100)
    model_type = models.CharField(max_length=20, choices=MODEL_TYPES)
    model_file = models.FileField(upload_to="models/")
    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.model_type})"


# -----------------------------
# PREDICTION TABLE
# -----------------------------
class Prediction(models.Model):

    image = models.ImageField(upload_to="uploads/")
    image_hash = models.CharField(max_length=64, db_index=True)

    resnet34_result = models.CharField(max_length=20)
    resnet50_result = models.CharField(max_length=20)
    vgg19_result = models.CharField(max_length=20)

    final_result = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction - {self.final_result}"