# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

FitFindr helps someone shopping secondhand turn a plain-language request, like "vintage graphic tee under $30," into a complete recommendation. It searches real thrift listings for a match, suggests an outfit that pairs the find with pieces already in the user's wardrobe, and writes a short caption someone could actually post about it. If nothing matches the request, it says so and suggests what to change instead of guessing.

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Filters listings by price ceiling and size, then ranks the rest by keyword overlap between the query and each listing's `title`, `description`, `style_tags`, and `category`; drops anything with zero keyword matches.
- **Inputs:** `description` (str), `size` (str or None), `max_price` (float or None, inclusive)
- **Returns:** A list of listing dicts (all 11 fields — `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, `platform`), best keyword match first, capped at `config.SEARCH_RESULT_LIMIT`.
- **When it has nothing:** An empty list — never `None`, never an exception.

### `suggest_outfit`

- **What it does:** Suggests 1–2 outfits pairing a new item with the user's wardrobe, naming specific pieces the user already owns; falls back to general styling advice when the wardrobe is empty.
- **Inputs:** `new_item` (listing dict), `wardrobe` (dict with an `items` list, each item having `id`, `name`, `category`, `colors`, `style_tags`, `notes`)
- **Returns:** A non-empty string of outfit suggestions.
- **When it has nothing:** If `wardrobe["items"]` is empty, returns general styling advice for the item instead of failing — never `""`.

### `create_fit_card`

- **What it does:** Writes a 2–4 sentence social-post-style caption for the item, mentioning its title, price, and platform once each, based on the suggested outfit.
- **Inputs:** `outfit` (str), `new_item` (listing dict)
- **Returns:** A 2–4 sentence string caption.
- **When it has nothing:** If `outfit` is empty or whitespace-only, returns a descriptive message string instead of raising.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If `search_listings` returns an empty list, put a message in `session["error"]` naming what to change (price, size, or keywords) and stop — do not call `suggest_outfit`. Otherwise, take the first result and go to `suggest_outfit`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regex, in `agent.py::_parse_query`. A `size X` pattern pulls out the size, a `$X` pattern pulls out the price ceiling, and whatever text is left (minus the word "under") becomes the description.

**What moves through the session:** `parsed` → `search_results` → `selected_item` → `outfit_suggestion` → `fit_card`, or `error` if the run stops early after `search_results`.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30'

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Here are 2 outfit ideas that pair the new **Y2K Baby Tee — Butterfly Print** with pieces already in your wardrobe:

### Outfit 1: Classic Y2K Contrast (Casual & Edgy)
* **Top:** Y2K Baby Tee — Butterfly Print
* **Bottoms:** Baggy straight-leg jeans, dark wash
* **Outerwear:** Vintage black denim jacket (worn open)
* **Shoes:** Chunky white sneakers
* **Accessories:** Black crossbody bag

**Why it works:** The ultra-slim, fitted silhouette of the baby tee creates a great proportion play when paired with your high-waisted, baggy dark-wash jeans (the ultimate 2000s combo). Layering the slightly cropped black denim jacket on top adds texture and ties into the black accents of the tee, while the chunky white sneakers finish the retro streetwear look.

---

### Outfit 2: Elevated Retro-Neutral (Smart-Casual)
* **Top:** Y2K Baby Tee — Butterfly Print
* **Bottoms:** Wide-leg khaki trousers
* **Accessories:** Brown leather belt + Black crossbody bag
* **Shoes:** Black combat boots

**Why it works:** Tucking the butterfly baby tee into your wide-leg khaki trousers instantly balances fitted and loose proportions for a chic, effortless silhouette. Cinching the look with your brown leather belt adds a nice contrast against the tan trousers, and grounding the outfit with black combat boots adds an unexpected edge that keeps it from looking too plain.

  Fit card: Found the ultimate butterfly print Y2K baby tee on Depop for just $18 and I'm literally obsessed. Styled it with some baggy dark denim and chunky sneakers today for the dreamiest 2000s streetwear fit. 🦋✨
```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]
```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
Here are two ways to style the Vintage Levi's 501 Jeans using pieces already in your wardrobe:

### Outfit 1: Casual & Balanced
*Pair the **Vintage Levi's 501 Jeans** with the **White ribbed tank top**, the **Vintage black denim jacket**, and the **Chunky white sneakers**.*

**Why it works:**
Levi's 501s have a classic, straight-leg fit that balances nicely with the fitted white tank top. Layering the slightly cropped black denim jacket on top adds a cool, vintage-on-vintage texture while keeping your silhouette defined. Finish with chunky white sneakers for an effortless, everyday street-style look.

### Outfit 2: Edgy & Proportion-Play
*Pair the **Vintage Levi's 501 Jeans** with the **Black cropped zip hoodie**, the **Black combat boots**, and the **Brown leather belt**.*

**Why it works:**
Tucking a fitted top or wearing a cropped layer with high-to-mid-rise 501s creates great proportions. The black cropped zip hoodie pairs seamlessly with the mid-ankle height black combat boots for a cohesive, slightly edgy vibe. Add the brown leather belt to break up the all-black top and add a subtle, warm contrast against the medium wash denim.
```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
The hunt is finally over and my crisp white sneakers have found their soulmate. Snagged these vintage Levi's 501 jeans in the absolute dreamiest medium wash for just $38.0 on Depop. Honestly, the slouchy fit is giving total 90s off-duty model and I'm never taking them off.
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* Help checking my acceptance criteria during Milestone 3, to see if they were actually testable.
- *What came back:* My first draft of the state criterion didn't say which argument it was comparing, and had no rate attached.
- *What I changed:* Rewrote it to name the exact comparison and added "5 of 5 tries."

