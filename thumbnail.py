from app import app
import json

@app.route('/api/thumbnail', methods=['GET'])
def ConvertToThumbnail():
    data = {"Message":"This method converts an original image to a thumbnail."}
    response = app.response_class(response=json.dumps(data),
                                  status=200,
                                  mimetype='application/json')
    
    return response