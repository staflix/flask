from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, select
import sqlalchemy
from flask import Flask, render_template

app = Flask(__name__)
SqlAlchemyBase = declarative_base()


class User(SqlAlchemyBase):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    surname = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    age = sqlalchemy.Column(sqlalchemy.Integer)
    position = sqlalchemy.Column(sqlalchemy.String)
    speciality = sqlalchemy.Column(sqlalchemy.String)
    address = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)

    def __repr__(self):
        return f"{self.surname}-{self.name}"


class Jobs(SqlAlchemyBase):
    __tablename__ = "jobs"

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    job = sqlalchemy.Column(sqlalchemy.Text)
    work_size = sqlalchemy.Column(sqlalchemy.Integer)
    collaborators = sqlalchemy.Column(sqlalchemy.String)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean)

    def __repr__(self):
        return f'{self.job}-{self.work_size}-{self.collaborators}-{self.is_finished}-{self.team_leader}'


result = []
full_names = []


@app.route("/table")
def table():
    return render_template("index.html", result=result)


engine = create_engine(f'sqlite:///data.db')
SqlAlchemyBase.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

query_jobs = select(Jobs)
data_jobs = session.execute(query_jobs)
team_leaders = [str(x).split("-")[-1] for x in data_jobs.scalars().all()]

query_jobs_other = select(Jobs)
data_jobs_other = session.execute(query_jobs)
other_info = [str(x).split("-")[:4] for x in data_jobs_other.scalars().all()]

for team_leader in team_leaders:
    query = select(User).filter(User.id == int(team_leader))
    data = session.execute(query)
    full_name = ' '.join(str(data.scalars().all()[0]).split("-"))
    full_names.append(full_name)

for i in range(len(team_leaders)):
    if other_info[i][3] is False:
        other_info[i][3] = "Is not finished"
    else:
        other_info[i][3] = "Is finished"
    result.append((other_info[i][0], full_names[i], other_info[i][1], other_info[i][2], other_info[i][3]))

print(result)
session.commit()
session.close()

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