**Moment 2**

- *What I asked for:* A commit for the search helper functions I'd drafted.
- *What came back:* Claude found that `_keywords`, `_size_tokens`, and `_size_matches` had a few bugs and wouldn't actually run.
- *What I changed:* Fixed the bugs before committing, so the functions worked.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Item in session matches item passed to suggest_outfit | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card mentions the item's actual price | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Price ceiling respected by every returned listing | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

Produced by `run_eval.py` against `agent.py::run_agent` (criteria 1, 2, 3, 5) and a direct call to `tools.py::create_fit_card` (criterion 4, which needs 5 different items rather than 5 tries of the same query — see the note in `scenarios.py`). Full output: `results/run_2026-10-07_1838_before.md`.

**Real output, one try per criterion:**

Criterion 1 — `agent.py::run_agent`, query `'vintage graphic tee under $30'`:
```
Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop
Outfit:   Here are 2 outfit ideas that pair the new Y2K Baby Tee — Butterfly Print with pieces already in your wardrobe: ...
Fit card: Found the ultimate butterfly print Y2K baby tee on Depop for just $18 and I'm literally obsessed. Styled it with some baggy dark denim and chunky sneakers today for the dreamiest 2000s streetwear fit. 🦋✨
```

Criterion 2 — `agent.py::run_agent`, query `'designer ballgown size XXS under $5'`:
```
Nothing in the listings matched description 'designer ballgown', size XXS, under $5.
Things to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; drop the size, or try a neighbouring one; raise the price ceiling above $5.
```

Criterion 3 — `agent.py::run_agent`, query `'platform sneakers size 8'`:
```
session["selected_item"]["id"]: lst_019
session["search_results"][0]["id"]: lst_019
```
Both come from the same dict — `run_agent` reads `session["selected_item"]` back out of the session to call `suggest_outfit` and `create_fit_card` (agent.py lines ~183-202), rather than a separate copy.

Criterion 4 — `tools.py::create_fit_card`, called directly on `lst_001` ($38):
```
Still pinching myself over finding these Vintage Levi's 501 Jeans in the absolute best medium wash for just $38. They fit like a glove and instantly elevated my go-to everyday tee-and-sneakers combo. Huge shoutout to my favorite Depop seller for the ultimate closet staple!
```

