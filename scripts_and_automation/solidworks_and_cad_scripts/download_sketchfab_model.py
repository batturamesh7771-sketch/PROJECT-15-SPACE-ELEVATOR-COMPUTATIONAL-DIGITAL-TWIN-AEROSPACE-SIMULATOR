import os
import sys
import zipfile
import requests

def download_model(api_token, model_id="2c9d195da8094f7d8365a275dcb08c63"):
    out_dir = r"C:\Users\user\Desktop\Space_Elevator_CAD_Phase1\Downloaded_Sketchfab_Models"
    os.makedirs(out_dir, exist_ok=True)
    
    headers = {
        "Authorization": f"Token {api_token.strip()}",
        "User-Agent": "Mozilla/5.0"
    }
    
    download_api_url = f"https://api.sketchfab.com/v3/models/{model_id}/download"
    print(f"[1/4] Querying Sketchfab Download API for model {model_id}...")
    resp = requests.get(download_api_url, headers=headers)
    
    if resp.status_code != 200:
        print(f"ERROR: API returned status {resp.status_code}")
        print("Response:", resp.text)
        return False
        
    data = resp.json()
    print("[2/4] Available download formats:", list(data.keys()))
    
    # Prefer source (original) or gltf
    download_entry = data.get("source") or data.get("gltf")
    if not download_entry:
        print("ERROR: No download URL found in response")
        return False
        
    dl_url = download_entry["url"]
    file_size = download_entry.get("size", 0)
    print(f"[3/4] Downloading archive ({file_size:,} bytes)...")
    
    zip_path = os.path.join(out_dir, f"{model_id}.zip")
    with requests.get(dl_url, stream=True) as r:
        r.raise_for_status()
        with open(zip_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=65536):
                f.write(chunk)
                
    print(f"      Downloaded to: {zip_path}")
    
    print("[4/4] Extracting archive...")
    extract_folder = os.path.join(out_dir, "Space_Elevator_2_Superduck")
    os.makedirs(extract_folder, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)
        
    print(f"\n[SUCCESS] Model extracted to: {extract_folder}")
    for root, dirs, files in os.walk(extract_folder):
        for file in files:
            p = os.path.join(root, file)
            print(f" - {file} ({os.path.getsize(p):,} bytes)")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        token = sys.argv[1]
    else:
        token = os.environ.get("SKETCHFAB_API_TOKEN")
        
    if not token:
        print("Usage: python download_sketchfab_model.py <SKETCHFAB_API_TOKEN>")
        sys.exit(1)
        
    download_model(token)
