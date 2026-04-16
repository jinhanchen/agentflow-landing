"""Crop nano-banana concept image + make cream background transparent."""
from pathlib import Path
from PIL import Image
import numpy as np

SRC = Path(r"C:\Users\jinha\xwechat_files\wxid_co3rxklu708i22_0b74\temp\RWTemp\2026-04\05802a40fd25a7dae3b497ccaa9923c0.png")
DST = Path(r"C:\Users\jinha\OneDrive\桌面\AgentFlow webpage\assets\hero-concept.png")

img = Image.open(SRC).convert("RGBA")
arr = np.array(img).astype(np.int16)
H, W = arr.shape[:2]
print(f"Source: {W}x{H}")

# 1. Sample bg color from 4 corners
corners = [arr[5:25, 5:25], arr[5:25, -25:-5], arr[-25:-5, 5:25], arr[-25:-5, -25:-5]]
bg_samples = np.concatenate([c.reshape(-1, 4) for c in corners], axis=0)
bg_rgb = np.median(bg_samples[:, :3], axis=0)
print(f"Detected bg color: RGB{tuple(bg_rgb.astype(int))}")

# 2. Euclidean distance from bg for each pixel
rgb = arr[:, :, :3]
dist = np.sqrt(np.sum((rgb - bg_rgb) ** 2, axis=-1))

# 3. Alpha map: smooth gradient for anti-aliased edges
T_LOW, T_HIGH = 28, 65
alpha = np.clip((dist - T_LOW) / (T_HIGH - T_LOW), 0, 1) * 255
alpha = alpha.astype(np.uint8)

# 4. Find content bounding box
mask = alpha > 40
ys, xs = np.where(mask)
y0, y1 = ys.min(), ys.max()
x0, x1 = xs.min(), xs.max()
print(f"Content bbox: ({x0},{y0}) - ({x1},{y1})")

# 5. Add padding (12% vertical, 8% horizontal)
h_c, w_c = y1 - y0, x1 - x0
pad_y = int(h_c * 0.12)
pad_x = int(w_c * 0.08)
y0 = max(0, y0 - pad_y)
y1 = min(H, y1 + pad_y)
x0 = max(0, x0 - pad_x)
x1 = min(W, x1 + pad_x)
print(f"Padded bbox: ({x0},{y0}) - ({x1},{y1}), size {x1-x0}x{y1-y0}")

# 6. Apply alpha + crop
rgba = arr.astype(np.uint8).copy()
rgba[:, :, 3] = alpha
cropped = rgba[y0:y1, x0:x1]

# 7. Save
result = Image.fromarray(cropped, mode="RGBA")
DST.parent.mkdir(parents=True, exist_ok=True)
result.save(DST, "PNG", optimize=True)
print(f"[OK] Saved {DST.name} ({result.size[0]}x{result.size[1]})")
