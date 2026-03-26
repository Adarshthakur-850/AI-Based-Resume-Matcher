# AI-Based Resume Matcher

An automated tool to rank resumes against a job description using NLP and Machine Learning.

## Features
- **Resume Parsing**: Supports PDF, DOCX, and TXT.
- **NLP Analysis**: Extracts skills and experience using SpaCy.
- **Semantic Matching**: Uses Sentence-Transformers for context-aware comparison.
- **Ranking**: Weighted scoring based on similarity, skills, and experience.
- **Reporting**: Generates CSV reports and visualization plots.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

2. Prepare Data:
   - Place resumes in `data/resumes/`
   - Update `data/job_description.txt`

3. Run:
   ```bash
   python main.py
   ```

## Output
Results are saved in `output/` folder:
- `ranking.csv`
- `ranking_plot.png`
