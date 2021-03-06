import pytest
import os
import sys
from faker import Faker
import random
import json
tests_folder_path = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.append(tests_folder_path)
from courses_crud import create_app # noqa


@pytest.fixture(scope='function')
def client(request):
    app = create_app(config_name="testing")
    app.config['test_data'] = generate_test_data()
    with app.test_client() as client:
        yield client

        @app.teardown_appcontext
        def delete_test_db_file(exception=None):
            test_db_file_path = app.config['DATABASE_FILE_PATH']
            os.unlink(test_db_file_path)


def generate_test_data():
    '''
    return Faker's test course data
    '''
    fake = Faker()
    fake_course = fake.profile()
    fake_course['title'] = fake.paragraph(nb_sentences=1)
    fake_course['lectures_count'] = random.randrange(1, 1000)
    fake_course['start_date'] = fake.date()
    fake_course['end_date'] = fake.date()
    return fake_course


def add_course(client, times=1):
    for count in range(times):
        test_user_data = generate_test_data()
        response = client.post(
            "/api/1.0/courses",
            data=json.dumps(
                {
                    'name': test_user_data['title'],
                    'lectures_count': test_user_data['lectures_count'],
                    'start_date': test_user_data['start_date'],
                    'end_date': test_user_data['end_date'],
                }
            ),
            content_type="application/json",
        )
        response = json.loads(response.data)
