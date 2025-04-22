from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from database import create_connection, create_table, insert_matches, query_player_matches
from call_champions import fetch_jungle_data
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

api_key = os.getenv("RIOT_API_KEY")
if not api_key:
    logger.warning("RIOT_API_KEY não está definida no ambiente.")

try:
    conn = create_connection()
    logger.info("Conexão com o banco estabelecida")
except Exception as e:
    logger.error(f"Erro ao conectar ao banco: {e}")
    conn = None

@app.route("/")
def serve_html():
    return send_file("index_um_jogador_botoes_api20.html", mimetype="text/html")

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "api_key_configured": bool(api_key)}), 200

@app.route("/player", methods=["GET"])
def get_player():
    game_name = request.args.get("name")
    tag_line = request.args.get("tag")
    server_code = request.args.get("server", "br")

    if not game_name or not tag_line:
        return jsonify({"error": "Name and tag are required parameters"}), 400
    if not conn:
        return jsonify({"error": "Database connection not available"}), 500

    player_name = f"{game_name}#{tag_line}"

    try:
        matches = query_player_matches(conn, player_name)
        return jsonify(matches), 200
    except Exception as e:
        logger.error(f"Erro ao buscar jogador: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/player", methods=["POST"])
def post_player():
    data = request.get_json()
    if not data or not data.get("name") or not data.get("tag"):
        return jsonify({"error": "Name and tag are required"}), 400
    if not conn:
        return jsonify({"error": "Database connection not available"}), 500

    game_name = data["name"]
    tag_line = data["tag"]
    server_code = data.get("server", "br")
    count = int(data.get("count", 10))

    if not api_key:
        return jsonify({"error": "API key not configured"}), 500

    try:
        data_list = fetch_jungle_data(game_name, tag_line, server_code, count=count)
        if data_list:
            insert_matches(conn, data_list)
            matches = query_player_matches(conn, f"{game_name}#{tag_line}")
            return jsonify({"message": "Data updated", "matches": matches}), 201
        else:
            return jsonify({"error": "No data returned from API"}), 404
    except Exception as e:
        logger.error(f"Erro no POST /player: {e}")
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Route not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    if conn:
        try:
            create_table(conn)
            logger.info("Tabela verificada com sucesso")
        except Exception as e:
            logger.error(f"Erro ao criar/verificar tabela: {e}")
    app.run(debug=True, host="0.0.0.0")