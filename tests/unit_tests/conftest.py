import pytest
import server
from flask import template_rendered


def clubs():
    return [
    {
        "name":"Test Club One",
        "email":"one@testclub.com",
        "points":"13"
    },
    {
        "name":"Test Club Two",
        "email": "two@testclub.com",
        "points":"4"
    },
    {   "name":"Test Club Three",
        "email": "three@testclub.com",
        "points":"12"
    }
]

def competitions():
    return [
        {
            "name": "Test Competition One",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Test Competition Two",
            "date": "2023-10-22 13:30:00",
            "numberOfPlaces": "13"
        },
        {
            "name": "Test Competition Three",
            "date": "2023-09-12 19:30:00",
            "numberOfPlaces": "10"
        }
    ]

@pytest.fixture
def app(mocker):
    mocker.patch.object(server, "clubs", clubs())
    mocker.patch.object(server, "competitions", competitions())
    return server.create_app({"TESTING": True})

@pytest.fixture
def client(app):
    with app.test_client() as client:
        return client

@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)