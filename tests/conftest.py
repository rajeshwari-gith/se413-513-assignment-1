import os
import tempfile

import pytest


@pytest.fixture
def valid_student():
    return {"current_credits": 12, "course_credits": 3, "prerequisite_met": True}


@pytest.fixture
def registration_log():
    fd, path = tempfile.mkstemp(suffix=".txt")
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)
