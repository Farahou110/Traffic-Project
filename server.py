from flask import Flask, request, jsonify, render_template, session,url_for,redirect,flash
from pymongo import MongoClient
import requests
from dotenv import load_dotenv
import os




client = MongoClient("mongodb://localhost:27017/")
db = client["Traffic_project"]
vehicle_table = db["vehicles"]
visitors = db["visitor"]

app = Flask(__name__)



load_dotenv()

app.secret_key =os.getenv("secret_key")
MAPBOX_ACCESS_TOKEN=os.getenv("MAPBOX_ACCESS_TOKEN")



@app.route("/")
def home():
    leaflet.html
    return render_template("front.html", MAPBOX_ACCESS_TOKEN=mapboxgl.accessToken)

@app.route("/verify", methods=["POST"])  
def verify_plate():
    if request.method == "POST":
        plate_number = request.form["plate_number"]
        Owner_ID = request.form["Owner_ID"]
        Owner_Name = request.form["Owner_name"]

        session['username'] = Owner_Name

        # Inserting vehicle data into the database
        vehicle_table.insert_one({
            "plate_number": plate_number,
            "Owner_ID": Owner_ID,
            "Owner_name": Owner_Name
        })

        # Fetch user data from NTSA data
       
        user = visitors.find_one({ "username": Owner_Name })
        print(user)
        
        if user:
            # app.logger.info("User found: Rendering dash.html,{Owner_Name}")
            # flash("Verified successfully!", "success")
            MAPBOX_ACCESS_TOKEN=("mapboxgl.accessToken")
            return render_template("dash.html", MAPBOX_ACCESS_TOKEN=os.getenv("mapboxgl.accessToken"), username=session.get("username"))
        else:
            # app.logger.info({Owner_Name})
            # flash("Vehicle not found, please try again.", "error")
            return redirect(url_for("home"))



@app.route("/calculate_route", methods=["POST"])
def calculate_route():
    # Extract user info from request
    user_location = request.json.get("user_location")  # {lat: ..., lng: ...}
    destination = request.json.get("destination")  # {lat: ..., lng: ...}

    if not user_location or not destination:
        return jsonify({"success": False, "msg": "Missing location or destination"}), 400

    # Make a request to Mapbox Directions API to calculate the route with traffic data
    directions_url = f'https://api.mapbox.com/directions/v5/mapbox/driving/{user_location["lng"]},{user_location["lat"]};{destination["lng"]},{destination["lat"]}?access_token={MAPBOX_ACCESS_TOKEN}&alternatives=true&geometries=geojson&steps=true'

    response = requests.get(directions_url)
    if response.status_code != 200:
        return jsonify({"success": False, "msg": "Error fetching route data"}), 500

    route_data = response.json()
    routes = route_data.get("routes", [])

    # Store route details in database (this is just an example, adjust based on your data model)
    for route in routes:
        vehicle_data = {
            "username": session.get("username"),
            "distance": route["distance"],  # in meters
            "duration": route["duration"],  # in seconds
            "steps": route["legs"][0]["steps"],  # Detailed steps
            "traffic": "Traffic data will be fetched here"  # Placeholder for traffic data
        }
        vehicle_table.insert_one(vehicle_data)

    return jsonify({"success": True, "routes": routes})



if __name__ == "__main__":
    app.run(debug=True)
