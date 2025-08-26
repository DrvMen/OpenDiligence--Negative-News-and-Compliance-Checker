from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import fetch_all_sources

app = Flask(__name__)
CORS(app)


@app.route("/api/search", methods=["POST"])
def search():
    try:
        data = request.get_json()
        query = data.get("query", "")

        if not query:
            return jsonify({"error": "Query required"}), 400

        articles = fetch_all_sources(query)

        return jsonify({"articles": articles})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
