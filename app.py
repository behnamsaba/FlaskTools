from flask import Flask,request,render_template,redirect,flash,session
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app=Flask(__name__)
app.config["SECRET_KEY"] = "test1234"
debug=DebugToolbarExtension(app)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"]= False

responses=[]
questions_str = [x.question for x in surveys.satisfaction_survey.questions]
all_choices = [x.choices for x in surveys.satisfaction_survey.questions]
# WITH SESSION
@app.route("/second-home")
def start():
    title = surveys.satisfaction_survey.title
    instructions = surveys.satisfaction_survey.instructions 
    return render_template("home-session.html",title=title,instructions=instructions)

@app.route("/session", methods=["POST"])
def set_session():
    session["responses"] = []
    next_page = len(session["responses"])
    return redirect(f"/questions/{next_page + 1}")

@app.route("/")
def home():
    responses.clear()
    title = surveys.satisfaction_survey.title
    instructions = surveys.satisfaction_survey.instructions 
    return render_template("home.html",title=title,instructions=instructions)
    
@app.route("/questions/<id>")
def ask_question(id):
    
    if int(id) > len(responses) +1:
        return redirect(f"/questions/{len(responses) + 1}")
    
    if len(responses) == len(questions_str):
        return redirect("/end")
    
    id = len(responses)#ensure we are in right question
    q=questions_str[int(id)]
    options = all_choices[int(id)]
    print(session["responses"])
    return render_template("question.html",id=id,q=q,options=options)

@app.route("/answer",methods=["POST"])
def add_movie():
    answer = request.form["survey"]
    responses.append(answer)
    ################################################################################## ADD TO SESSION
    responses2 = session["responses"]
    responses2.append(answer)
    session["responses"] = responses2
    ################################################################################### 
    next = len(responses) +1
    if next == len(questions_str) +1:
        return redirect("/end")
    else:
        return redirect(f"/questions/{next}")

@app.route("/end")
def end():
    return render_template("thanks.html")