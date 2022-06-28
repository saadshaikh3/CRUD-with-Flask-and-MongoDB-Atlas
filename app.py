from flask import Flask, request, jsonify, redirect
import pymongo
from flask.helpers import url_for
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from bson.objectid import ObjectId

app= Flask(__name__)

try:
    CONNECTION_STRING = "mongodb+srv://saadshaikh:saad12345@cluster0.uvqy4qi.mongodb.net/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(CONNECTION_STRING)
    db = client.get_database('Test')
    user_collection = pymongo.collection.Collection(db, 'user_collection')

    app.config["JWT_SECRET_KEY"] = "tHis123IsCrEATedFoR123Test"   ##### random string for Json Web Token generation
    jwt = JWTManager(app)

except:
    print("ERROR - cant connect")


@app.route("/register", methods=["POST"])               ####### first endpoint
def create_user():
    try:

        first_name=request.json["first_name"]
        last_name=request.json["last_name"]
        email=request.json["email"]
        password=request.json["password"]

        db.users.insert_one({"first_name":first_name,                   ###### collection named as Users
        "last_name":last_name,
        "email":email,
        "password":password})

        return jsonify({"first_name":first_name,
        "last_name":last_name,
        "email":email,
        "password":password})

    except Exception as ex:
        print(ex)


@app.route("/login", methods=["POST"])                  #####second endpoint
def login_user():
    try:
       
        email=request.json["email"]
        password=request.json["password"]

        db.users.insert_one({
        "email":email,
        "password":password})

        access_token = create_access_token(identity=email)

        return jsonify({
        "email":email,
        "password":password,
        "access_token":access_token})

    except Exception as ex:
        print(ex)


@app.route("/template", methods=["POST"])                      ######third endpoint
@jwt_required()
def template_info():
    try:
       
        template_name=request.json["template_name"]
        subject= request.json["subject"]
        body=request.json["body"]

        db.templates.insert_one({                               ######## new collection Templates
        "template_name":template_name,
        "subject":subject,
        "body":body})

        return jsonify({
        "template_name":template_name,
        "subject":subject,
        "body":body})

    except Exception as ex:
        print(ex)


@app.route("/template", methods=["GET"])
@jwt_required()
def all_temp():
    try:
       
        holder = []
        for i in db.templates.find():
            holder.append({'template_name':i['template_name'], 'subject' : i['subject'], 'body' : i['body']})
        return jsonify(holder)

    except Exception as ex:
        print(ex)


@app.route("/template/<string:template_id>", methods=["GET"])               ###### to retrieve a single template
@jwt_required()
def single_temp(template_id):

    try:     
        data = db.templates.find_one({"_id" : ObjectId(template_id)})
        return jsonify({
        "template_name":data["template_name"],
        "subject":data["subject"],
        "body":data["body"]})

    except Exception as ex:
        print(ex)


@app.route("/template/<string:template_id>", methods=["PUT"])                   ######to update attribute
@jwt_required()
def update_temp(template_id):

    try:      
        up_template_name=request.json["template_name"]
        up_subject= request.json["subject"]
        up_body=request.json["body"]
        db.templates.update_one({"_id" : ObjectId(template_id)},{"$set": 
        {"template_name" : up_template_name,"subject":up_subject,"body":up_body}})
        return redirect(url_for('all_temp'))
        
    except Exception as ex:
        print(ex)


@app.route("/template/<string:template_id>", methods=["DELETE"])                        ###### to delete a template
@jwt_required()
def delete_temp(template_id):

    try:      
        db.templates.delete_one({"_id" : ObjectId(template_id)})
        return redirect(url_for('all_temp'))

    except Exception as ex:
        print(ex)


if __name__=="__main__":
    app.run(debug=True)
