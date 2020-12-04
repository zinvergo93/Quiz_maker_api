# To get the server running for the back end and test database routes:

- Navigate into database directory with "cd directory"

- Enter "pipenv shell"

- Run "pipenv install" and then "pipenv update" to ensure all dependencies are installed and the latest versions are implemented

- Enter python repl ">>>"

- Type "from quiz_maker import db", then on the next line "db.create_all()"

- Exit repl with Ctrl/Cmd Z

- Run with "python quiz_maker.py"

- Heroku URL: https://bottega-quiz-maker-api.herokuapp.com/

## ROUTES

- '/add-quiz'
- '/all-quizzes'
- '/edit-quiz/<id>' methods= PUT
- '/delete-quiz/<id>'

- '/add-question'
- '/all-questions'
- '/edit-question/<id>' methods= PUT
- '/delete-question/<id>'

'/add-quiz'
methods= POST
{
"title" = "title"
}

'/add-question'
methods = POST
{
"quiz_id" = "quiz_id"
"question" = "question"
"answer_a" = "answer_a"
"answer_b" = "answer_b"
"answer_c" = "answer_c"
"answer_d" = "answer_d"
"correct_answer" = "correct_answer" \*\*SINGLE DIGIT EXPECTED i.e. "a", "b", "c", "d"
}
