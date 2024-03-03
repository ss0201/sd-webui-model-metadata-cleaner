import os
from pathlib import Path

from modules import paths, shared


def model_exists_for_base_name(base_path: Path, model_extensions: list) -> bool:
    for ext in model_extensions:
        if base_path.with_suffix(ext).exists():
            return True
    return False


def remove_unmatched_files(directory: Path, model_extensions: list) -> None:
    if not directory.exists():
        return

    for path in directory.rglob("*"):
        if path.is_file() and path.suffix not in model_extensions:
            parts = path.name.split(".")
            for i in range(1, len(parts) + 1):
                base_name = ".".join(parts[:i])
                base_path = path.parent / base_name

                if model_exists_for_base_name(base_path, model_extensions):
                    break
            else:
                path.unlink()
                print(f"Model Metadata Cleaner: Removed {path}")


def main():
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
        remove_unmatched_files(Path(directory), model_extensions)


main()
