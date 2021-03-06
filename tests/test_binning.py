"""
OptimalBinning testing.
"""

# Guillermo Navas-Palencia <g.navas.palencia@gmail.com>
# Copyright (C) 2020

import pandas as pd

from pytest import approx, raises

from optbinning import OptimalBinning
from sklearn.datasets import load_breast_cancer
from sklearn.exceptions import NotFittedError


data = load_breast_cancer()
df = pd.DataFrame(data.data, columns=data.feature_names)

variable = "mean radius"
x = df[variable].values
y = data.target


def test_params():
    with raises(TypeError):
        optb = OptimalBinning(name=1)
        optb.fit(x, y)

    with raises(ValueError):
        optb = OptimalBinning(dtype="nominal")
        optb.fit(x, y)

    with raises(ValueError):
        optb = OptimalBinning(prebinning_method="new_method")
        optb.fit(x, y)

    with raises(ValueError):
        optb = OptimalBinning(solver="new_solver")
        optb.fit(x, y)

    with raises(ValueError):
        optb = OptimalBinning(max_n_prebins=-2)
        optb.fit(x, y)

    with raises(ValueError):
        optb = OptimalBinning(min_prebin_size=0.6)
        optb.fit(x, y)

    with raises(ValueError):
        optb = OptimalBinning(min_n_bins=-2)
        optb.fit(x, y)

    with raises(ValueError):
        optb = OptimalBinning(max_n_bins=-2.2)
        optb.fit(x, y)

    with raises(ValueError):
        optb = OptimalBinning(min_n_bins=3, max_n_bins=2)
        optb.fit(x, y)

    with raises(ValueError):
        optb = OptimalBinning(min_bin_size=0.6)
        optb.fit(x, y)

    with raises(ValueError):
        optb = OptimalBinning(max_bin_size=-0.6)
        optb.fit(x, y)

    with raises(ValueError):
        optb = OptimalBinning(min_bin_size=0.5, max_bin_size=0.3)
        optb.fit(x, y)

    with raises(ValueError):
        optb = OptimalBinning(min_bin_n_nonevent=-2)
        optb.fit(x, y)

    with raises(ValueError):
        optb = OptimalBinning(max_bin_n_nonevent=-2)
        optb.fit(x, y)

    with raises(ValueError):
        optb = OptimalBinning(min_bin_n_nonevent=3, max_bin_n_nonevent=2)
        optb.fit(x, y)

    with raises(ValueError):
        optb = OptimalBinning(min_bin_n_event=-2)
        optb.fit(x, y)

    with raises(ValueError):
        optb = OptimalBinning(max_bin_n_event=-2)
        optb.fit(x, y)

    with raises(ValueError):
        optb = OptimalBinning(min_bin_n_event=3, max_bin_n_event=2)
        optb.fit(x, y)

    with raises(ValueError):
        optb = OptimalBinning(monotonic_trend="new_trend")
        optb.fit(x, y)

    with raises(ValueError):
        optb = OptimalBinning(min_event_rate_diff=1.1)
        optb.fit(x, y)

    with raises(ValueError):
        optb = OptimalBinning(max_pvalue=1.1)
        optb.fit(x, y)

    with raises(ValueError):
        optb = OptimalBinning(max_pvalue_policy="new_policy")
        optb.fit(x, y)

    with raises(TypeError):
        optb = OptimalBinning(class_weight=[0, 1])
        optb.fit(x, y)

    with raises(ValueError):
        optb = OptimalBinning(class_weight="unbalanced")
        optb.fit(x, y)

    with raises(ValueError):
        optb = OptimalBinning(cat_cutoff=-0.2)
        optb.fit(x, y)

    with raises(TypeError):
        optb = OptimalBinning(user_splits={"a": [1, 2]})
        optb.fit(x, y)

    with raises(TypeError):
        optb = OptimalBinning(special_codes={1, 2, 3})
        optb.fit(x, y)

    with raises(ValueError):
        optb = OptimalBinning(split_digits=9)
        optb.fit(x, y)

    with raises(ValueError):
        optb = OptimalBinning(mip_solver="new_solver")
        optb.fit(x, y)

    with raises(ValueError):
        optb = OptimalBinning(time_limit=-2)
        optb.fit(x, y)

    with raises(TypeError):
        optb = OptimalBinning(verbose=1)
        optb.fit(x, y)


def test_numerical_default():
    optb = OptimalBinning()
    optb.fit(x, y)

    assert optb.status == "OPTIMAL"
    assert optb.splits == approx([11.42500019, 12.32999992, 13.09499979,
                                  13.70499992, 15.04500008, 16.92500019],
                                 rel=1e-6)


def test_numerical_default_solvers():
    optb_mip_cbc = OptimalBinning(solver="mip", mip_solver="cbc")
    optb_mip_cbc.fit(x, y)

    optb_mip_bop = OptimalBinning(solver="mip", mip_solver="bop")
    optb_mip_bop.fit(x, y)

    optb_cp = OptimalBinning(solver="cp")
    optb_cp.fit(x, y)

    for optb in [optb_mip_bop, optb_mip_cbc, optb_cp]:
        assert optb.status == "OPTIMAL"
        assert optb.splits == approx([11.42500019, 12.32999992, 13.09499979,
                                      13.70499992, 15.04500008, 16.92500019],
                                     rel=1e-6)


def test_numerical_default_transform():
    optb = OptimalBinning()
    with raises(NotFittedError):
        x_transform = optb.transform(x)

    optb.fit(x, y)

    x_transform = optb.transform([12, 14, 15, 21], metric="woe")
    assert x_transform == approx([-2.71097154, -0.15397917, -0.15397917,
                                  5.28332344], rel=1e-6)


def test_numerical_default_fit_transform():
    optb = OptimalBinning()

    x_transform = optb.fit_transform(x, y, metric="woe")
    assert x_transform[:5] == approx([5.28332344, 5.28332344, 5.28332344,
                                      -3.12517033, 5.28332344], rel=1e-6)


def test_information():
    optb = OptimalBinning(solver="cp")

    with raises(NotFittedError):
        optb.information()

    optb.fit(x, y)

    with raises(ValueError):
        optb.information(print_level=-1)

    optb.information(print_level=0)
    optb.information(print_level=1)
    optb.information(print_level=2)

    optb = OptimalBinning(solver="mip")
    optb.fit(x, y)
    optb.information(print_level=2)


def test_verbose():
    optb = OptimalBinning(verbose=True)
    optb.fit(x, y)

    assert optb.status == "OPTIMAL"
