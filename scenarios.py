"""
The runs your test needs. ← UNIT 4, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
the empty-search branch needs an impossible query. One about the fit card needs
the same item run more than once. Working that out is Milestone 3's first step,
and this file is where you write it down.

`run_eval.py` runs everything here five times and writes the run log — five
because your criteria are written out of five.

Three scenarios are filled in to show the shape. Add or change whatever your
own criteria need — these are a starting point, not a fixed set.
"""

SCENARIOS = [
    {
        # A query the data can match. Criterion 1.
        "name": "matching query completes",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        # A query nothing can match. Criterion 2 — the branch.
        "name": "impossible query stops early",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        # A user with nothing saved. One of unit 4's three failure modes.
        "name": "empty wardrobe",
        "query": "denim jacket under $50",
        "wardrobe": "empty",
        "criterion": None,
    },
    {
        # A matching query, run 5 times. Criterion 3 — state: the item found
        # in search_results is the same item (by id) passed to suggest_outfit
        # and create_fit_card. This is deterministic (no model call picks the
        # item), so any matching query works.
        "name": "state matches through the session",
        "query": "platform sneakers size 8",
        "wardrobe": "example",
        "criterion": 3,
    },
    {
        # A query with a real price ceiling. Criterion 5 — every listing
        # search_listings returns must have a price at or under that ceiling.
        "name": "price ceiling respected",
        "query": "denim jacket under $50",
        "wardrobe": "example",
        "criterion": 5,
    },
    # Criterion 4 (the fit card mentions the item's price, across 5 DIFFERENT
    # listings) isn't tested here. run_eval.py repeats one scenario's query,
    # which always selects the same top-ranked item — it can't produce 5
    # different listings on its own. That criterion is tested directly with
    # create_fit_card() on 5 different items instead; see the README's Run
    # Log for that output.
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )
    return problems
