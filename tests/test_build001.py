import hashlib
from pathlib import Path
import numpy as np
import pytest
from evaluation_lab.generator import generate_case, canonical_csv_bytes, export_all
from evaluation_lab.reference import references, decompose, summarize_pandas
from evaluation_lab.scenarios import SCENARIOS, SEGMENTS, PERIODS

EXPECTED = [
    (14.5, 16.0, 1.5, 1.5, 0.0),
    (14.5, 15.8, 1.3, 0.0, 1.3),
    (14.5, 17.1, 2.6, 1.4, 1.2),
    (14.5, 14.5, 0.0, 0.0, 0.0),
]
KEYS = ["baseline_rate_pct","after_rate_pct","total_change_pp","mix_pp","within_pp"]

@pytest.mark.parametrize("i",range(4))
def test_exact_expected_and_sqlite(i):
    df=generate_case(SCENARIOS[i])
    assert len(df)==40000
    assert set(df.columns)=={"trial_id","customer_id","period","segment","converted"}
    assert df.trial_id.is_unique and df.customer_id.is_unique
    assert set(df.converted.unique())=={0,1}
    assert df.groupby("period").size().to_dict()=={"2026-08":20000,"2026-09":20000}
    pand,sql=references(df,engine="sqlite")
    for key,expected in zip(KEYS,EXPECTED[i]):
        assert pand[key]==pytest.approx(expected,abs=1e-10)
        assert sql[key]==pytest.approx(expected,abs=1e-10)
    assert pand["mix_pp"]+pand["within_pp"]==pytest.approx(pand["total_change_pp"],abs=1e-10)

@pytest.mark.parametrize("i",range(4))
def test_duckdb_reference(i):
    pytest.importorskip("duckdb")
    pand,duck=references(generate_case(SCENARIOS[i]),engine="duckdb")
    assert all(pand[k]==pytest.approx(duck[k],abs=1e-10) for k in KEYS)

def test_reproducible_and_seed_changes():
    c=SCENARIOS[2]
    a=canonical_csv_bytes(generate_case(c,seed=17))
    b=canonical_csv_bytes(generate_case(c,seed=17))
    d=canonical_csv_bytes(generate_case(c,seed=18))
    assert hashlib.sha256(a).hexdigest()==hashlib.sha256(b).hexdigest()
    assert a!=d

def test_private_metadata_not_in_public_csv(tmp_path):
    manifest=export_all(tmp_path)
    for case in SCENARIOS:
        data=(tmp_path/"public"/f"{case.identifier}.csv").read_bytes()
        assert hashlib.sha256(data).hexdigest()==manifest["cases"][case.identifier]["sha256"]
        assert b"pure_mix" not in data and b"ground_truth" not in data
        assert b"scenario" not in data

def test_sampled_references_from_realized_data():
    for c in SCENARIOS:
        df=generate_case(c,mode="sampled",seed=33)
        pandas,sql=references(df,engine="sqlite")
        for k in KEYS:
            assert pandas[k]==pytest.approx(sql[k],abs=1e-10)
        assert pandas["mix_pp"]+pandas["within_pp"]==pytest.approx(pandas["total_change_pp"],abs=1e-10)

def test_invalid_mode_and_too_small_denominator():
    with pytest.raises(ValueError):generate_case(SCENARIOS[0],mode="bogus")
    with pytest.raises(ValueError):generate_case(SCENARIOS[0],n_per_period=0)
