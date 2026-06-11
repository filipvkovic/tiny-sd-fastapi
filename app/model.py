from diffusers import StableDiffusionPipeline
import torch

MODEL_NAME = "segmind/tiny-sd"

pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_NAME,
    cache_dir="./models",
    # local_files_only=True,
    torch_dtype=torch.float32,
    safety_checker=None,
)

pipe.enable_attention_slicing()

pipe.to("cpu")


@torch.inference_mode()
def generate_image(prompt):

    image = pipe(prompt, height=512, width=512, num_inference_steps=10).images[0]

    return image
