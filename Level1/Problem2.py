from flask import Flask, request, jsonify,url_for
app = Flask(__name__)

data = {}
@app.route("/create", methods=['POST'])
def create():
    if(request.method == 'POST'):
        global data
        data = request.get_json()            
        return jsonify({"msg": f"data received: {data}"})
        # return f"data: {data}"
    else:
        return 'please make POST request'


@app.route("/read", methods=['GET'])
def read():
    return jsonify({"data": data})


@app.route("/update", methods=['PUT', 'PATCH'])
def update():
    global data
    if(request.method == 'PUT'):
        data = request.get_json()
    elif(request.method == 'PATCH'):
        temp = request.get_json()
        data.update(temp)
        
    return jsonify({"udpated data": data})

@app.route('/delete', methods=['POST'])
def delete():
    global data
    inp = request.get_json()
    key = list(inp.keys())
    for i in key:
        if i in data:
            data.pop(i)
    return jsonify({"after delete": data, 'key_deleted': key})


if __name__ == '__main__':
    app.run()