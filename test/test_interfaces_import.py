# Interface import smoke test (task 2.3/A06).
#
# Imports every generated Python interface and instantiates each part, so a
# broken IDL definition or a failed rosidl Python generation turns the
# `build / build` check red. Runs via ament_cmake_pytest under colcon test;
# the CI workflow sources install/setup.bash first, which puts this package's
# installed Python bindings on PYTHONPATH.
import pytest

ACTIONS = ["ManageEpisode", "RecordEpisode", "RunPolicy"]
SERVICES = ["StartHILEpisode", "StartRecording"]


@pytest.mark.parametrize("name", ACTIONS)
def test_action_imports_and_instantiates(name):
    module = __import__("rosetta_interfaces.action", fromlist=[name])
    action = getattr(module, name)
    for part in ("Goal", "Result", "Feedback"):
        instance = getattr(action, part)()
        assert instance is not None


@pytest.mark.parametrize("name", SERVICES)
def test_service_imports_and_instantiates(name):
    module = __import__("rosetta_interfaces.srv", fromlist=[name])
    service = getattr(module, name)
    for part in ("Request", "Response"):
        instance = getattr(service, part)()
        assert instance is not None


def test_action_field_contract():
    from rosetta_interfaces.action import RunPolicy

    goal = RunPolicy.Goal()
    assert goal.prompt == ""
    assert goal.policy_name == ""
    fields = RunPolicy.Goal.get_fields_and_field_types()
    assert fields["pretrained_name_or_path"] == "string"
    assert fields["policy_type"] == "string"
