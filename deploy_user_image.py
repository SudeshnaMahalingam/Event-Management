import os
import shutil

src = r"C:\Users\SUDESHNA\.gemini\antigravity\brain\7d75b47f-04a2-4e51-a3fe-8fb64385b853\uploaded_image_1766037605994.png"
dst_dir = r"c:\Users\SUDESHNA\Desktop\aerele\event_scheduler\static\images"
dst = os.path.join(dst_dir, "hero-image.png")

print(f"Deploying user image {src} to {dst}")

try:
    os.makedirs(dst_dir, exist_ok=True)
    if os.path.exists(dst):
        os.remove(dst)
    shutil.copy2(src, dst)
    print(f"SUCCESS: Copied to {dst}")
except Exception as e:
    print(f"ERROR: {e}")
