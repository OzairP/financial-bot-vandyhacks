from flask import Flask, request, jsonify
from backend.Bot import Bot
import traceback

# data format
# {
#     "user_id": "123ef",
#     "query": "What's the nearest ATM?",
#     "extra": {
#          "location": {
#                "lat": 123.412,
#                "long": 123.213
#           }
#     }
# }
app = Flask(__name__)

Bot = Bot()


@app.route("/queries", methods=['POST'])
def run_features():
    try:
        data = request.get_json()
        print(data)
        response = Bot.parse(data["user_id"], data["query"])
        print(response)
        # print(jsonify(response))
        return jsonify(response)
    except:
        return jsonify(error=404, exception=traceback.format_exc())


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True)




# EXAMPLE DESIGN PATTERN
# @app.route("/queries")
# def get_balance():
#     send.Bot.hear("ferefrerfe")
#     return "Hello World!"
#
# class Bot:
#     def static hear(query):
#         parse
#         if parse == balance:
#             get_balance()
