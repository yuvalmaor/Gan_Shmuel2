from flask import Flask,request,jsonify
from swagger_ui import api_doc

app=Flask(__name__)

api_doc(app, config_path='./swagger/openapi.json', url_prefix='/api/doc', title='API doc')

@app.get("/health")
def health():
    #docker compose ps --format "{{.Service}} {{.State}}"
    temp={"sevices":{"Weight": {"api":"running","database":"running"},
                     "Billing":{"api":"running","database":"running"}}}
    return jsonify(temp)

@app.post("/trigger")
def trigger():
    data=request.get_json()
    print(data)
    return "ok"

if __name__=="__main__":
    app.run()