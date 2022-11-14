from flask import Flask,request,render_template,redirect,flash
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app=Flask(__name__)
app.config["SECRET_KEY"] = "test1234"
debug=DebugToolbarExtension(app)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"]= False

responses=[]
all_questions = list(surveys.satisfaction_survey.questions)
questions_str = [str(x) for x in all_questions]


@app.route("/")
def home():
    title = surveys.satisfaction_survey.title
    instructions = surveys.satisfaction_survey.instructions 
    return render_template("home.html",title=title,instructions=instructions)
    
@app.route("/questions/<id>")
def ask_question(id):
    q=questions_str[int(id)]
    return render_template("question.html",id=id,q=q)

@app.route("/answer",methods=["POST"])
def add_movie():
    answer = request.form["survey"]
    responses.append(answer)
    next = len(responses) +1
    if next == len(questions_str):
        return redirect("/end")
    else:
        return redirect(f"/questions/{next}")

@app.route("/end")
def end():
    responses.clear()
    return render_template("thanks.html")