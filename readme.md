# To get the server running for the back end and test database routes:

- Navigate into database directory with "cd directory"

- Enter "pipenv shell"

- Run "pipenv install" and then "pipenv update" to ensure all dependencies are installed and the latest versions are implemented

- Enter python repl ">>>"

- Type "from quiz_maker import db", then on the next line "db.create_all()"

- Exit repl with Ctrl/Cmd Z

- Run with "python quiz_maker.py"

## ROUTES

- '/add-quiz'
- '/all-quizzes'
- '/edit-quiz/<id>'
- '/delete-quiz/<id>'

- '/add-question'
- '/all-questions'
- '/edit-question/<id>'
- '/delete-question/<id>'
