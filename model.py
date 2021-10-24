import pandas as pd
import sqlalchemy
# noinspection PyPackageRequirements
from google.cloud.sql.connector import connector
from sqlalchemy.sql import select
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Student(Base):
    __tablename__ = 'student'
    id = sqlalchemy.Column(sqlalchemy.VARCHAR)
    class_name = sqlalchemy.Column(sqlalchemy.VARCHAR)
    unique_id = sqlalchemy.Column(sqlalchemy.VARCHAR, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.VARCHAR)
    at_risk = sqlalchemy.Column(sqlalchemy.VARCHAR)
    test_when_at_risk = sqlalchemy.Column(sqlalchemy.VARCHAR)
    outperform = sqlalchemy.Column(sqlalchemy.VARCHAR)
    on_track = sqlalchemy.Column(sqlalchemy.VARCHAR)
    pred_vs_perf_latest_diff = sqlalchemy.Column(sqlalchemy.VARCHAR)
    test_since_at_risk = sqlalchemy.Column(sqlalchemy.VARCHAR)


class Scores(Base):
    __tablename__ = 'score'
    id = sqlalchemy.Column(sqlalchemy.VARCHAR, primary_key=True)
    test = sqlalchemy.Column(sqlalchemy.VARCHAR)
    score = sqlalchemy.Column(sqlalchemy.VARCHAR)
    class_name = sqlalchemy.Column(sqlalchemy.VARCHAR)


def init_connection_engine():
    def getconn():
        conn = connector.connect(
            "studious-matrix-329918:us-central1:student-check",
            "pg8000",
            user="postgres",
            password = "postgres123",
            db = "postgres"
        )
        return conn

    engine = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )
    engine.dialect.description_encoding = None
    return engine


class Model:
    student = 'student_table'

    def __init__(self):
        self._engine = init_connection_engine()

    def upload_new_test_scores(self, frame: pd.DataFrame, test_name):
        frame_copy = frame.assign(test=test_name)
        frame_copy.to_sql(
            self.student, self._engine, if_exists='append', index=False
        )

    def query_scores(self, grade=None, ids=None):
        selection = select(Scores)
        if grade is not None:
            selection = selection.where(Scores.class_name == grade)
        if ids is not None:
            if not isinstance(ids, list):
                ids = [ids]
            selection = selection.where(Scores.id.in_(ids))
        return pd.read_sql(selection, self._engine)

    def query_students(self,
                       class_name=None, ids=None, at_risk=None,
                       outperform=None, on_track=None
                       ):

        selection = select(Student)
        if class_name is not None:
            selection = selection.where(Student.class_name == class_name)
        if ids is not None:
            if not isinstance(ids, list):
                ids = [ids]
            selection = selection.where(Student.id.in_(ids))
        if at_risk is not None:
            selection = selection.where(Student.at_risk == at_risk)
        if outperform is not None:
            selection = selection.where(Student.outperform == outperform)
        if on_track is not None:
            selection = selection.where(Student.on_track == on_track)
        return pd.read_sql(selection, self._engine)


def main():
    model = Model()
    scores = model.query_students(class_name='Grade 3, Maths')
    print(scores.shape[0])


if __name__ == '__main__':
    main()
