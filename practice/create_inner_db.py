from flask import Flask , jsonify
from flask_restful import Api , Resource , abort , reqparse , fields ,marshal_with
from flask_sqlalchemy import SQLAlchemy 

app=Flask(__name__)
api=Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db=SQLAlchemy(app)

video_args=reqparse.RequestParser()
video_args.add_argument('name' , type= str , help="enter the name" , required=True )
video_args.add_argument('views' , type = int , help="ente view count" , required=True)
video_args.add_argument('likes' , type=int ,help = "enter likes count" , required = True)


class Video_model(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(100) , nullable = False)
    views = db.Column(db.Integer , nullable = True)
    likes = db.Column(db.Integer , nullable = True)

    def __repr__(self):
        return f"videos(name={self.name} , views = {self.views} , likes = {self.likes})"

resource_fields={
    'id' :fields.Integer,
    'name' : fields.String,
    'viwes' : fields.Integer,
    'likes' : fields.Integer

}
    
class video(Resource):
    @marshal_with(resource_fields)
    def get(self,video_id):
        result=Video_model.query.get(id=video_id)
        return result
    
    def put(self,video_id):
        args=video_args.parse_args()
        result=

api.add_resource(video , "/video/<int:video_id>")

if __name__=='__main__':
    app.run(debug=True)