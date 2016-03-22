"""Rank annotators for the standings generator.

Each rank annotator is responsible for computing a particular type of ranking
for each team and annotating team standings with them. The most obvious example
is the basic ranking from first to last (taking into account equal rankings),
but there are other "types" of ranks, for example, ranks within brackets
("subranks") or divisions ("division ranks").

Note: There's a registry at the bottom of the file. If you add a new
RankAnnotator subclass, be sure to add it to the registry.
"""

from .metrics import metricgetter
from itertools import groupby
from operator import attrgetter
import logging
logger = logging.getLogger(__name__)

def RankAnnotator(name, *args, **kwargs):
    """Factory function. Returns an instance of an appropriate subclass of
    BaseRankAnnotator, with the given arguments passed to the constructor."""
    klass = registry[name]
    return klass(*args, **kwargs)


class BaseRankAnnotator:
    """Base class for all rank annotators.

    A rank annotator is a class that adds rankings to a TeamStandings object.
    Subclasses must implement the method `annotate_teams()`.

    Subclasses must also set the `key`, `name` and `abbr` attributes, either as
    class attributes or object attributes. The `glyphicon` attribute is
    optional.

     - `name` is a name for display in the user interface
     - `abbr` is used instead of `name` when there is not enough space for `name`
     - `glyphicon`, optional, is the name of a glyphicon to be used if possible

    The default constructor does nothing, but subclasses may have constructors
    that initialise themselves with parameters."""

    key = None # must be set by subclasses
    name = None # must be set by subclasses
    abbr = None # must be set by subclasses
    glyphicon = None

    def annotate(self, standings):
        standings.record_added_ranking(self.key, self.name, self.abbr, self.glyphicon)
        self.annotate_teams(standings)

    def annotate_teams(self, standings):
        """Annotates the given `standings` by calling `add_ranking()` on every
        `TeamStandingInfo` object in `standings`.

        `standings` is a `TeamStandings` object.
        """
        raise NotImplementedError("BaseRankAnnotator subclasses must implement annotate_teams()")


class BasicRankAnnotator(BaseRankAnnotator):

    key = "rank"
    name = "rank"
    abbr = "Rk"
    glyphicon = "signal"

    def __init__(self, metrics):
        self.rank_key = metricgetter(*metrics)

    def annotate_teams(self, standings):
        rank = 1
        for key, group in groupby(standings, key=self.rank_key):
            group = list(group)
            for tsi in group:
                tsi.add_ranking("rank", (rank, len(group) > 1))
            rank += len(group)


class BaseRankWithinGroupAnnotator(BaseRankAnnotator):
    """Base class for ranking annotators that rank within groups."""

    def annotate_teams(self, standings):
        by_group = sorted(standings, key=self.group_key)
        for key, group in groupby(by_group, key=self.group_key):
            rank_in_group = 1
            for _, subgroup in groupby(group, self.rank_key):
                subgroup = list(subgroup)
                for tsi in subgroup:
                    tsi.add_ranking(self.key, (rank_in_group, len(subgroup) > 1))
                rank_in_group += len(subgroup)


class SubrankAnnotator(BaseRankWithinGroupAnnotator):

    key = "subrank"
    name = "subrank"
    abbr = "SubR"

    def __init__(self, metrics):
        self.group_key = metricgetter(metrics[0])
        self.rank_key = metricgetter(*metrics[1:])


class DivisionRankAnnotator(BaseRankWithinGroupAnnotator):

    key = "division_rank"
    name = "division rank"
    abbr = "DivR"

    def __init__(self, metrics):
        self.group_key = lambda x: x.team.division.id
        self.rank_key = metricgetter(*metrics)


class RankFromInstitutionAnnotator(BaseRankWithinGroupAnnotator):

    key = "institution"
    name = "rank from institution"
    abbr = "InstR"

    def __init__(self, metrics):
        self.group_key = lambda x: x.team.institution.id
        self.rank_key = metricgetter(*metrics)


registry = {
    "rank"       : BasicRankAnnotator,
    "subrank"    : SubrankAnnotator,
    "division"   : DivisionRankAnnotator,
    "institution": RankFromInstitutionAnnotator,
}

