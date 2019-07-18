import pytest


@pytest.fixture
def expected_defaults():
    return {
        "version": 2,
        "name": "<Unnamed Scenario>",
        "scenario": {"serial": {"runner": None, "config": "salami"}},
        "settings": {
            "gas_price": "fast",
            "timeout": 200,
            "notify": None,
            "chain": "any",
            "services": {},
        },
        "token": {"address": None, "block": 0, "reuse": False, "symbol": str(), "decimals": 0},
        "nodes": {
            "list": [],
            "count": 1,
            "commands": {},
            "default_options": {},
            "node_options": {},
            "raiden_version": "LATEST",
        },
    }


@pytest.fixture
def minimal_yaml_dict():
    return {
        "scenario": {"serial": {"runner": None, "config": "salami"}},
        "settings": {},
        "token": {},
        "nodes": {"list": [], "count": 1},
    }
