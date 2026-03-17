import requests
from data.db_session import global_init, create_session
from data.jobs import Jobs
import pytest

@pytest.fixture
def create_conn():
    global_init('db/mass_explorer.db')
    sess = create_session()
    yield sess
    sess.close()


def test_get_jobs(create_conn):
    response = requests.get('http://localhost:5000/api/jobs')
    assert response.status_code == 200
    jobs = [item.to_dict(only=('id', 'job', 'work_size', 'team_leader'))
            for item in create_conn.query(Jobs).all()]

    assert response.json() == jobs


def test_get_one_job(create_conn):
    response = requests.get('http://localhost:5000/api/jobs/1')
    assert response.status_code == 200
    job = create_conn.get(Jobs, 1).to_dict(max_serilization_depth=0)
    assert response.json() == {'job': job}


def test_get_wrong_job_id():
    response = requests.get('http://localhost:5000/api/jobs/100000')
    assert response.status_code == 404
    assert response.json() == {'error': 'Job not found'}


def test_get_str_job_id():
    response = requests.get('http://localhost:5000/api/jobs/asd')
    assert response.status_code == 404
    assert response.json() == {'error': 'Not found'}


def test_post_job(create_conn):
    response = requests.get('http://localhost:5000/api/jobs',
                            json={
                                "job": 'task',
                                "work_size": 26,
                                "team_leader": 337,
                                "start_date": '2026-03-13'
                            })
    assert response.status_code == 201
    jid = response.json()['id']
    job = create_conn.get(Jobs, jid)
    assert job.job == "task"


def test_post_empty_job():
    response = requests.post('http://localhost:5000/api/jobs', json={})
    assert response.status_code == 400
    assert response.json() == {'error': 'Empty request'}


def test_post_bad_job():
    response = requests.post('http://localhost:5000/api/jobs', json={'job': 'jhkahfvewkaf'})
    assert response.status_code == 400
    assert response.json() == {'error': 'Bad request'}


def test_post_bad_date_job(create_conn):
    response = requests.get('http://localhost:5000/api/jobs',
                            json={
                                "job": 'task',
                                "work_size": 26,
                                "team_leader": 337,
                                "start_date": '13-03-2026'
                            })
    assert response.status_code == 400
    assert response.json() == {'error': 'Bad date format, need %Y-%m-%d'}

