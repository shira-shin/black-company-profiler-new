import pytest
from server.services.scoring import compute_score, rank_from_score

@pytest.fixture
def sample_official():
    return {
        "GET_STATS_DATA": {
            "STATISTICAL_DATA": {
                "RESULTS_OVER_TIME": {
                    "TIME_PERIOD": [
                        {"@timeCode": "2020", "C1": "100", "C2": "0.10", "C3": "0.8"},
                        {"@timeCode": "2021", "C1": "150", "C2": "0.15", "C3": "1.0"},
                    ]
                }
            }
        }
    }

def test_compute_score_default(sample_official):
    total, breakdown = compute_score(sample_official, 'default')
    # growth: (150-100)/100*100 = 50% -> normalize to (50-(-50))/(100)*100 = 100
    assert breakdown['growth'] == 100.0
    # profit: 15% -> 15 -> normalize (15-0)/(30)*100 = 50
    assert breakdown['profit'] == 50.0
    # info: 1.0 -> 100 -> normalize (100-0)/100*100 = 100
    assert breakdown['info'] == 100.0
    # total = 100*0.4 + 50*0.4 + 100*0.2 = 40 + 20 + 20 = 80.0
    assert total == 80.0
    assert rank_from_score(total) == 'S'
