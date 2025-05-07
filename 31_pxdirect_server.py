import csv
from flask import Flask, jsonify,request, Response

# flask route to read csv file and return json
app = Flask(__name__)


@app.route('/endpoints', methods=['GET'])
def read_csv():
    # Basic authentication
    auth = request.authorization
    if not auth or auth.username != 'cisco' or auth.password != 'cisco':
        return Response(
            'Could not verify your access level for that URL.\n'
            'You have to login with proper credentials', 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        )

    # Read the CSV file and return  a JSON response
    data = []
    try:
        with open("pxdirect_server.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return jsonify({"data": data})
    except FileNotFoundError:
        return jsonify({"error": "CSV file not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)