Criterion 5 — `tools.py::search_listings`, query `'denim jacket'`, `max_price=50`:
```
lst_007 Denim Jacket — Light Wash, Cropped  42.0
lst_001 Vintage Levi's 501 Jeans — Medium Wash  38.0
lst_004 90s Track Jacket — Navy/White Stripe  45.0
lst_016 High-Waisted Denim Shorts — Cutoff  24.0
lst_032 Shacket — Olive Canvas  33.0
lst_037 Straight Leg Black Jeans — Faded  30.0
lst_038 Denim Vest — Medium Wash, Studded  27.0
```
All 7 returned listings are at or under $50.

A note on this run: the first two attempts at `run_eval.py` hit a real `503 UNAVAILABLE` ("experiencing high demand") from the Gemini free tier partway through, which `agent.py`'s `ModelUnavailable` handler caught cleanly each time — no crash, no hang. That's unrelated to the agent's own correctness, so those two runs were discarded; the table above is from the third, clean run.

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Matching query completes all three tools | 4 of 5 | MET (5/5), but see note below | 5 of 5 tries completed with a fit card, which clears the 4/5 bar on paper — but see the diagnosis underneath before trusting this one |
| 2 | Impossible query stops before the second tool | 5 of 5 | MET (5/5) | All 5 tries stopped at the branch with the error message set and `suggest_outfit` never called (confirmed via the trace, which ends at step `branch`) |
| 3 | Item in session matches item passed to suggest_outfit | 5 of 5 | MET (5/5) | All 5 tries: `session["selected_item"]["id"]` equaled `session["search_results"][0]["id"]`, and the same dict is what `run_agent` passes into `suggest_outfit`/`create_fit_card` — no copy is ever made |
| 4 | Fit card mentions the item's actual price | 4 of 5 | MET (5/5) | Called `create_fit_card` directly on 5 different listings; every caption included that item's real price string |
| 5 | Price ceiling respected by every returned listing | 5 of 5 | MET (5/5) | All 5 tries returned the same 7 listings from `search_listings`, and every one of their prices was ≤ $50 |

**Diagnoses**

No criterion missed its target this run, so there's no tool/branch/session/model failure to trace. But "nothing missed" isn't the same as "nothing to say" — criterion 1 deserves a second look before taking its MET at face value.

**Criterion 1's test didn't actually test what the target was written to protect against.** The 4/5 target exists because plain keyword matching can miss a real match on an unlucky phrasing — that's the risk named in `criteria.md`'s own "why." But the scenario in `scenarios.py` runs the *same* query, `'vintage graphic tee under $30'`, five times. `search_listings` is deterministic, so all 5 tries hit the identical search result; the only thing that could vary between tries is the wording `suggest_outfit` and `create_fit_card` generate, and neither of those has a failure path that a bad search phrasing would ever trigger. The one real failure this run hit — a `503` from the model provider — is external and has nothing to do with phrasing either. So a MET here mostly proves the model-calling path is stable, not that the search tolerates varied phrasing 4 times out of 5. This isn't a bug in the agent; it's a gap in how the scenario was designed to measure the criterion.

**The fix, next time:** replace the single repeated query in criterion 1's scenario with 5 *different* matching queries (e.g. pulled from `python app.py examples`), so a phrasing that the keyword scorer actually fails on has a chance to show up as a real FAIL instead of being invisible to the test.

---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
$ python app.py ask 'denim jacket under $50' --empty-wardrobe --trace
(running with an empty wardrobe)
[1] parse_query
      in:  denim jacket under $50
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 7 items: Denim Jacket — Light Wash, Cropped, Vintage Levi's 501 Jeans — Medium Wash, 90s Track Jacket — Navy/White Stripe … +4 more
      →    7 match(es)
[3] select_item
      out: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
[4] suggest_outfit
      in:  Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
      out: A light-wash cropped denim jacket is a versatile wardrobe staple that pairs effortlessly with high-waisted wid…
      →    0 wardrobe item(s)
