from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

app = Flask(__name__)

def extract_natura_info(url):
    return {
        "nome": "Ekos Maracujá Desodorante Colônia 150ml",
        "preco": "R$ 79,90",
        "parcelamento": "em até 3x R$ 26,63",
        "imagem_url": "https://cdn.natura.com/cdn/ff/w1Wy59R03Y50ZX5PFFvOK2XbQynLMxqUKEULJUxlU3w/1684231010/public/styles/292x384/public/product-images/54316_1_3.jpg"
    }

def generate_image(produto):
    response = requests.get(produto["imagem_url"])
    img = Image.open(BytesIO(response.content)).convert("RGB")
    img = img.resize((600, 600))
    background = Image.new("RGB", (600, 800), (255, 255, 255))
    background.paste(img, (0,0))
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 28)
    draw.text((20,620), produto["nome"], fill="black", font=font)
    draw.text((20,680), produto["preco"], fill="green", font=font)
    draw.text((20,720), produto["parcelamento"], fill="gray", font=font)
    path = "/tmp/natura_post.jpg"
    background.save(path)
    return path

@app.route("/gerar-post", methods=["POST"])
def gerar_post():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"erro": "URL não fornecida"}), 400
    produto = extract_natura_info(url)
    image_path = generate_image(produto)
    mensagem = f"🌿 {produto['nome']}\n💰 {produto['preco']} ({produto['parcelamento']})\n🛍️ Compre aqui: {url}"
    return jsonify({"mensagem": mensagem}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
