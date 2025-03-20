import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import json
import os
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

# ✅ Define paths to files
MODEL_PATH = "/home/michael/myproject/myapp/model/data.pkl"
SPECIES_MAPPING_PATH = "/home/michael/myproject/myapp/metadata/plantnet300K_species_id_2_name.json"
CLASS_IDX_MAPPING_PATH = "/home/michael/myproject/myapp/metadata/class_idx_to_species_id.json"
FAMILY_MAPPING_PATH = "/home/michael/myproject/myapp/mapping/plants_family_mapping.json"

# ✅ Check if files exist before loading
for path in [MODEL_PATH, SPECIES_MAPPING_PATH, CLASS_IDX_MAPPING_PATH, FAMILY_MAPPING_PATH]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Error: File not found - {path}")

# ✅ Load species ID to name mapping
with open(SPECIES_MAPPING_PATH, 'r') as f:
    species_id_to_name = json.load(f)

# ✅ Load class index to species ID mapping
with open(CLASS_IDX_MAPPING_PATH, 'r') as f:
    class_idx_to_species_id = json.load(f)

# ✅ Load plant family mapping
with open(FAMILY_MAPPING_PATH, 'r') as f:
    family_mapping = json.load(f)

# ✅ Create species-to-family lookup
species_to_family = {species: family for family, details in family_mapping.items() for species in details.get("notable_examples", [])}

# ✅ Load the trained MobileNet v3 model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = models.mobilenet_v3_large(pretrained=False)
num_features = model.classifier[-1].in_features
model.classifier[-1] = nn.Linear(num_features, 1081)  # Ensure correct class count

# ✅ Load the trained model weights
checkpoint = torch.load(MODEL_PATH, map_location=device)
model.load_state_dict(checkpoint['model'])
model.to(device)
model.eval()

print("✅ Model loaded successfully!")

# ✅ Define image transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# ✅ API endpoint to handle image uploads and predictions
@api_view(['POST'])
def predict_image(request):
    try:
        if 'image' not in request.FILES:
            return Response({"error": "No image uploaded"}, status=400)

        image_file = request.FILES['image']
        image = Image.open(image_file).convert("RGB")  # Ensure RGB format
        image = transform(image).unsqueeze(0).to(device)  # Preprocess image

        # 🔹 Run inference
        with torch.no_grad():
            output = model(image)
            predicted_class = torch.argmax(output, dim=1).item()

        # 🔹 Map predicted class index to species ID
        species_id = class_idx_to_species_id.get(str(predicted_class), None)
        species_name = species_id_to_name.get(species_id, "Unknown") if species_id else "Unknown"

        # 🔹 Determine plant family using lookup
        plant_family = species_to_family.get(species_name, "Unknown")

        # 🔹 Generate timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 🔹 Response dictionary
        response_data = {
            "predicted_species": species_name,
            "family": plant_family,
            "date": timestamp
        }

        return Response(response_data, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
