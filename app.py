from flask import Flask, render_template, request, session, redirect
import random

app = Flask(__name__)
app.secret_key = "secret123"

@app.route("/", methods=["GET", "POST"])
def start_game():
    message = ""

    # Initialize attempts (same as your attempts = 0)
    if "attempts" not in session:
        session["attempts"] = 0

    if request.method == "POST":

        user_input = request.form.get("action")

        # ===== START GAME (your range input part) =====
        if user_input == "start":
            try:
                low = int(request.form.get("low"))
                high = int(request.form.get("high"))
            except:
                message = "Please enter valid numbers for range."
                return render_template("index.html", message=message)

            if low >= high:
                message = "Minimum should be less than maximum."
            else:
                session["number"] = random.randint(low, high)
                session["attempts"] = 0
                session["low"] = low
                session["high"] = high
                message = f"Game started between {low} and {high}"

        # ===== RESTART (same as your restart) =====
        elif user_input == "restart":
            return redirect("/")

        # ===== STOP (same as break) =====
        elif user_input == "stop":
            session.clear()
            message = "Game stopped"

        # ===== GUESS (your guessing logic) =====
        elif user_input == "guess":
            if "number" not in session:
                message = "Start the game first!"
            else:
                user_guess = request.form.get("guess")

                if user_guess.lower() == "restart":
                    return redirect("/")

                if user_guess.lower() == "stop":
                    session.clear()
                    message = "Game stopped"
                else:
                    try:
                        guess = int(user_guess)
                    except:
                        message = "Enter a valid number."
                        return render_template("index.html", message=message)

                    session["attempts"] += 1

                    if guess == session["number"]:
                        message = f"Correct! Attempts: {session['attempts']}"
                        session.clear()
                    elif guess < session["number"]:
                        message = "Up"
                    else:
                        message = "Down"

    return render_template(
        "index.html",
        message=message,
        attempts=session.get("attempts", 0)
    )

if __name__ == "__main__":
    app.run(debug=True)