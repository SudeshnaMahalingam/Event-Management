import base64

src = r"C:\Users\SUDESHNA\.gemini\antigravity\brain\7d75b47f-04a2-4e51-a3fe-8fb64385b853\uploaded_image_1766037605994.png"
out = "image_b64.txt"

try:
    with open(src, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
    with open(out, "w") as f:
        f.write(encoded_string)
        
    print("SUCCESS: Encoded to image_b64.txt")
except Exception as e:
    print(f"ERROR: {e}")
