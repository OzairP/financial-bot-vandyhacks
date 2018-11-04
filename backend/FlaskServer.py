from flask import Flask, request, jsonify
from backend.Bot import Bot
app = Flask(__name__)


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

Bot = Bot()


@app.route("/queries", methods=['GET', 'POST'])
def run_features():
    data = request.get_json()
    print(data)
    response = Bot.parse(data["user_id"], data["query"])
    return jsonify(response)


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