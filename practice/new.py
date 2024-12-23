from flask import Flask 
from flask_restful import Api, Resource ,reqparse , abort


app=Flask(__name__)
api=Api(app)

video_parser=reqparse.RequestParser()
video_parser.add_argument("likes" , type=int , help="enter no of likes")
video_parser.add_argument("viwes", type=int , help="enter the viwe count")
video_parser.add_argument("dislikes" , type=int , help="enter dislike count")

video={}

def if_id_not_in_videos(video_id):
    if video_id not in video:
        abort(404,message="video not found")

def id_in_videos(video_id):
    if video_id in video:
        abort(409,"video is already exists")


class data(Resource):
    def get(self,video_id):
        print("this is get :")
        if_id_not_in_videos(video_id)
        return video[video_id],201
    
    #def post(self,video_id):
    #    return {"data" : f"this is post data"}

    def put(self,video_id):
        id_in_videos(video_id)
        args=video_parser.parse_args()
        video[video_id]=args
        return video[video_id],201
    
    def delete(self,video_id):
        if_id_not_in_videos(video_id)
        del video[video_id]
        return abort(204,message="deleted")
    
api.add_resource(data,"/data/<int:video_id>")


if __name__=="__main__":
    app.run(debug=True)