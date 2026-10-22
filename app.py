
from flask import Flask, render_template, request, redirect, url_for, session
from sudoku_logic import generate_game, is_valid
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-key-change-before-deployment")


def new_game():
    puzzle, solution = generate_game()
    session["puzzle"] = puzzle
    session["solution"] = solution
    session["initial"] = [row[:] for row in puzzle]
    session["lives"] = 3
    session["message"] = "Game started! Fill in the empty cells."
    session["message_type"] = "info"
    session["won"] = False


@app.route("/", methods=["GET", "POST"])
def index():
    if "puzzle" not in session:
        new_game()

    if request.method == "POST":
        action = request.form.get("action")

        if action == "new":
            new_game()
            return redirect(url_for("index"))

        if action == "move" and not session.get("won", False):
            try:
                row = int(request.form.get("row", "")) - 1
                col = int(request.form.get("col", "")) - 1
                num = int(request.form.get("number", ""))

                puzzle = session["puzzle"]
                solution = session["solution"]
                initial = session["initial"]

                if not (0 <= row < 9 and 0 <= col < 9 and 1 <= num <= 9):
                    raise ValueError

                if initial[row][col] != 0:
                    session["message"] = "That cell is fixed. Choose an empty cell."
                    session["message_type"] = "error"

                elif puzzle[row][col] != 0:
                    session["message"] = "That cell is already filled."
                    session["message_type"] = "error"

                elif num == solution[row][col]:
                    puzzle[row][col] = num
                    session["puzzle"] = puzzle

                    if all(0 not in line for line in puzzle):
                        session["won"] = True
                        session["message"] = "Congratulations! You solved Sudoku!"
                        session["message_type"] = "success"
                    else:
                        session["message"] = "Correct move!"
                        session["message_type"] = "success"

                else:
                    session["lives"] -= 1
                    session["message"] = (
                        f"Incorrect number! {session['lives']} lives remaining."
                    )
                    session["message_type"] = "error"

                    if session["lives"] <= 0:
                        session["message"] = "Game over! Start a new game to try again."
                        session["message_type"] = "error"
                        session["won"] = True

            except (ValueError, TypeError):
                session["message"] = "Enter a valid row, column, and number."
                session["message_type"] = "error"

        return redirect(url_for("index"))

    return render_template(
        "index.html",
        puzzle=session["puzzle"],
        initial=session["initial"],
        lives=session["lives"],
        message=session["message"],
        message_type=session["message_type"],
        won=session["won"],
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

