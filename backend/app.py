from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import PickASong
import random

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET'])
def process_heart_rate():
    try:
        # Get heart rate from the query parameters
        heart_rate = int(request.args.get('heartRate'))    
        resting_hr = int(request.args.get('restingHR'))    

        # have model return number
        returnedSong = PickASong.pickASong(heart_rate, resting_hr)
        print(returnedSong)

        # Return the selected MP3 file as a response
        return jsonify({"returnedSong" : returnedSong}), 200
    except ValueError:
        return jsonify({'error': 'Invalid heart rate value. It should be a number.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)