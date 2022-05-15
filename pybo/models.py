from django.db import models

# Create your models here.
class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
"""
CREATE TABLE "pybo_question" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
"subject" varchar(200) NOT NULL, "content" text NOT NULL, "create_date" datetime NOT NULL);
"""
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
"""
CREATE TABLE "pybo_answer" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,"content" text NOT NULL, "create_date"
datetime NOT NULL, "question_id" integer NOT NULL REFERENCES "pybo question" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "pybo_answer_question_id_e174c39f" ON "pybo_answer" ("question_id");
"""