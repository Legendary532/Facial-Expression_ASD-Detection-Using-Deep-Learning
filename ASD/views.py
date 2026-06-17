import os
import uuid
import hashlib
import logging

from django.shortcuts import render
from django.conf import settings

from .models import Prediction
from .model_loader import load_resnet50, load_resnet34, load_vgg19
from .utils import predict_image
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_protect

logger = logging.getLogger(__name__)

# =========================
# LOAD MODELS
# =========================
resnet50_model, resnet50_checkpoint = load_resnet50()
resnet34_model, resnet34_checkpoint = load_resnet34()
vgg19_model, vgg19_checkpoint = load_vgg19()

# =========================
# HASH FUNCTION
# =========================
def get_image_hash(file):
    file.seek(0)
    img_hash = hashlib.md5(file.read()).hexdigest()
    file.seek(0)
    return img_hash

# =========================
# SUGGESTION LOGIC
# =========================
def get_suggestion(result):
    if result == "ASD":
        return "Ensemble AI (3 models) predicts ASD patterns. Must consult pediatrician for final diagnosis."
    elif result == "Non ASD":
        return "AI confirms typical development. No further screening needed."
    else:
        return "Invalid or unclear face input. This system analyzes ONLY ASD vs Non-ASD from frontal face images."
# =========================
# BASIC PAGES
# =========================
def index(request):
    return render(request, "index.html")

def main_view(request):
    return render(request, "main.html")

# =========================
# HISTORY
# =========================
@login_required
@user_passes_test(lambda u: u.is_superuser)
def history_view(request):
    records = Prediction.objects.all().order_by("-created_at")
    return render(request, "history.html", {"records": records})

# =========================
# ENSEMBLE LOGIC
# =========================
def ensemble_decision(preds):

    score = {"ASD": 0.0, "Non ASD": 0.0}
    labels = []
    confidences = []

    for label, conf in preds:
        labels.append(label)
        conf = float(conf)
        confidences.append(conf)

        conf = max(0.55, min(conf, 0.90))
        score[label] += conf

    asd_count = labels.count("ASD")
    non_count = labels.count("Non ASD")

    avg_conf = sum(confidences) / len(confidences)
    diff = abs(score["ASD"] - score["Non ASD"])

    if avg_conf < 0.75:
        return "Uncertain"

    if asd_count != 3 and non_count != 3:
        return "Uncertain"

    if diff < 0.35:
        return "Uncertain"

    if max(confidences) < 0.80:
        return "Uncertain"

    return "ASD" if score["ASD"] > score["Non ASD"] else "Non ASD"

# =========================
# PREDICTION VIEW
# =========================
@csrf_protect
@csrf_protect
def predict(request):

    if request.method != "POST":
        return render(request, "main.html")

    image_file = request.FILES.get("image")

    if not image_file:
        return render(request, "main.html", {
            "error": "Upload image required"
        })

    # -------------------------
    # FILE SIZE CHECK (before writing)
    # -------------------------
    if image_file.size > 5 * 1024 * 1024:
        return render(request, "main.html", {"error": "Max 5MB allowed"})

    # -------------------------
    # COMPUTE HASH (from in-memory file)
    # -------------------------
    image_hash = get_image_hash(image_file)

    # -------------------------
    # CHECK FOR EXISTING RECORD
    # -------------------------
    existing = Prediction.objects.filter(image_hash=image_hash).first()

    # If duplicate exists and its result is "Uncertain"
    if existing and existing.final_result == "Uncertain":
        # Show input screen with uncertain message (no duplicate popup)
        return render(request, "main.html", {
            "uncertain": True,
            "suggestion": get_suggestion("Uncertain")
        })

    # If duplicate exists and result is NOT Uncertain (ASD / Non ASD)
    if existing:
        # We must still delete any temp file if it was already created?
        # In this flow we haven't written temp file yet (we moved hash check earlier),
        # so no cleanup needed. Just show duplicate screen.
        return render(request, "main.html", {
            "duplicate": True,
            "result": existing.final_result,
            "is_uncertain": False,
            "model_results": {
                "resnet50": existing.resnet50_result,
                "resnet34": existing.resnet34_result,
                "vgg19": existing.vgg19_result
            },
            "suggestion": get_suggestion(existing.final_result)
        })

    # -------------------------
    # SAVE TEMP IMAGE (only if new image)
    # -------------------------
    temp_path = os.path.join(
        settings.MEDIA_ROOT,
        f"{uuid.uuid4().hex}.jpg"
    )
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

    with open(temp_path, "wb+") as f:
        for chunk in image_file.chunks():
            f.write(chunk)

    # -------------------------
    # MODEL PREDICTION
    # -------------------------
    try:
        result50 = predict_image(temp_path, resnet50_model, resnet50_checkpoint)
        result34 = predict_image(temp_path, resnet34_model, resnet34_checkpoint)
        resultvgg = predict_image(temp_path, vgg19_model, vgg19_checkpoint)

        label50, conf50 = result50["label"], result50["confidence"]
        label34, conf34 = result34["label"], result34["confidence"]
        labelvgg, confvgg = resultvgg["label"], resultvgg["confidence"]

        final_result = ensemble_decision([
            (label50, conf50),
            (label34, conf34),
            (labelvgg, confvgg)
        ])

        avg_conf = (conf50 + conf34 + confvgg) / 3
        if avg_conf < 0.70:
            final_result = "Uncertain"

    except Exception as e:
        logger.error(e)
        final_result = "Uncertain"
        label50 = label34 = labelvgg = "Error"

    # -------------------------
    # CLEAN TEMP FILE
    # -------------------------
    if os.path.exists(temp_path):
        os.remove(temp_path)

    # -------------------------
    # SAVE TO DATABASE
    # -------------------------
    Prediction.objects.create(
        image=image_file,
        image_hash=image_hash,
        resnet50_result=label50,
        resnet34_result=label34,
        vgg19_result=labelvgg,
        final_result=final_result
    )

    # -------------------------
    # RESPONSE
    # -------------------------
    if final_result == "Uncertain":
        return render(request, "main.html", {
            "uncertain": True,
            "suggestion": get_suggestion(final_result)
        })

    return render(request, "main.html", {
        "result": final_result,
        "show_models": True,
        "model_results": {
            "resnet50": label50,
            "resnet34": label34,
            "vgg19": labelvgg
        },
        "suggestion": get_suggestion(final_result)
    })
