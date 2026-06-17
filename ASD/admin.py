from django.contrib import admin
from .models import MLModel, Prediction


@admin.register(MLModel)
class MLModelAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "model_type", "is_active", "created_at")

    list_filter = ("model_type", "is_active")

    search_fields = ("name",)


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "final_result",
        "created_at",
    )

    list_filter = (
        "final_result",
    )