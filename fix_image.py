import os
import shutil

# Correct paths based on previous list_dir findings
src = r"C:\Users\SUDESHNA\.gemini\antigravity\brain\7d75b47f-04a2-4e51-a3fe-8fb64385b853\landing_hero_saas_1766036881126.png"
dst_dir = r"c:\Users\SUDESHNA\Desktop\aerele\event_scheduler\static\images"
dst = os.path.join(dst_dir, "landing-hero-3d.png")

print(f"Source exists: {os.path.exists(src)}")
print(f"Dest dir exists: {os.path.exists(dst_dir)}")

try:
    os.makedirs(dst_dir, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"SUCCESS: Copied to {dst}")
    print(f"File size: {os.path.getsize(dst)} bytes")
except Exception as e:
    print(f"ERROR: {e}")
