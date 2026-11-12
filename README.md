# CSC17104 Final Project — MyAnimeList Dataset Analysis

> Fill every placeholder with work done by your team. Do not include conclusions you did not verify.

## Team and responsibilities

| Member | Student ID | Questions owned | Other tasks |
|---|---|---|---|
| [Member A] | [ID] | Q1, Q2 | [Task] |
| [Member B] | [ID] | Q3, Q4 | [Task] |
| [Member C] | [ID] | Q5, Q6 | [Task] |

## Dataset

- **Topic and unit of observation:** anime and users of MyAnimeList (MAL). Three tables: one row is an anime (`AnimeList.csv`), a user (`UserList.csv`), or a user–anime pair on a user's list (`UserAnimeList.csv`).
- **Original author:** Matěj Račinský.
- **URL and publication date:** [kaggle.com/datasets/azathoth42/myanimelist](https://www.kaggle.com/datasets/azathoth42/myanimelist), 2018 (Kaggle version 9).
- **License and attribution:** Kaggle lists "Database: Open Database, Contents: Database Contents". The data may be used without extra permission or fees; cite as *Matěj Račinský, "MyAnimeList Dataset." Kaggle, 2018, doi: 10.34740/KAGGLE/DSV/45582.*
- **Collection method:** crawl of public pages of MyAnimeList.net. Usernames were collected from the 2015–2018 watching-challenge forum threads and from the first ~40k of ~80k clubs. **Limitations:** users come from forums and clubs, so the sample may lean towards active users; the data stops around 2018; each user–anime pair keeps only the current status and last update, with no history.
- **Raw files (the ones we analyse):**

  | File | One row is | Size |
  |---|---|---|
  | `AnimeList.csv` | an anime | 10 MB |
  | `UserList.csv` | a user | 30 MB |
  | `UserAnimeList.csv` | a user–anime pair | ~5 GB |

- **Other versions in the same Kaggle dataset:** the author also publishes *filtered* (users with birth date, location and gender: 116,133 users, 35,802,010 list rows) and *cleaned* versions (further fixes by the author). We analyse the raw files and clean them ourselves, so every filtering decision is ours and documented; the other versions are only used for comparison.
- **Checks against the author's description:** the differences we found (users with empty lists, the username `null` read as `NaN`, 537 rows with unexplained `my_status` values) are in [kaggle/01_compare_with_description_run.ipynb](kaggle/01_compare_with_description_run.ipynb).
- **Related public notebooks:** the dataset has [many public notebooks](https://www.kaggle.com/datasets/azathoth42/myanimelist/code). The ones we reviewed are mostly recommender systems, score prediction from anime metadata, and genre/gender visualisations. **How our questions differ:** [TODO, fill in once the questions are final]

## Order of exploration

We explore in a fixed order: **1** compare with the description, **2** column dictionary, **3** raw quality audit (only measures), **4** cleaning decisions, **5** verify meanings and summarise on the cleaned data, **6** research questions. A number computed on raw data is not a finding until it is re-checked after cleaning. The steps, the rules and the list of conclusions to re-check are in [docs/exploration_order.md](docs/exploration_order.md).

## Known data limits (verified on Kaggle)

> The numbers below were computed on **raw** data. The ones marked in [docs/exploration_order.md](docs/exploration_order.md) are re-checked after the cleaning step.

Evidence for each line is in the step notebooks in [kaggle/](kaggle/) (the order is explained in [docs/exploration_order.md](docs/exploration_order.md)), and every column is listed in [step 2](kaggle/02_column_dictionary_run.ipynb) with a tag: **[A]** author-defined, **[I]** inferred, **[V]** verified by us.

- **Keys.** `anime_id` is unique in `AnimeList.csv` (confirmed). `user_id` is **not** unique in `UserList.csv` (302,673 distinct values for 302,675 rows: 2 ids are each used by 2 usernames: one account crawled under two names, with the same list stored twice, 1,059 duplicated list rows), so tables are joined on `username`. `(username, anime_id)` is the key of `UserAnimeList.csv`: 0 repeated pairs among 80,076,112 rows (confirmed). So counting rows per anime counts users.
- **Our users vs the published counts.** The crawled users are only a part of MAL, so our counts should be smaller than the published `members` and `scored_by`. That holds for `members` (our count is larger for 2 of 14,474 anime) but **not for `scored_by`** (larger for 59 anime, up to 64 times), which we have not explained yet. We use `scored_by` for the order of anime, not as an exact count. Over all anime our rows are about 24% of `members`. The share varies by anime (middle 90%: 21% to 55%), so the crawled users are not a uniform slice of MAL and our results describe the crawled users.
- **`stats_rewatched` (user table) is unverified [I]. We do not build a main question on it.** What we know it is *not*: the number of anime rewatched (5,086 users have a value larger than their whole list), the sum of `my_rewatching_ep` (96.9% of users with a positive value have no row with an episode value; rank correlation 0.11 where both exist), or the number of rows with `my_rewatching = 1` (rank correlation 0.14). It behaves like a total that MyAnimeList computed on the profile, which we cannot recompute from our tables. If a question needs it, we use it as given and say so. Details: [step 5b](kaggle/05b_rewatch_check_run.ipynb) and [step 5a](kaggle/05a_verify_meanings_run.ipynb).
- **Impossible values.** `stats_episodes` reaches 243,794,900 (step 3), `my_watched_episodes` 65,535 and `my_rewatching_ep` 16,777,215, so they need a cap or removal before use. `stats_episodes` equals the sum of the user's `my_watched_episodes` for only 50.8% of users (median ratio 1.000).
- **Placeholders that `isna()` does not see:** `source = Unknown` (4,210 anime), `rating = None` (544), `type = Unknown` (30), `0000-00-00` dates, and `episodes = 0` meaning unknown.
- **`related`:** the 4,515 anime without a relation are written as an empty list `[]`, not as missing data.
- **`rank` is not simply the order of `score`:** its rank correlation is −0.855 with `score` and −0.862 with `members`.

## Research questions

See [docs/question_plan.md](docs/question_plan.md).

## Reproduce

1. Install Miniconda / Conda.
2. At the repository root, create and activate the environment:
   ```bash
   conda env create -f environment.yml
   conda activate csc17104-final
   jupyter lab
   ```
3. Download the three raw files from the Kaggle URL above and place them in `data/raw/` (do not commit them). Alternatively run on Kaggle, where the dataset is attached as an input and no download is needed.
4. Run the notebooks in order:
   - `notebooks/01_collection_exploration.ipynb`
   - `notebooks/02_analysis.ipynb`
   - `notebooks/03_ml_question.ipynb`

   `UserAnimeList.csv` has about 80 million rows. Read only the columns you need and use small dtypes, otherwise a laptop with 16 GB of RAM can run out of memory.

## Working with Kaggle and Git without conflicts

We run the heavy notebooks on Kaggle and keep the project in Git. Kaggle's "Link to GitHub" writes the notebook to the **repository root** under a name taken from the Kaggle notebook title (currently `24122024-ltkhdl-final-project.ipynb`) and **overwrites the whole file on every push**. A conflict only appears when two people change the same file, so we split the files by owner:

| Path | Who changes it | Purpose |
|---|---|---|
| `24122024-ltkhdl-final-project.ipynb` (repo root) | **Only Kaggle.** Never edit or commit it by hand. | Mirror of the last Kaggle run, with real outputs |
| `kaggle/NN_<topic>.ipynb` | Us | **Source** of a step: clean notebook, no outputs, imported into Kaggle |
| `kaggle/NN_<topic>_run.ipynb` | Us | **Record** of a step: copy of the Kaggle mirror with our explanations written below the real outputs |
| `notebooks/01…03_*.ipynb` | Us | Final deliverable notebooks, assembled from the stage records |

**One stage, step by step:**

1. Import `kaggle/NN_<topic>.ipynb` into the linked Kaggle notebook (replace its content) and run it.
2. Push from Kaggle (Save version → GitHub). This overwrites the root file on the Kaggle branch.
3. Locally: `git fetch`, then `git status`, then `git pull`. Because nobody edited the root file, the pull merges cleanly.
4. Copy the root file to `kaggle/NN_<topic>_run.ipynb` and add explanations below its outputs there. Do not edit the root file.
5. Commit and push your own files, then start the next stage with a new source file.

**Rules that keep it conflict-free:**

- **Pull before you commit or push.** Your commits then sit on top of Kaggle's.
- **One Kaggle notebook is linked to one branch.** Each member works on their own branch and the branches are merged into `main` at the end, as the course requires.
- **Keep our files and Kaggle's files on different paths.** Kaggle only writes the root file, and we only write inside `kaggle/` and `notebooks/`.
- **Data stays out of Git.** `data/raw/` and `data/processed/` are ignored.

**If `git push` is rejected** (non-fast-forward), Kaggle pushed first. Run `git pull`, then `git push` again. A merge commit is normal and is not a content conflict.

**If a real conflict appears in the root notebook**, always keep Kaggle's version; never merge the JSON by hand:

```bash
git checkout --theirs -- 24122024-ltkhdl-final-project.ipynb
git add 24122024-ltkhdl-final-project.ipynb
git commit
```

(`--theirs` is the remote version during a merge, which is what `git pull` does by default. Use `--ours` instead if you pulled with `--rebase`.)

## Key findings

- [Fill with verified findings, numbers, and limitations after analysis]

## Project notes

- Raw data must remain unchanged.
- Shared processed data should document cleaning decisions.
- For every filtering, merging or dropping operation report row count before/after and explain why.
- Use `LLM_USAGE.md` for significant AI assistance. Each member must understand submitted code and analysis.
