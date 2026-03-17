from flask import *
import datetime

from data import db_session
from data.jobs import Jobs

blueprint = Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('id', 'job', 'work_size', 'team_leader'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_jobs(jobs_id):
    db_sess = db_session.create_session()
    job = db_sess.get(Jobs, jobs_id)
    if not job:
        return make_response(jsonify({'error': 'Job not found'}), 404)
    return jsonify(
        {
            'jobs': job.to_dict(max_serilization_depth=0)
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['job', 'work_size', 'team_leader', 'start_date']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    data = request.json
    try:
        data['start_date'] = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d')
        if data.get('end_date'):
            data['end_date'] = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d')
    except ValueError:
        return make_response(jsonify({'error': 'Bad date format, need %Y-%m-%d'}), 400)
    db_sess = db_session.create_session()
    jobs = Jobs(
        job=data['job'],
        work_size=data['work_size'],
        team_leader=data['team_leader'],
        start_date=data['start_date'],
        end_date=data.get(['end_date']),
        collaborators=data.get(['collaborators']),
        is_finished=data.get('is_finished'),
    )
    db_sess.add(jobs)
    db_sess.commit()
    return make_response(jsonify({'id': jobs.id}), 201)