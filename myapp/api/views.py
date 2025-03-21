import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import json
import os
from datetime import datetime
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
import dill  # Use dill for improved pickle handling

# ✅ Define BASE_DIR Correctly
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ✅ Use Correct Relative Paths
MODEL_PATH = os.path.join(BASE_DIR, "myapp/model/new_checkpoint.tar")

SPECIES_MAPPING_PATH = os.path.join(
    BASE_DIR, "myapp/metadata/plantnet300K_species_id_2_name.json"
)
CLASS_IDX_MAPPING_PATH = os.path.join(
    BASE_DIR, "myapp/metadata/class_idx_to_species_id.json"
)
FAMILY_MAPPING_PATH = os.path.join(BASE_DIR, "myapp/mapping/plants_family_mapping.json")

# ✅ Load metadata mappings safely
try:
    with open(SPECIES_MAPPING_PATH, "r") as f:
        species_id_to_name = json.load(f)
    with open(CLASS_IDX_MAPPING_PATH, "r") as f:
        class_idx_to_species_id = json.load(f)
    with open(FAMILY_MAPPING_PATH, "r") as f:
        family_mapping = json.load(f)
    species_to_family = {
        species: family
        for family, details in family_mapping.items()
        for species in details.get("notable_examples", [])
    }
except FileNotFoundError as e:
    raise FileNotFoundError(f"❌ Missing required file: {str(e)}")


# ✅ Custom function to load checkpoint using dill with an overridden persistent_load
def load_checkpoint_with_dill(path, device):
    with open(path, "rb") as f:
        unpickler = dill.Unpickler(f)
        # Override persistent_load to simply return None for any persistent id.
        unpickler.persistent_load = lambda saved_id: None
        checkpoint = unpickler.load()
    return checkpoint


# ✅ Load the model lazily (without weights_only)
def load_model():
    """Loads the ML model only when needed."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"❌ Model file not found: {MODEL_PATH}")

    model = models.mobilenet_v3_large(pretrained=False)
    num_features = model.classifier[-1].in_features
    model.classifier[-1] = nn.Linear(num_features, 1081)

    # Load trained weights using dill without the conflicting weights_only parameter.
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    checkpoint = torch.load(MODEL_PATH, map_location=device, pickle_module=dill)
    print("Checkpoint keys:", checkpoint.keys())  # Debug output
    if "model" not in checkpoint or checkpoint["model"] is None:
        raise ValueError("❌ Checkpoint does not contain a valid 'model' state dict.")

    model.load_state_dict(checkpoint["model"])
    model.to(device)
    model.eval()
    return model, device


# ✅ Image transformations
transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)


# ✅ API endpoint for image prediction
@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def predict_image(request):
    try:
        print("✅ Request received. Checking for image...")
        print("FILES:", request.FILES)
        print("DATA:", request.data)

        if "image" not in request.FILES:
            return Response({"error": "No image uploaded"}, status=400)

        image_file = request.FILES["image"]
        print(f"✅ Image uploaded: {image_file.name}")

        if not image_file.name.lower().endswith((".png", ".jpg", ".jpeg")):
            return Response(
                {"error": "Invalid image format. Only JPG, JPEG, and PNG are allowed."},
                status=400,
            )

        try:
            image = Image.open(image_file).convert("RGB")
        except Exception as e:
            print("❌ Exception when opening image:", str(e))
            return Response({"error": "Invalid image file"}, status=400)

        image = transform(image).unsqueeze(0)

        model, device = load_model()
        image = image.to(device)

        with torch.no_grad():
            output = model(image)
            predicted_class = torch.argmax(output, dim=1).item()

        species_id = class_idx_to_species_id.get(str(predicted_class), None)
        species_name = (
            species_id_to_name.get(species_id, "Unknown") if species_id else "Unknown"
        )
        plant_family = species_to_family.get(species_name, "Unknown")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print("✅ Inference complete. Returning response...")
        return Response(
            {
                "predicted_species": species_name,
                "family": plant_family,
                "date": timestamp,
            },
            status=200,
        )
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return Response({"error": str(e)}, status=500)


# ✅ Minimal test endpoint for file upload debugging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def test_upload_simple(request):
    return JsonResponse({"FILES": str(request.FILES), "POST": str(request.POST)})
