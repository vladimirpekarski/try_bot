# -*- coding: utf-8 -*-

import ast
import urllib


from constants import JENKINS, PYTHON_API, LAST_COMPLETED_BUILD


def get_job_statuses(job):
    job = PYTHON_API.format(job)
    return ast.literal_eval(urllib.urlopen('{}/{}'.format(JENKINS, job)).read())


def get_last_build(job):
    job_statuses = get_job_statuses(job)
    return job_statuses[LAST_COMPLETED_BUILD]['number']


def get_job_status(job_id):
    job = 'test_job'
    url = '{}/{}/{}'.format(JENKINS, job, job_id)
    url = PYTHON_API.format(url)

    return ast.literal_eval(
        urllib.urlopen(url).read())["result"]


def get_last_job_status():
    last_id = get_last_build('test_job')
    return last_id, get_job_status(last_id)
