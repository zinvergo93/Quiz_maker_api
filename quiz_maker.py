from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from flask_cors import CORS
from flask.json import JSONEncoder
from flask_heroku import Heroku
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()
app = Flask(__name__)
CORS(app)
heroku = Heroku(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
#     os.path.join(basedir, 'quiz_maker.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json_encoder = JSONEncoder
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    questions = relationship('Question', backref="Quiz", lazy=True)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question = db.Column(db.String(200), unique=False)
    answer_a = db.Column(db.String(100), unique=False)
    answer_b = db.Column(db.String(100), unique=False)
    answer_c = db.Column(db.String(100), unique=False)
    answer_d = db.Column(db.String(100), unique=False)
    correct_answer = db.Column(db.String(5), unique=False)


class QuestionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'quiz_id', 'question', 'answer_a',
                  'answer_b', 'answer_c', 'answer_d', 'correct_answer')


class QuizSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    questions = fields.Nested(QuestionSchema, many=True)


quiz_schema = QuizSchema()
quizzes_schema = QuizSchema(many=True)
question_schema = QuestionSchema()
questions_schema = QuestionSchema(many=True)

# Quiz Routes


@app.route('/add-quiz', methods=["POST"])
def add_quiz():
    title = request.json["title"]

    new_quiz = Quiz(title=title)

    db.session.add(new_quiz)
    db.session.commit()

    quiz = Quiz.query.get(new_quiz.id)
    return quiz_schema.jsonify(quiz)


@app.route("/all-quizzes", methods=["GET"])
def get_quizzes():
    all_quizzes = Quiz.query.all()
    result = quizzes_schema.dump(all_quizzes)
    return jsonify(result)


@app.route("/edit-quiz/<id>", methods=["PUT"])
def quiz_update(id):
    quiz = Quiz.query.get(id)
    title = request.json["title"]

    quiz.title = title

    db.session.commit()
    return jsonify(message="Quiz edit successful")


@app.route("/delete-quiz/<id>", methods=["DELETE"])
def quiz_delete(id):
    quiz = Quiz.query.get(id)
    db.session.delete(quiz)
    db.session.commit()

    return jsonify(message="Successful quiz delete")

# Question Routes


@app.route("/add-question", methods=["POST"])
def add_question():
    quiz_id = request.json["quiz_id"]
    question = request.json["question"]
    answer_a = request.json["answer_a"]
    answer_b = request.json["answer_b"]
    answer_c = request.json["answer_c"]
    answer_d = request.json["answer_d"]
    correct_answer = request.json["correct_answer"]

    new_question = Question(
        quiz_id=quiz_id,
        question=question,
        answer_a=answer_a,
        answer_b=answer_b,
        answer_c=answer_c,
        answer_d=answer_d,
        correct_answer=correct_answer
    )

    db.session.add(new_question)
    db.session.commit()

    question = Question.query.get(new_question.id)

    return jsonify(message="Successful question addition")


@app.route("/all-questions", methods=["GET"])
def get_questions_by_quizid():
    all_questions = Question.query.all()
    result = questions_schema.dump(all_questions)
    return jsonify(result)


@app.route("/edit-question/<id>", methods=["PUT"])
def edit_question(id):
    this_question = Question.query.get(id)
    quiz_id = request.json["quiz_id"]
    question = request.json["question"]
    answer_a = request.json["answer_a"]
    answer_b = request.json["answer_b"]
    answer_c = request.json["answer_c"]
    answer_d = request.json["answer_d"]
    correct_answer = request.json["correct_answer"]
    this_question.quiz_id = quiz_id
    this_question.question = question
    this_question.answer_a = answer_a
    this_question.answer_b = answer_b
    this_question.answer_c = answer_c
    this_question.answer_d = answer_d
    this_question.correct_answer = correct_answer
    db.session.commit()

    return jsonify(message="Successful question edit")


@app.route("/delete-question/<id>", methods=["DELETE"])
def delete_question(id):
    this_question = Question.query.get(id)
    db.session.delete(this_question)
    db.session.commit()

    return jsonify(message="Successful question delete")


if __name__ == '__main__':
    app.debug = True
    app.run()
