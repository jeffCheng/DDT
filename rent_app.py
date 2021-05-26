from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import re


app = Flask(__name__)
app.config['MONGO_DBNAME'] = '591'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/591'

mongo = PyMongo(app)

@app.route('/api/v1/resources/rent', methods=['GET'])
def get_rent_by_region():
    rents = mongo.db.rent
    output = []
    query = dict()
    if 'region' in request.args:
        query['region_name'] = request.args['region']
    if 'renter_name' in request.args:
        query['linkman'] = request.args['renter_name']
    if 'renter_type' in request.args:
        query['nick_name'] = request.args['renter_type']
    if 'non_renter_type' in request.args: #非屋主
        query['nick_name'] = {"$ne":request.args['non_renter_type']} 
    if 'gender' in request.args:
        query['gender'] = {"$in":[int(request.args['gender']),2]} # 女生 or 男生 or 皆可
        gender_list = ['女生','男生','男女生皆可']
    for rent in rents.find(query):
        output.append({'region': rent['region_name'], 'renter_name' : rent['linkman'], 'renter_type' : rent['nick_name'], 'type_name' : rent['type_name'], 'kind_name' : rent['kind_name'], 'phone_number' : rent['phone_number'], 'gender' : gender_list[rent['gender']] ,'post_link': "https://rent.591.com.tw/rent-detail-"+str(rent['url_id'])+".html"})
    
    return jsonify({'result' : output})

# 以【聯絡電話】查詢租屋物件
@app.route('/api/v1/resources/rent/phone/<phone_number>', methods=['GET'])
def get_rent_by_phone(phone_number):
    rents = mongo.db.rent
    rgx = re.compile('.*'+phone_number+'.*', re.IGNORECASE) 
    output = []
    query = {"phone_number": rgx}
    gender_list = ['女生','男生','男女生皆可']
    for rent in rents.find(query):
        output.append({'region': rent['region_name'], 'renter_name' : rent['linkman'], 'renter_type' : rent['nick_name'], 'type_name' : rent['type_name'], 'kind_name' : rent['kind_name'], 'phone_number' : rent['phone_number'], 'gender' : gender_list[rent['gender']] ,'post_link': "https://rent.591.com.tw/rent-detail-"+str(rent['url_id'])+".html"})
    return jsonify({'result' : output})

