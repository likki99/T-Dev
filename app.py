import requests
import os
from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from

import config as cf
app = Flask(__name__)
swagger_config = Swagger.DEFAULT_CONFIG
Swagger(app, config=swagger_config)


@app.route('/connect', methods=['POST', 'OPTIONS'])
@swag_from(os.path.join(cf.BASE_PATH, "api_docs", "connect_swag.yml"))
def connect():
    if 'file' in request.files:
        file = request.files['file']
        file.save(os.path.join('uploads', file.filename))
        return jsonify({'message': 'File uploaded successfully'})

    elif 'url' in request.json:
        url = request.json['url']
        try:
            response = requests.get(url)
            # Save the file from URL
            with open(os.path.join('uploads', url.split('/')[-1]), 'wb') as f:
                f.write(response.content)
            return jsonify({'message': 'File downloaded and saved successfully'})
        except Exception as e:
            return jsonify({'error': str(e)})

    else:
        return jsonify({'error': 'No file or URL provided'}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)
