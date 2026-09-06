import os
from app import app

# Output directory create karein
os.makedirs("dist/api", exist_ok=True)

with app.test_client() as client:
    # Get Main HTML
    res_home = client.get('/')
    with open("dist/index.html", "w", encoding="utf-8") as f:
        f.write(res_home.data.decode('utf-8'))

    # Get Backend UI Endpoint Data
    res_ui = client.get('/api/render-ui')
    with open("dist/api/render-ui", "w", encoding="utf-8") as f:
        f.write(res_ui.data.decode('utf-8'))

print("Build successful! Files rendered into 'dist/' folder.")
