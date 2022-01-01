# http://pyrocko.org - GPLv3
#
# The Pyrocko Developers, 21st Century
# ---|P------/S----------~Lg----------

from __future__ import absolute_import, print_function

from .. import common
from pyrocko import util
from pyrocko.plot import terminal
from pyrocko.get_terminal_size import get_terminal_size
from pyrocko.squirrel import model


def setup(subparsers):
    p = common.add_parser(
        subparsers, 'coverage',
        help='Report time spans covered.',
        description='''Report time spans covered.

Time spans covered by the given data selection are listed or plotted.
''')

    common.add_selection_arguments(p)
    common.add_query_arguments(p, without=['time'])
    return p


def call(parser, args):
    from pyrocko import squirrel as sq

    squirrel = common.squirrel_from_selection_arguments(args)
    tmin_g, tmax_g = squirrel.get_time_span()
    sx, _ = get_terminal_size()

    kwargs = common.squirrel_query_from_arguments(args)
    kinds = kwargs.pop('kind', sq.supported_content_kinds())
    codes = kwargs.pop('codes', None)
    tmin = kwargs.pop('tmin', tmin_g)
    tmax = kwargs.pop('tmax', tmax_g)

    for kind in kinds:
        coverage = squirrel.get_coverage(
            kind,
            codes_list=[codes] if codes else None,
            tmin=tmin,
            tmax=tmax,
            return_raw=False, **kwargs)

        if coverage:
            scodes_list = [
                '.'.join(entry.codes.split(model.separator))
                for entry in coverage]

            label = 'kind: %s' % kind
            sc = max(len(s) for s in scodes_list)
            sc = max(len(label), sc) + 1
            si = (sx-sc) - 2
            sl = si // 2
            sr = si - sl
            print(''.join((
                label.ljust(sc),
                terminal.ansi_dim,
                terminal.bar_right,
                util.time_to_str(tmin).ljust(sl),
                util.time_to_str(tmax).rjust(sr),
                terminal.bar_left,
                terminal.ansi_dim_reset)))

            for scodes, entry in zip(scodes_list, coverage):
                line = scodes.ljust(sc) + terminal.bar(
                    tmin, tmax, entry.changes, entry.tmin, entry.tmax, sx-sc)
                print(line)
