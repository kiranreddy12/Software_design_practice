from flask import Flask
from flask_restful import Api,Resource
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
api=Api(app)
class Helloworld(Resource):
    def get(self,n):
        return {"name":n ,
                "age":len(n)*2+4}

    def marry(self,n=0):
        if int(n) <= 21:
            return "not eligible"
        elif 21 < int(n) <= 45:
            return "eligible"
        else:
            return "please marry in another life"
api.add_resource(Helloworld,"/Helloworld/<string:n>")
@app.route("/marry/<string:n>")
def marry(n=0):
    if int(n)<=21:
        return "not eligible"
    elif 21<int(n)<=45:
        return "eligible"
    else:
        return "please marry in another life"
if __name__=="__main__":
     app.run(debug=True)
