from flask import Flask, render_template, request


app=Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
# Default value of methods as get in all the situation of root route("/")
# 

@app.route("/signup", methods=["POST"])
def signup():
    userID=request.form.get("userID1")
    userPass=request.form.get("userPass")
        
    adminMail="qwer@qwer.com"
    adminPass="12341234"
        
    # 만약 가입한 회원이 admin일 경우 "관리자님 환영합니다."
    # 아닐경우,
    # 만약 아이디만 맞는 경우 : "관리자님 비번이 틀렸어요, 좀만 더 생각해보세요.
    # 아이디도 틀릴 경우: "꺼지셈".
    
    if userID==adminMail and userPass==adminPass:
        s="관리자님 환영합니다."
    elif userID==adminMail:
        s="관리자님 좀 더 생각 좀."
    else:
        s="꺼지세용."
        
    print(userID,userPass)
    return render_template("signup.html",mail=s)
### password and Id is credential!!! => post
