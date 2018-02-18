from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine

db_connect = create_engine('sqlite:///chinook.db')
app = Flask(__name__)
api = Api(app)

@app.route('/')
def api_root():
	return 'Rest API in flask framework'

class Employees(Resource):
	def get(self):
		conn = db_connect.connect()
		query = conn.execute("select * from employees;")
		return {'employees': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}

	def post(self):
		conn = db_connect.connect()
		LastName = request.json['LastName']
		FirstName = request.json['FirstName']
		Title = request.json['Title']
		ReportsTo = request.json['ReportsTo']
		BirthDate = request.json['BirthDate']
		HireDate = request.json['HireDate']
		Address = request.json['Address']
		City = request.json['City']
		State = request.json['State']
		Country = request.json['Country']
		PostalCode = request.json['PostalCode']
		Phone = request.json['Phone']
		Fax = request.json['Fax']
		Email = request.json['Email']
		query = conn.execute("insert into employees values(null,'{0}','{1}','{2}','{3}', \
                             '{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}', \
                             '{13}')".format(LastName,FirstName,Title,
                             ReportsTo, BirthDate, HireDate, Address,
                             City, State, Country, PostalCode, Phone, Fax,
                             Email))
		return {'status':'success'}
	

class Tracks(Resource):
	def get(self):
		conn = db_connect.connect()
		query = conn.execute("select trackid, name, composer, unitprice from tracks;")
		result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
		return jsonify(result)

	def post(self):
		conn = db_connect.connect()
		Name = request.json['Name']
		AlbumId = request.json['AlbumId']
		MediaTypeId = request.json['MediaTypeId']
		GenreId = request.json['GenreId']
		Composer = request.json['Composer']
		Milliseconds = request.json['Milliseconds']
		Bytes = request.json['Bytes']
		UnitPrice = request.json['UnitPrice']
		query = conn.execute("insert into tracks values(null,'{0}','{1}','{2}','{3}', \
                             '{4}','{5}','{6}','{7}')".format(Name,AlbumId,MediaTypeId,
                             GenreId, Composer, Milliseconds, Bytes,
                             UnitPrice))
		return {'status':'success'}	


class Track(Resource):
	def get(self, track_id):
		conn = db_connect.connect()
		query = conn.execute("select * from tracks where TrackId =%d " %int(track_id))
		result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
		return jsonify(result)

	def delete(self, track_id):
		conn = db_connect.connect()
		query = conn.execute("delete from tracks where TrackId =%d " %int(track_id))
		return {'status':'success'}


class Employee(Resource):
	def get(self, employee_id):
		conn = db_connect.connect()
		query = conn.execute("select * from employees where EmployeeId =%d " %int(employee_id))
		result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
		return jsonify(result)

	def delete(self, employee_id):
		conn = db_connect.connect()
		query = conn.execute("delete from employees where EmployeeId=%d" %int(employee_id))
		return {'status':'success'}

api.add_resource(Employees, '/employees')
api.add_resource(Tracks, '/tracks')
api.add_resource(Track, '/tracks/<track_id>')
api.add_resource(Employee, '/employees/<employee_id>')

if __name__ == '__main__':
	app.run(port=5002)