from flask import Flask, render_template, request, redirect, url_for, flash
from surveys import satisfaction_survey

responses = []
question_number = 0
app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"


# Route for the root page
@app.route('/')
def index():
  survey_title = satisfaction_survey.title
  instructions = satisfaction_survey.instructions
  return render_template('index.html', title=survey_title, instructions=instructions)

# Route for handling questions

@app.route('/questions/<int:question_number>', methods=['GET', 'POST'])
def question(question_number):
    if responses is None:
      return redirect("/")

    if len(responses) != question_number:
      # Trying to access questions out of order
      flash(f"Invalid question id: {question_number}.")
      
      return redirect(f"/questions/{len(responses)}")

    if request.method == 'POST':
      # Retrieve the answer from the form
      answer = request.form.get('answer')

      # Append the answer to the responses list
      responses.append(answer)

      # Redirect to the next question
      return redirect(url_for('question', question_number=question_number + 1))

    # Redirect to the result page when all questions have been answered
    if len(responses) == len(satisfaction_survey.questions):
      @app.route('/result')
      def result():
        responses_str = ', '.join(responses)  # Convert the responses list to a string
        return render_template('result.html', responses=responses_str, title=satisfaction_survey.title)

    # If it's a GET request, render the question template with the current question
    question_text = satisfaction_survey.questions[question_number].question
    return render_template('question.html', question_number=question_number, question_text=question_text)
  
  # Redirect to the result page when all questions have been answered
    if len(responses) == len(satisfaction_survey.questions):
      @app.route('/result')
      def result():
        responses_str = ', '.join(responses)  # Convert the responses list to a string
        return render_template('result.html', responses=responses_str, title=satisfaction_survey.title)
    

  # @app.route('/result')
  #  def result():
  #   responses_str = ', '.join(responses)  # Convert the responses list to a string
  #   return render_template('result.html', responses=responses_str, title=satisfaction_survey.title)


if __name__ == '__main__':
  app.run()

