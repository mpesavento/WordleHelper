from flask import Flask, request
from markupsafe import escape

from wordle_helper.wordle_filters import WordleFilters

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return (
        f"Welcome to Yet Another Wordle Helper API!<br/>")


@app.route("/api/filter")
def filter_possible_words():
    # print out query for now
    # use escape to sanitize the query input
    excluded_letters = escape(request.args.get("exclude"))
    position_letters = escape(request.args.get("position"))
    unpositioned_letters = escape(request.args.get("unpos"))

    wordle_filters = WordleFilters()

    possible_words = wordle_filters.run_iter(excluded_letters, position_letters, unpositioned_letters)

    page = f"""
    <h2>Excluded letters</h2><p>{excluded_letters}</p>
    <h2>Positioned letters</h2><p>{position_letters}</p>
    <h2>Unpositioned letters</h2><p>{unpositioned_letters}</p>
    <h1>Possible words</h1><p>{possible_words}</p>
    """

    return page


if __name__ == '__main__':
    app.run()
