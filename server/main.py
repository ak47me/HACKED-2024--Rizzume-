from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/resume', methods=['POST'])
def process_data():
    data = request.json
    print(data)
    # Process the data here
    processed_data = data['0'] * 2
    print(processed_data)
    return jsonify({'result': processed_data})

if __name__ == '__main__':
    app.run(debug=True)
