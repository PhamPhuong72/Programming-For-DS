# CSC17104 Final Project — [PROJECT TITLE]

> Fill every placeholder with work done by your team. Do not include conclusions you did not verify.

## Team and responsibilities

| Member | Student ID | Questions owned | Other tasks |
|---|---|---|---|
| [Member A] | [ID] | Q1, Q2 | [Task] |
| [Member B] | [ID] | Q3, Q4 | [Task] |
| [Member C, if any] | [ID] | Q5, Q6 | [Task] |

## Dataset
- Topic and unit of observation: [TODO]
- Original author / organization: [TODO]
- URL and publication date: [TODO]
- License and attribution conditions: [TODO]
- Collection method, time period, population, limitations: [TODO]
- Raw files: [TODO: file names and download instructions]
- Related public notebooks / work and how our questions differ: [TODO]

## Research questions
See [docs/question_plan.md](docs/question_plan.md).

## Reproduce
1. Install Miniconda / Conda.
2. At repository root, create and activate environment:
   ```bash
   conda env create -f environment.yml
   conda activate p4ds-final
   jupyter lab
   ```
3. Download raw data from the URL above and place in `data/raw/` (do not commit large files).
4. Run notebooks in order:
   - `notebooks/01_collection_exploration.ipynb`
   - `notebooks/02_analysis.ipynb`
   - `notebooks/03_ml_question.ipynb`
5. Update this section with exact file names, steps and dependencies once real data is chosen.

## Key findings
- [Fill with verified findings, numbers, and limitations after analysis]

## Project notes
- Raw data must remain unchanged.
- Shared processed data should document cleaning decisions.
- For every filtering, merging or dropping operation report row count before/after and explain why.
- Use `LLM_USAGE.md` for significant AI assistance. Each member must understand submitted code and analysis.
