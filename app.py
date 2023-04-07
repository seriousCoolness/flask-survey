from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Survey, Question, satisfaction_survey

app = Flask(__name__)

# the toolbar is only enabled in debug mode:
app.debug = True
app.config['SECRET_KEY'] = 'coolcode' # set a 'SECRET_KEY' to enable the Flask session cookies

toolbar = DebugToolbarExtension(app)

responses = []


@app.route('/')
def home_page():

    survey = satisfaction_survey
    return render_template('home.html', title=survey.title, instructions=survey.instructions)

@app.route('/begin', methods=['POST'])
def begin_questions():

    session['responses'] = []
    return redirect("/questions/0")

@app.route('/questions/<int:number>')
def question_form(number):
    
    if number != len(session['responses']):
        flash("Please do not attempt to access questions out of order.")
        return redirect(f"/questions/{len(session['responses'])}")

    survey = satisfaction_survey
    if number >= len(survey.questions):
        flash("Thank you for completing the survey!")
        return redirect('/')
    else:
        return render_template('question.html', number=number, question=survey.questions[number].question, choices=survey.questions[number].choices, allow_text=survey.questions[number].allow_text)

@app.route('/answer', methods=["POST"])
def submit_answer():

    answer = request.form.get("answer")
    
    if not answer:

        flash("Must provide valid answer!")
        return redirect(f"/questions/{len(session['responses'])}")
    else:

        session['responses'].append(answer)
        
        flash(f"{session['responses']}")
        return redirect(f"/questions/{len(session['responses'])}")
