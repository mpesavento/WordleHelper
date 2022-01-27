from flask import Flask, request, render_template, url_for, flash, redirect
from markupsafe import escape

from wordle_helper.wordle_filters import WordleFilters
from wordle_helper.word_list import find_first_guess


# -----------
# create the app instance
app = Flask(__name__)
app.config['SECRET_KEY'] = '90cccb9f24224248d93fdda06fa7af8e1875331fd77bb86c'

# leave this as a global for now?
first_guesses = find_first_guess()


@app.route("/")
@app.route("/index")
def index():
    possible_words = None
    excluded_letters = escape(request.args.get("excluded"))
    position_letters = escape(request.args.get("positioned"))
    unpositioned_letters = escape(request.args.get("unpositioned"))

    if request.method == 'GET' and excluded_letters:

        wordle_filters = WordleFilters()
        possible_words = wordle_filters.run_iter(excluded_letters, position_letters, unpositioned_letters)
        # title = request.form['title']
        # content = request.form['content']
        #
        # if not title:
        #     flash('Title is required!')
        # elif not content:
        #     flash('Content is required!')
        # else:
        #     messages.append({'title': title, 'content': content})
        #     return redirect(url_for('index'))
    return render_template('index.html', possible_words=possible_words)
    # return (
    #     f"Welcome to Yet Another Wordle Helper API!<br/>")


@app.route("/first_guess")
def first_guess():
    return render_template('first_guess.html', first_guesses=first_guesses)


# @app.route('/create/', methods=('GET', 'POST'))
# def create():
#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']
#
#         if not title:
#             flash('Title is required!')
#         elif not content:
#             flash('Content is required!')
#         else:
#             messages.append({'title': title, 'content': content})
#             return redirect(url_for('index'))
#     return render_template('create.html')


@app.route("/about")
def about():
    return render_template('about.html')


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
