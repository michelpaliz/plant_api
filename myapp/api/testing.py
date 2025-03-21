# In Colab (where the checkpoint loads successfully)
import torch

# Load your model checkpoint as you do in Colab
checkpoint_path = "/home/michael/myproject/myapp/model/mobilenet_v3_large_weights_best_acc.tar"
checkpoint = torch.load(
    checkpoint_path, map_location=torch.device("cpu"), weights_only=True
)

# Save only the state dictionary
torch.save({"model": checkpoint["model"]}, "/home/michael/myproject/myapp/model/new_checkpoint.tar")
print("New checkpoint saved.")
