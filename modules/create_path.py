import os

def create_media_path(name: str) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(current_dir, "..", "media", name))