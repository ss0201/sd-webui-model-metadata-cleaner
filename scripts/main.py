import os
from pathlib import Path

from modules import paths, shared

model_path = shared.cmd_opts.ckpt_dir
if model_path is None:
    model_dir = "Stable-diffusion"
    model_path = os.path.abspath(os.path.join(paths.models_path, model_dir))

directories: list[str] = [
    model_path,
    shared.cmd_opts.lora_dir,
    shared.cmd_opts.embeddings_dir,
    shared.cmd_opts.hypernetwork_dir,
]

model_extensions = [".pt", ".ckpt", ".safetensors"]

for directory in directories:
    if directory is None:
        continue

    if not Path(directory).exists():
        continue

    for path in Path(directory).rglob("*"):
        if path.is_file() and path.suffix not in model_extensions:
            base_name = path.name.split(".")[0]
            base_path = path.parent / base_name

            model_exists = False

            for ext in model_extensions:
                if (base_path.with_suffix(ext)).exists():
                    model_exists = True
                    break

            if not model_exists:
                path.unlink()
                print(f"Model Metadata Cleaner: Removed {path}")
