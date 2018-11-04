from flask import Flask, request, jsonify
from backend.Bot import Bot
import traceback

app = Flask(__name__)
Bot = Bot()


@app.route("/queries", methods=['POST'])
def run_features():
    try:
        data = request.get_json()
        response = Bot.parse(data["user_id"], data["query"])
        return jsonify(response)
    except:
        return jsonify(error=404, exception=traceback.format_exc())


if __name__ == "__main__":
    # app.run(debug=True, threaded=True)
    app.run(host='0.0.0.0', debug=True, threaded=True)
