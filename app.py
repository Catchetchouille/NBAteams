from flask import Flask, render_template, request
import nba_api  # your existing Python API

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    user_input = request.form["user_input"]
    
    # Call your Python API here
    result = nba_api(user_input)
    
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)