# index_images.py
import os, hashlib, datetime, csv
from pathlib import Path


def file_hash(source, algo="sha256", chunk_size=8192):
    """Compute hex digest for a path or a file-like object.

    Accepts a path (str / os.PathLike / Path) or a file-like object
    (with a .read() method). When reading a file-like object, the
    current stream position is preserved when possible.
    """
    h = hashlib.new(algo)

    # Path-like input
    if isinstance(source, (str, os.PathLike, Path)):
        with open(str(source), "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                h.update(chunk)
        return h.hexdigest()

    # File-like input (BytesIO, file handle, etc.)
    try:
        read = source.read
    except Exception:
        raise TypeError("source must be a path or file-like object with a .read() method")

    # Try to remember and restore position
    pos = None
    try:
        pos = source.tell()
        source.seek(0)
    except Exception:
        pos = None

    for chunk in iter(lambda: source.read(chunk_size), b""):
        h.update(chunk)

    if pos is not None:
        try:
            source.seek(pos)
        except Exception:
            pass

    return h.hexdigest()

def human_size(num_bytes):
    for unit in ["B","KB","MB","GB","TB"]:
        if num_bytes < 1024.0:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} PB"

def index_images(drives, extensions, output_file="image_index.csv"):
    extensions = [ext.lower() for ext in extensions]
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Filename","Hash","Path","Size","Created","Modified"])
        for drive in drives:
            for root, dirs, files in os.walk(drive):
                for fname in files:
                    if any(fname.lower().endswith(ext) for ext in extensions):
                        full_path = os.path.join(root, fname)
                        try:
                            stat = os.stat(full_path)
                            created = datetime.datetime.fromtimestamp(stat.st_ctime)
                            modified = datetime.datetime.fromtimestamp(stat.st_mtime)
                            size = stat.st_size
                            h = file_hash(full_path)
                            writer.writerow([
                                fname,
                                h,
                                full_path,
                                human_size(size),
                                created.strftime("%Y-%m-%d %H:%M:%S"),
                                modified.strftime("%Y-%m-%d %H:%M:%S")
                            ])
                        except Exception as e:
                            print(f"Error reading {full_path}: {e}")

if __name__ == "__main__":
    drives = ["D:\\", "E:\\"]
    extensions = [".jpg",".jpeg",".png"]
    index_images(drives, extensions, "image_index.csv")