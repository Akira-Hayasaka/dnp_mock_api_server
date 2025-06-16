from flask import Flask, request, jsonify
import base64, time, os, mimetypes

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Base64 画像エンコード

def encode_image_base64(path):
    full_path = os.path.join(BASE_DIR, path)
    mime_type, _ = mimetypes.guess_type(full_path)
    if not mime_type:
        mime_type = "application/octet-stream"
    with open(full_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"

DUMMY_MP3 = "http://localhost:8000/static/winning_sound.wav"

@app.route("/api/goods/all", methods=["GET"])
def get_all_goods():
    try:
        type_img = encode_image_base64("static/img/test.png")
        win_img = encode_image_base64("static/img/test.png")
        name_img = encode_image_base64("static/img/test.png")
        all_img = encode_image_base64("static/img/test.png")
        prize_img = encode_image_base64("static/img/test.png")

        return jsonify({
            "data": {
                "gacha": {
                    "id": 1,
                    "prize": "A賞",
                    "types": [
                        {"id": 1, "initial": 4000, "stock": 3234},
                        {"id": 2, "initial": 4000, "stock": 3200}
                    ]
                },
                "dice": {
                    "id": 1,
                    "prizes": [
                        {"id": 1, "prize": "A賞", "initial": 4000, "stock": 3234},
                        {"id": 2, "prize": "B賞", "initial": 4000, "stock": 3200}
                    ]
                }
            }
        })
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/api/goods/gacha", methods=["GET"])
def get_gacha_goods():
    try:
        full_data = get_all_goods().json
        return jsonify({"data": {"gacha": full_data["data"]["gacha"]}})
    except Exception:
        return jsonify({"error": "Failed to retrieve gacha data"}), 500

@app.route("/api/goods/dice", methods=["GET"])
def get_dice_goods():
    try:
        full_data = get_all_goods().json
        return jsonify({"data": {"dice": full_data["data"]["dice"]}})
    except Exception:
        return jsonify({"error": "Failed to retrieve dice data"}), 500

@app.route("/api/goods/decrement", methods=["POST"])
def decrement_stock():
    data = request.json
    required = {"game_type", "prize", "decrement"}
    if not required.issubset(data):
        return jsonify({"error": "Invalid parameter: prize_id"}), 400
    return jsonify({"success": True}), 200

@app.route("/api/qrcode/consume", methods=["POST"])
def consume_qr():
    data = request.get_json()
    token = data.get("token", "")

    if not isinstance(token, str) or len(token) != 16:
        return jsonify({"success": False, "message": "Invalid or already used token."}), 400

    if token == "USED":
        return jsonify({"success": False, "message": "Token already used."}), 400

    return jsonify({
        "success": True,
        "message": "Token successfully consumed",
        "token": token,
        "used_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }), 200

@app.route("/api/user/record", methods=["POST"])
def user_record():
    data = request.json
    required_fields = {"game_type", "game_at", "times", "use_qr", "prizes"}
    if not required_fields.issubset(data):
        return jsonify({"error": "Missing field: game_type"}), 400
    return jsonify({"success": True, "data": data}), 201

if __name__ == "__main__":
    app.run(debug=True, port=8000)
