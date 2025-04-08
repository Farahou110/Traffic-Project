from flask import Flask, request, jsonify

app = Flask(__name__)

mock_db = {
    "KDA123A": {"make": "Toyota", "model": "Axio", "owner": "John Doe", "status": "Valid"},
    "KCE456B": {"make": "Nissan", "model": "Note", "owner": "Jane Mwangi", "status": "Insurance Expired"},
    "KDD789C": {"make": "Mazda", "model": "Demio", "owner": "Ali Yusuf", "status": "Roadworthy"},
}

@app.route("/verify", methods=["POST"])
def verify_plate():
    plate = request.json.get("plate_number")
    data = mock_db.get(plate.upper())
    if data:
        return jsonify({"success": True, "data": data})
    else:
        return jsonify({"success": False, "error": "Plate not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
