from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [
    {
        "name": "My Wonderful Store",
        "items": [
            {
                "name": "My Item",
                "price": 15.99
            }
        ]
    }
]

@app.route('/')
def home():
    return render_template('index.html')


# POST  /store {name:}                                       #* POST / Create a new store with the given name
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store ={
        "name":request_data["name"],
        "items": []
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET   /store/<string:name>                                 #* GET / Return a new store with the given name
@app.route('/store/<string:name>')                           #? The default method is GET, so no need to mention it in 'methods=[]'
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return jsonify(store)
        return jsonify({"message": "Store Not Found!"})

# GET   /store                                               #* GET / Return a list of stores
@app.route('/store')
def get_stores():
    return jsonify({'stores':stores})

# POST  /store/<string:name>/item {name:, price:}            #* POST / Create an item inside a specific store with the given name
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {
                "name": request_data['name'],
                "price": request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({"message": "Store Not Found!"})

# GET   /store<string:name>/item                             #* GET / Return all the items in a specific store
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    for store in stores:
        if store["name"] == name:
            return jsonify({"items":store["items"]})
    return jsonify({"message": "Store/Item Not Found!"})


app.run(port=8000)