[5] create_fit_card
      in:  Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
      out: Scored this light-wash cropped denim jacket on Poshmark for just $42 and I'm officially obsessed. The boxy fit…
```

**Empty search**

```
$ python app.py ask 'designer ballgown size XXS under $5' --trace
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
      →    0 match(es)
[3] branch
      →    search returned []: stopping before suggest_outfit

  Nothing in the listings matched description 'designer ballgown', size XXS, under $5.
Things to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; drop the size, or try a neighbouring one; raise the price ceiling above $5.
```

The empty-search trace stops at step 3, before `suggest_outfit` or `create_fit_card` ever run — visibly shorter than the happy path's 5 steps, which is the proof the branch is actually doing something.

**On the MCP move:** `run_agent` now calls `search_listings` through `mcp_client.call_tool` instead of importing and calling the function directly, with a fallback to the direct call if the MCP server can't be reached. Nothing behaved differently afterward — the same query returns the same top-ranked listing either way. The one thing MCP did surface: the tool's published description in `mcp_server.py` claimed it searched `brand` and `colors` and broke price ties by cheapest-first, neither of which the actual implementation does. Writing the tool's contract out separately from its code, for an audience that can't see the implementation, is what caught that mismatch.



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:** Not the agent's code — the *test* for criterion 1. The old check ran the same query, `'vintage graphic tee under $30'`, five times through `run_eval.py`. The new check runs 5 genuinely different matching queries (`'vintage graphic tee under $30'`, `'90s track jacket in size M'`, `'silk slip dress in midi length under $40'`, `'platform sneakers size 8'`, `'denim jacket under $50'`) directly through `agent.py::run_agent`, each selecting a different real item.

**Which failure it was meant to fix:** Not a code failure — a measurement gap, diagnosed in Milestone 4. `search_listings` is deterministic, so repeating one query 5 times could never actually exercise the phrasing-variance risk the 4/5 target was written for. The old MET (5/5) was true but weak evidence.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools (5 different queries) | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Item in session matches item passed to suggest_outfit | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card mentions the item's actual price | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Price ceiling respected by every returned listing | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

Full output: `results/run_2026-10-08_2010_after.md` (criteria 2, 3, 5, plus a smoke-test of criterion 1's old scenario). Criterion 1's real evidence this time:

```
Try 1: PASS | query='vintage graphic tee under $30'              | item=Y2K Baby Tee — Butterfly Print
Try 2: PASS | query='90s track jacket in size M'                 | item=90s Track Jacket — Navy/White Stripe
Try 3: PASS | query='silk slip dress in midi length under $40'   | item=90s Silk Slip Dress — Floral, Midi Length
Try 4: PASS | query='platform sneakers size 8'                   | item=Platform Sneakers — White Chunky Sole
Try 5: PASS | query='denim jacket under $50'                     | item=Denim Jacket — Light Wash, Cropped
```

Note: try 4 hit the 15-requests-per-minute limit mid-run — the adapter paused 7s, then 60s, and retried automatically. That's the rate limiter doing its job, not a failure.

**Did it help, and how do I know:** The raw number didn't move — still 5/5, still MET. What changed is whether I can trust that number. Before, 5/5 came from one query that could only ever select one item, so it couldn't have failed from a phrasing miss even if my search genuinely had that weakness. After, 5/5 comes from 5 different real phrasings selecting 5 different items, which is the actual scenario the 4/5 target was written to guard against — and all 5 still passed. So this run gives me real confidence that `search_listings` handles a reasonable spread of query phrasing, rather than confidence built on a test that couldn't have told me otherwise. If I had to guess why none of the 5 missed: the test queries are still fairly literal matches to each item's title/style_tags (e.g. "90s track jacket" → a listing literally titled "90s Track Jacket"), so the real edge case — an indirect or synonym-heavy phrasing — still hasn't been tried. That's named honestly under What's Still Broken below.



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
