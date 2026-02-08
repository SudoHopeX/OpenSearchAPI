from flask import Flask, request, jsonify, render_template
from engines import search

app = Flask(__name__)

ENGINES = ["google", "duckduckgo", "bing"] #, "brave"]

@app.route("/search")
def handle_search():
    query = request.args.get("q")
    engine = request.args.get("engines", "duckduckgo").lower()

    if not query:
        return jsonify({"error": "Missing query parameter 'q'"}), 400

    if engine not in ENGINES:
        return jsonify({"error": f"Engine must be one of {ENGINES}"}), 400

    results = search(query, engine)
    return jsonify({
        "query": query,
        "engine": engine,
        "results": results
    })


@app.route("/mega/search")
def handle_mega_search():
    query = request.args.get("q")
    engines_param = request.args.get("engine", "google").lower()

    if not query:
        return jsonify({"error": "Missing query parameter 'q'"}), 400

    requested_engines = [e.strip() for e in engines_param.split(",")]

    invalid_engines = [e for e in requested_engines if e not in ENGINES]
    if invalid_engines:
        return jsonify({"error": f"Invalid engines: {invalid_engines}. Must be one of {ENGINES}"}), 400

    all_results = {}
    for engine in requested_engines:
        results = search(query, engine)
        all_results[engine] = results

    return jsonify({
        "query": query,
        "engines": requested_engines,
        "results": all_results
    })

@app.route("/")
def index():
    host = request.host  # e.g., "127.0.0.1:5000", "localhost:5000", or "10.10.10.10:5000"
    return render_template("index.html", host=host)


if __name__ == "__main__":
    app.run(port=5000, debug=False, threaded=True)

