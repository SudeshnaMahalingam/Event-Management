import os
import shutil
import time

src = r"C:\Users\SUDESHNA\.gemini\antigravity\brain\7d75b47f-04a2-4e51-a3fe-8fb64385b853\uploaded_image_1766037605994.png"
dst_dir = r"c:\Users\SUDESHNA\Desktop\aerele\event_scheduler\static\images"
dst = os.path.join(dst_dir, "hero-image.png")
temp_local = "temp_hero.png"

with open("copy_log.txt", "w") as log:
    def log_print(msg):
        print(msg)
        log.write(msg + "\n")
        log.flush()

    log_print(f"Starting copy process...")
    log_print(f"Source: {src}")
    
    if not os.path.exists(src):
        log_print("CRITICAL ERROR: Source file does not exist!")
        exit(1)
        
    log_print(f"Source size: {os.path.getsize(src)}")

    try:
        # Step 1: Local copy
        log_print(f"Copying to local temp: {temp_local}")
        shutil.copy2(src, temp_local)
        log_print("Local copy successful.")
        
        # Step 2: Ensure dir
        os.makedirs(dst_dir, exist_ok=True)
        log_print(f"Destination dir secured: {dst_dir}")

        # Step 3: Move to dest
        if os.path.exists(dst):
            os.remove(dst)
            log_print("Removed existing destination file.")
            
        shutil.move(temp_local, dst)
        log_print(f"SUCCESS: Moved to {dst}")
        log_print(f"Final file size: {os.path.getsize(dst)}")
        
    except Exception as e:
        log_print(f"EXCEPTION: {e}")
