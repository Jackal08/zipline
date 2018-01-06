#
# Copyright 2018 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from functools import partial

from .metric import (
    BenchmarkReturns,
    CashFlow,
    DailyLedgerField,
    Orders,
    PNL,
    Returns,
    SimpleLedgerField,
    StartOfPeriodLedgerField,
    Transactions,
)
from .tracker import MetricsTracker


__all__ = ['MetricsTracker']


_registered_metrics_sets = {}


def register_metrics_set(name, function=None):
    """Register a new metrics set.

    Parameters
    ----------
    name : str
        The name of the metrics set
    function : callable
        The callable which produces the metrics set.

    Notes
    -----
    This may be used as a decorator if only ``name`` is passed.
    """
    if function is None:
        # allow as decorator with just name.
        return partial(register_metrics_set, name)

    if name in _registered_metrics_sets:
        raise ValueError('metrics set %r is already registered' % name)

    _registered_metrics_sets[name] = function


def get_metrics_set(name):
    """Return an instance of the metrics set registered with the given name.

    Returns
    -------
        A new instance of the metrics set.

    Raises
    ------
    ValueError
        Raised when no metrics set is registered to ``name``
    """
    try:
        function = _registered_metrics_sets[name]
    except KeyError:
        raise ValueError('no metrics set registered as %r' % name)

    return function()


register_metrics_set('none', set)


@register_metrics_set('default')
def default_metrics():
    """The default default set of metrics.
    """
    return {
        Returns(),
        BenchmarkReturns(),
        PNL(),
        CashFlow(),
        Orders(),
        Transactions(),

        SimpleLedgerField('positions'),

        StartOfPeriodLedgerField(
            'portfolio.positions_exposure',
            'starting_exposure',
        ),
        DailyLedgerField(
            'portfolio.positions_exposure',
            'ending_exposure',
        ),

        StartOfPeriodLedgerField(
            'portfolio.positions_value',
            'starting_value'
        ),
        DailyLedgerField('portfolio.positions_value', 'ending_value'),

        StartOfPeriodLedgerField('portfolio.cash', 'starting_cash'),
        DailyLedgerField('portfolio.cash', 'ending_cash'),

        DailyLedgerField('portfolio.portfolio_value'),

        DailyLedgerField('position_tracker.stats.longs_count'),
        DailyLedgerField('position_tracker.stats.shorts_count'),
        DailyLedgerField('position_tracker.stats.long_value'),
        DailyLedgerField('position_tracker.stats.short_value'),
        DailyLedgerField('position_tracker.stats.long_exposure'),
        DailyLedgerField('position_tracker.stats.short_exposure'),

        DailyLedgerField('account.gross_leverage'),
        DailyLedgerField('account.net_leverage'),
    }
