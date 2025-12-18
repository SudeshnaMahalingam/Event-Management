import os
import shutil

src = r"C:\Users\SUDESHNA\.gemini\antigravity\brain\7d75b47f-04a2-4e51-a3fe-8fb64385b853\uploaded_image_1766037605994.png"
intermediate = r"C:\Users\SUDESHNA\Desktop\temp_hero.png"
dst_dir = r"c:\Users\SUDESHNA\Desktop\aerele\event_scheduler\static\images"
dst = os.path.join(dst_dir, "hero-image.png")

print("Starting 2-step copy...")

try:
    # Step 1
    shutil.copy2(src, intermediate)
    print(f"Step 1: Copied to {intermediate}")
    
    # Step 2
    os.makedirs(dst_dir, exist_ok=True)
    shutil.move(intermediate, dst)
    print(f"Step 2: Moved to {dst}")
    
    if os.path.exists(dst):
        print("Final verification: File exists.")
        print(f"Size: {os.path.getsize(dst)}")
    else:
        print("Final verification FAILED.")

except Exception as e:
    print(f"ERROR: {e}")
