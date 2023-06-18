import sqlite3

DB_NAME = "quiz.db"


class Answer:
    def __init__(self, text, id):
        self.id = id
        self.text = text


class Question:
    def __init__(self, id, quiz_id, text, answers, correct_id):
        self.id = id
        self.quiz_id = quiz_id
        self.text = text
        self.answers = answers
        self.correct_id = correct_id


class Quiz:
    def __init__(self, id, name, questions):
        self.id = id
        self.name = name
        self.questions = questions


premade_questions = [
    Question(
        id=1,
        quiz_id=1,
        text="question 1",
        correct_id=1,
        answers=[
            Answer(text="answer 1.1", id=1),
            Answer(text="answer 1.2", id=2),
            Answer(text="answer 1.3", id=3),
            Answer(text="answer 1.4", id=4),
        ],
    ),
    Question(
        id=2,
        quiz_id=1,
        text="question 2",
        correct_id=2,
        answers=[
            Answer(text="answer 2.1", id=1),
            Answer(text="answer 2.2", id=2),
            Answer(text="answer 2.3", id=3),
            Answer(text="answer 2.4", id=4),
        ],
    ),
    Question(
        id=3,
        quiz_id=1,
        text="question 3",
        correct_id=3,
        answers=[
            Answer(text="answer 3.1", id=1),
            Answer(text="answer 3.2", id=2),
            Answer(text="answer 3.3", id=3),
            Answer(text="answer 3.4", id=4),
        ],
    ),
]


quiz = Quiz(id=1, name="The very first quiz!", questions=premade_questions)


def get_quizes():
    conn = sqlite3.connect(DB_NAME)
    quizes = []
    cursor = conn.execute("SELECT ID, NAME from QUIZ ORDER BY ID")
    for row in cursor:
        quizes.append(
            Quiz(id=row[0], name=row[1], questions=get_questions(conn, row[0]))
        )

    conn.close()

    return quizes


def get_quiz(quiz_id):
    conn = sqlite3.connect(DB_NAME)

    quiz_name = ""

    cursor = conn.execute("SELECT ID, NAME from QUIZ WHERE ID=%s" % quiz_id)
    for row in cursor:
        quiz_name = row[1]

    questions = get_questions(conn, quiz_id)

    conn.close()

    return Quiz(id=quiz_id, name=quiz_name, questions=questions)


def get_questions(conn, quiz_id):
    questions = []
    cursor = conn.execute(
        "SELECT ID, TEXT, CORRECT_ANSWER_ID FROM QUESTION WHERE QUIZ_ID=%s" % quiz_id
    )
    for row in cursor:
        questions.append(
            Question(
                id=row[0],
                quiz_id=quiz_id,
                text=row[1],
                correct_id=row[2],
                answers=get_answers(conn, row[0]),
            )
        )

    return questions


def get_answers(conn, question_id):
    answers = []
    cursor = conn.execute(
        "SELECT ID, TEXT FROM ANSWER WHERE QUESTION_ID=%s" % question_id
    )

    for row in cursor:
        answers.append(Answer(id=row[0], text=row[1]))

    return answers


def add_quiz(name):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("INSERT INTO QUIZ (NAME) VALUES ('%s')" % name)
    conn.commit()
    conn.close()


def delete_quiz(quiz_id):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("DELETE FROM QUIZ WHERE ID = %s" % quiz_id)
    conn.commit()
    conn.close()


def update_quiz(quiz_id, quiz_name):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("UPDATE QUIZ SET NAME='%s' WHERE ID = %s" % (quiz_name, quiz_id))
    conn.commit()
    conn.close()

def add_question(text, quiz_id, ca_id):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("INSERT INTO QUESTION (TEXT, QUIZ_ID, CORRECT_ANSWER_ID) VALUES ('%s', '%s', '%s')" % (text, quiz_id, ca_id))
    conn.commit()
    conn.close()


def delete_question(question_id):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("DELETE FROM QUESTION WHERE ID = %s" % question_id)
    conn.commit()
    conn.close()

def update_question(question_id, text):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("UPDATE QUESTION SET TEXT='%s' WHERE ID = %s" % (text, question_id))
    conn.commit()
    conn.close()