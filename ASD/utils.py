import torch
from torchvision import transforms
from PIL import Image

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def predict_image(image_path, model, checkpoint):

    try:

        image = Image.open(image_path).convert("RGB")
        image = transform(image).unsqueeze(0)

        with torch.no_grad():

            outputs = model(image)

            probs = torch.softmax(outputs, dim=1)

            asd_prob = probs[0][0].item()
            td_prob = probs[0][1].item()

            print("Probabilities =", probs.tolist())
            print("ASD Probability =", asd_prob)
            print("TD Probability =", td_prob)

            # ASD sensitivity increase
            if asd_prob >= 0.40:
                return {
                    "label": "ASD",
                    "confidence": round(asd_prob, 2)
                }

            if td_prob >= 0.82:
                return {
                    "label": "Non ASD",
                    "confidence": round(td_prob, 2)
                }

            return {
                "label": "Uncertain",
                "confidence": round(max(asd_prob, td_prob), 2)
            }

    except Exception as e:

        print(f"Prediction Error: {e}")

        return {
            "label": "Uncertain",
            "confidence": 0.0
        }