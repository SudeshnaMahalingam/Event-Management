import os
import shutil

src = r"C:\Users\SUDESHNA\.gemini\antigravity\brain\7d75b47f-04a2-4e51-a3fe-8fb64385b853\landing_hero_saas_1766036881126.png"
dst_dir = r"c:\Users\SUDESHNA\Desktop\aerele\event_scheduler\static\images"
dst = os.path.join(dst_dir, "landing-hero-3d.png")

try:
    os.makedirs(dst_dir, exist_ok=True)
    shutil.copy2(src, dst)
    print("SUCCESS: File copied to", dst)
except Exception as e:
    print("ERROR:", e)
