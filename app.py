from flask import Flask, render_template, request
from mbta_helper import find_stop_near

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/nearest_mbta", methods=["POST"])
def nearest_mbta():
    place_name = request.form.get("place_name")
    if not place_name:
        return render_template("error.html", message="Please enter a valid location.")
    try:
        stop_name, is_accessible = find_stop_near(place_name)
        return render_template("mbta_station.html", place=place_name, stop=stop_name, accessible=is_accessible)
    except Exception as e:
        return render_template("error.html", message=f"Error: {e}")

if __name__ == "__main__":
    app.run(debug=True)
