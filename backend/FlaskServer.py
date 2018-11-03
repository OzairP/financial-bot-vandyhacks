from flask import Flask, request, jsonify
from Bot import Bot
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

@app.route("/queries/run_features", methods=['GET', 'POST'])
def run_features():
    query = request.get_json()
    result = Bot.hear(query)
    return jsonify(result)


if __name__ == "__main__":
    print("Hello World")



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