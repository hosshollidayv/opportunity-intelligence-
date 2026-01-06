import pytest
from opportunity_intel.models import Opportunity
from opportunity_intel.pack import create_opportunity_pack

def test_opportunity_creation():
    opportunity = Opportunity("Test Opportunity", "This is a test.", 5000)
    assert opportunity.title == "Test Opportunity"
    assert opportunity.value == 5000

def test_create_opportunity_pack(mocker):
    mocker.patch('opportunity_intel.signals.fetch_signal', return_value=[{"title": "Test Opportunity", "description": "Test Description", "value": 5000}])
    opportunities = create_opportunity_pack("http://fakeurl.com")
    assert len(opportunities) == 1
    assert opportunities[0].title == "Test Opportunity"
