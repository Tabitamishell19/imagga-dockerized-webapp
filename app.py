from flask import Flask, render_template, request
import requests
import base64

app = Flask(__name__)

# Lista de imágenes (puedes cambiar las URLs por las que prefieras)
images = [
    "https://images.unsplash.com/photo-1516117172878-fd2c41f4a759",
    "https://images.unsplash.com/photo-1532009324734-20a7a5813719",
    "https://images.unsplash.com/photo-1524429656589-6633a470097c",
]



@app.route("/")
def index():
    return render_template("index.html", images=images)

@app.route("/analyze", methods=["POST"])
def analyze():
    image_url = request.form["image_url"]
    response = analyze_image(image_url)
    tags = response.get("result", {}).get("tags", [])
    top_tags = sorted(tags, key=lambda x: x["confidence"], reverse=True)[:2]
    return render_template("result.html", tags=top_tags)

def analyze_image(image_url):
    api_key = "acc_6a384b8802fdbc0"  # Tu API Key
    api_secret = "343e5e26e3f36267fc004716de3217d9"  # Tu API Secret
    url = "https://api.imagga.com/v2/tags"
    
    # Codificar credenciales en Base64
    credentials = f"{api_key}:{api_secret}"
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    
    headers = {"Authorization": f"Basic {encoded_credentials}"}
    params = {"image_url": image_url}
    
    # Depuración antes de la solicitud
    print("Realizando solicitud a la API de Imagga...")
    print(f"URL de la imagen: {image_url}")
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response_data = response.json()
        
        # Depuración después de recibir la respuesta
        print("Respuesta de la API:")
        print(response_data)
        
        return response_data
    except Exception as e:
        # Captura y muestra cualquier error
        print("Error durante la solicitud a la API:")
        print(e)
        return {"error": str(e)}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
