from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process_data', methods=['POST'])
def process_data():
    data = request.json
    
    # Process the data here
    processed_data = data['some_key'] * 2

    return jsonify({'result': processed_data})

if __name__ == '__main__':
    app.run(debug=True)
