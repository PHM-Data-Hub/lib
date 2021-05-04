from typer.testing import CliRunner
import pytest
from pytest_mock import MockFixture
from unittest import mock
import requests


# TUTORIAL FROM TYPER
import machine_data_hub
from machine_data_hub.cli import app

MOCK_DATASETS = [
    {
        "id": 1,
        "Rank": 1,
        "Name": "Combined Cycle Power Plant Data Set",
        "Owner": "UC Irvine",
        "URL": "https://archive.ics.uci.edu/ml/machine-learning-databases/00294/CCPP.zip",
        "Short Summary": "The dataset contains 9568 data points collected from a Combined Cycle Power Plant over 6 years (2006-2011), when the power plant was set to work with full load. Features consist of hourly average ambient variables Temperature (T), Ambient Pressure (AP), Relative Humidity (RH) and Exhaust Vacuum (V) to predict the net hourly electrical energy output (EP) of the plant. A combined cycle power plant (CCPP) is composed of gas turbines (GT), steam turbines (ST) and heat recovery steam generators. In a CCPP, the electricity is generated by gas and steam turbines, which are combined in one cycle, and is transferred from one turbine to another. While the Vacuum is collected from and has effect on the Steam Turbine, he other three of the ambient variables effect the GT performance. For comparability with our baseline studies, and to allow 5x2 fold statistical tests be carried out, we provide the data shuffled five times. For each shuffling 2-fold CV is carried out and the resulting 10 measurements are used for statistical testing.",
        "Sector": "Power",
        "ML Type": "Regression",
        "Labeled": "Yes",
        "Time Series": "No",
        "Simulation (Yes/No)": "N/A",
        "Attributes": 4,
        "Instances": 9568,
        "Downloads": 191037,
        "Likes": 0,
        "File Size": "3.7 MB",
        "img_link": "https://www.miga.org/sites/default/files/2018-06/power-plant-bright-blue-sky.jpg",
        "Datasets": [
            {
                "Name": "Dataset 1",
                "URL": "https://archive.ics.uci.edu/ml/machine-learning-databases/00294/CCPP.zip",
                "Likes": 0,
                "Downloads": 191037,
                "File Size": "3.7 MB"
            }
        ]
    }
]


@pytest.fixture
def mock_requests_get(mocker):
    """Fixture for mocking requests.get."""
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = MOCK_DATASETS
    return mock


@pytest.fixture
def mock_requests_file_get(mocker):
    """Fixture for mocking requests.get."""
    mock = mocker.patch("requests.get")
    mock.return_value.content = b"Example File Content"
    return mock


@pytest.fixture
def mock_get_datasets(mocker):
    """Fixture for mocking get_datasets."""
    mock = mocker.patch("machine_data_hub.cli.get_datasets")
    mock.return_value = MOCK_DATASETS
    return mock


@pytest.fixture
def runner():
    return CliRunner()


# The first parameter to runner.invoke() is a Typer app.
# The second parameter is a list of str, with all the text you would pass in the command line, right as you would pass it:
def test_success_download(runner, mock_get_datasets, mock_requests_file_get):
    print(f"Try the get_datasets() mock: {machine_data_hub.cli.get_datasets('hello')}")
    print(f"Try the request.get mock: {requests.get('hello').json()}")
    result = runner.invoke(app, ["download", 1, 1])
    assert result.exit_code == 0


def test_fail_download(runner, mock_requests_get, mock_requests_file_get):
    # passing in incorrect name
    result = runner.invoke(app, ["download", 9999])
    assert result.exit_code == 0


def test_metadata(runner, mock_requests_get, mock_requests_file_get):
    result = runner.invoke(app, ["metadata", 1])
    assert result.exit_code == 0
    # assert f"Downloading {name} right now!" in result.stdout


def test_suggest(runner):
    print("don't want to test every time")
#    result = runner.invoke(app, ["suggest", "Test", "www.google.com", "Testing summary"])
#    assert result.exit_code == 0


def test_list(runner, mock_requests_get, mock_requests_file_get):
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0