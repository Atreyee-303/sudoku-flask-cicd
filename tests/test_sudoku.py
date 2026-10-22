
from app import app
from sudoku_logic import generate_game


def setup_client():
    app.config["TESTING"] = True
    return app.test_client()


def test_generated_puzzle():
    puzzle, solution = generate_game()

    assert len(puzzle) == 9
    assert all(len(row) == 9 for row in puzzle)
    assert sum(row.count(0) for row in puzzle) == 40

    expected = set(range(1, 10))

    # Check every row, column, and 3x3 box in the solution.
    for i in range(9):
        assert set(solution[i]) == expected
        assert {solution[r][i] for r in range(9)} == expected

    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            box = [
                solution[r][c]
                for r in range(box_row, box_row + 3)
                for c in range(box_col, box_col + 3)
            ]
            assert set(box) == expected


def test_homepage_loads():
    client = setup_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"Sudoku" in response.data


def test_correct_move():
    client = setup_client()
    client.get("/")

    with client.session_transaction() as session:
        puzzle = session["puzzle"]
        solution = session["solution"]

        row, col = next(
            (r, c)
            for r in range(9)
            for c in range(9)
            if puzzle[r][c] == 0
        )
        number = solution[row][col]

    response = client.post(
        "/",
        data={
            "action": "move",
            "row": row + 1,
            "col": col + 1,
            "number": number,
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Correct move!" in response.data

    with client.session_transaction() as session:
        assert session["puzzle"][row][col] == number
        assert session["lives"] == 3


def test_incorrect_move_reduces_lives():
    client = setup_client()
    client.get("/")

    with client.session_transaction() as session:
        puzzle = session["puzzle"]
        solution = session["solution"]

        row, col = next(
            (r, c)
            for r in range(9)
            for c in range(9)
            if puzzle[r][c] == 0
        )
        wrong_number = next(
            n for n in range(1, 10)
            if n != solution[row][col]
        )

    response = client.post(
        "/",
        data={
            "action": "move",
            "row": row + 1,
            "col": col + 1,
            "number": wrong_number,
        },
        follow_redirects=True,
    )

    assert response.status_code == 200

    with client.session_transaction() as session:
        assert session["lives"] == 2
        assert session["puzzle"][row][col] == 0


def test_fixed_cell_cannot_be_changed():
    client = setup_client()
    client.get("/")

    with client.session_transaction() as session:
        initial = session["initial"]
        row, col = next(
            (r, c)
            for r in range(9)
            for c in range(9)
            if initial[r][c] != 0
        )
        original = initial[row][col]

    response = client.post(
        "/",
        data={
            "action": "move",
            "row": row + 1,
            "col": col + 1,
            "number": original,
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"That cell is fixed" in response.data


def test_new_game_resets_lives():
    client = setup_client()
    client.get("/")

    # First, lose one life.
    with client.session_transaction() as session:
        puzzle = session["puzzle"]
        solution = session["solution"]
        row, col = next(
            (r, c)
            for r in range(9)
            for c in range(9)
            if puzzle[r][c] == 0
        )
        wrong_number = next(
            n for n in range(1, 10)
            if n != solution[row][col]
        )

    client.post(
        "/",
        data={
            "action": "move",
            "row": row + 1,
            "col": col + 1,
            "number": wrong_number,
        },
    )

    # Start a new game.
    response = client.post(
        "/",
        data={"action": "new"},
        follow_redirects=True,
    )

    assert response.status_code == 200

    with client.session_transaction() as session:
        assert session["lives"] == 3
        assert sum(row.count(0) for row in session["puzzle"]) == 40

