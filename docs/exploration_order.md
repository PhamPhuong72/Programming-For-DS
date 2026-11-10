# Order of exploration

## Why a fixed order

A conclusion is only as good as the data it was computed on. Our first notebooks grew in the order in which we noticed things ("we saw X, so we looked at X"). That order mixes three different questions:

1. **What is in the files, and what do the columns mean?** (structure and meaning)
2. **What is wrong with the data?** (audit)
3. **What does the data say?** (statistics and analysis)

A statistic computed on uncleaned data (a correlation, a mean, a ratio) is a **raw result**. It can *show* us a problem and motivate a cleaning rule, but it is not a finding. Findings are computed after cleaning.

This order follows the course template of `notebooks/01_collection_exploration.ipynb`: context, load and compare with the description, quality exploration, cleaning decisions, exploration summary.

## The steps

| Step | Question | Notebook | May conclude | State |
|---|---|---|---|---|
| 1 | What do the files contain, and where do they differ from the author's description? | [kaggle/01_compare_with_description_run.ipynb](../kaggle/01_compare_with_description_run.ipynb), section 2 of notebook 01 | Record counts, keys, codes that the description does not define | Done. Redone with the safe load (second run): 283,045 users with rows, 19,630 without, 8 of them declare anime |
| 2 | What does each column mean, and in which format is it stored? | [kaggle/02_column_dictionary_run.ipynb](../kaggle/02_column_dictionary_run.ipynb) | Meaning tagged [A], [I] or [V]; formats; placeholders written as words | Done |
| 3 | What is wrong with each table (placeholders, impossible values, inconsistencies)? | [kaggle/03_raw_quality_audit.ipynb](../kaggle/03_raw_quality_audit.ipynb) | A list of problems with counts. **No cleaning, no statistics between columns** | Written, not yet run |
| 4 | What do we do about each problem? | section 4 of notebook 01, output `data/processed/` | A cleaning rule per problem, with the row count before and after | Not started |
| 5 | Do the meanings we only guessed hold on the **cleaned** data? | [05a](../kaggle/05a_verify_meanings_run.ipynb), [05b](../kaggle/05b_rewatch_check_run.ipynb), [05c](../kaggle/05c_sample_vs_published.ipynb) | Meaning tags [V]; how our sample relates to the published numbers | Run on raw data once. Must be re-run on cleaned data |
| 6 | The research questions | `notebooks/02_analysis.ipynb`, `notebooks/03_ml_question.ipynb` | Findings | Not started |

## Rules

1. **Load safely, always.** `pd.read_csv(..., keep_default_na=False, na_values=[""])`. Otherwise the username `null` becomes missing.
2. **Steps 1–3 only measure.** They never drop or change a value.
3. **Every cleaning rule is written down in step 4** with the evidence from step 3 and the number of rows before and after.
4. **Statistics between columns belong to step 5 or later** and use the cleaned data. If one was computed earlier on raw data, it is re-run.
5. **A meaning tagged [V] by a statistical test is re-confirmed after cleaning.**

## Conclusions that must be re-checked after cleaning

Everything in this table was computed on raw data.

| Conclusion | Where | Why cleaning may change it | Re-check |
|---|---|---|---|
| Users with list rows, users without, users declaring anime without rows | step 1 | The first run lost the user `null` (283,044 / 19,631 / 9). **Re-checked with the safe load: 283,045 / 19,630 / 8** | **Done** |
| Mean score 7.49, dropped 4.95 against completed 7.57, share of unrated rows per status | step 1 | Includes the 537 rows with an unknown status. Depends on the rule for score 0 and for unknown status | **Yes** (a small change is expected) |
| Counts of placeholders and missing values per column | step 2 | Counted before we decided which words are missing | **Yes**, after the rules of step 4 |
| `popularity` follows `members`, `rank` against `score`, `episodes` by type | 05a | Anime table only, which has few impossible values | Check only |
| `related`: 4,515 empty lists, 96.5% of Sequel links mirrored | 05a | Anime table only | Check only |
| Our counts against the published `members` and `scored_by`: ratios, the 2 and 59 anime above the published value | 05a, 05c | Built from all 80 million rows. If a cleaning rule drops rows, the counts change | **Yes**, if rows are dropped |
| `score` against the mean of our users' scores (Pearson 0.976, mean difference −0.17) | 05a | Uses all rated rows | **Yes**, if rows are dropped |
| `stats_episodes` against the sum of `my_watched_episodes` (equal for 50.8%, median ratio 1.000) | 05a | `my_watched_episodes` reaches 65,535 and `stats_episodes` reaches 10,989,789. This is the **most sensitive** result | **Yes** |
| `stats_rewatched` is none of the three candidates we tried | 05a, 05b | `my_rewatching_ep` reaches 16,777,215 | **Yes** (the verdict "unverified" will probably stay) |
| Declared counts against actual rows, and whether the users without rows have other values | 03 parts 4 and 5 | Not yet run. Depends on the safe load | Run first |

## Cleaning decisions still open (for step 4)

- Impossible values: `stats_episodes`, `my_watched_episodes`, `my_rewatching_ep` (cap, flag or drop).
- The 537 rows with an unknown `my_status`.
- Placeholders written as words: `Unknown`, `None`, `0000-00-00`, `episodes = 0`.
- Anime that have not aired yet (336).
- Missing gender (28%), birth date (44%) and location (48%).
- The users with no row in the list table (drop them from list analyses, or report them as missing).
- The 129 users with missing `join_date` and statistics.
