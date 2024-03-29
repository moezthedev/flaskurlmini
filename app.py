from flask import Flask,render_template,jsonify,redirect,request
from pymongo import MongoClient
import urllib.parse
import random
import os
app = Flask(__name__)
def connect_to_mongodb():
   try:
     uri_name = os.environ.get('uri_name')
     uri_pass = os.environ.get('uri_pass')
     project_details = os.environ.get('project_details')
     mongo_uri = os.environ.get('mongo_uri')
     client = MongoClient(mongo_uri,connect=False)
     print("Connected To MongoDB client successfully")
     
     
     return client
   except  Exception as e:
      print(e)
      
      return "Error connecting MongoDB Client"
 
@app.route('/', methods=['GET'])
def Home():
   
   return render_template("index.html")

@app.route('/post/', methods=['POST',"GET"])
def gen_code():
    
    url_from_user = request.form.get("url_from_user")
    if url_from_user:
      client =  connect_to_mongodb()
      db = client.get_database("URLMinifier")
      collection = db.get_collection("codeNum")
      random_number = str(random.randint(1000, 10000000))
      
      result = collection.insert_one({random_number: url_from_user}) 
    if result.acknowledged==True:
       shortened_url = request.host+"/" + random_number
       #print(shortened_url)
       return render_template("success.html",shortened_url=shortened_url)
       #jsonify({"status":result.acknowledged,"message":"Url added successfully","data":request.host+"/" + random_number})
    
    elif result.acknowledged==False:
      return render_template("fail.html")
    #jsonify({"status":result.acknowledged,"message":"Url was not added successfully"})
    

    
   
@app.route('/<codeValue>', methods=['GET'])
def access_code(codeValue):
   try:
      client =  connect_to_mongodb()
      db =  client.get_database("URLMinifier")
      collection = db.get_collection("codeNum")
      result = collection.find_one({codeValue:{'$exists': True}}) 
      list_of_matched_keyval = list(result.values())
      matched_code_value = list_of_matched_keyval[1]
      print(matched_code_value)
      return redirect("https://"+matched_code_value)
      
      
      
      
      
   except Exception as e:
      print(e)
      
      
   return "An unexpected problem has occurred Please try again."   
@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')   
 
if __name__ == "__main__":
    app.run(debug=True,port=8000,host="0.0.0.0")
