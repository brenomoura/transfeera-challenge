import pytest

from receivers.tests.helpers import (
    new_receiver_entity,
    new_receiver_model,
    new_base_model,
)


@pytest.fixture
def receiver():
    return new_receiver_entity()


@pytest.fixture
def receiver_model():
    return new_receiver_model()


@pytest.fixture
def base_receiver():
    return new_base_model()
