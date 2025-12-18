import os
import shutil

src = r"C:\Users\SUDESHNA\.gemini\antigravity\brain\7d75b47f-04a2-4e51-a3fe-8fb64385b853\landing_hero_calendar_only_1766037482551.png"
dst_dir = r"c:\Users\SUDESHNA\Desktop\aerele\event_scheduler\static\images"
dst = os.path.join(dst_dir, "landing-hero-3d.png")

print(f"Deploying {src} to {dst}")

try:
    os.makedirs(dst_dir, exist_ok=True)
    if os.path.exists(dst):
        os.remove(dst) # Remove existing to ensure overwrite
    shutil.copy2(src, dst)
    print(f"SUCCESS: Deployed new clean image to {dst}")
except Exception as e:
    print(f"ERROR: {e}")
