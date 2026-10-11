# [Your question as a plain title]

[The finding in two or three sentences, with the main numbers and what
they mean for the person who would act on it.]

![Chart title that states the finding](output/main_chart.png)

## Data
- **Dataset:** [name], [publisher]
- **Link:** [address]
- **Period covered:** [from - to]
- **Downloaded:** [date]
- **Licence:** [licence, and the credit line the publisher asks for]

## Approach
- [Key cleaning decision, with counts: what you removed or kept, and why]
- [How you defined the main measure]
- [Main method: comparison, test or model]
- [Anything you joined, and from where]

## Limitations
- [A limit that could change the conclusion]
- [A second one]
- [A third, if it matters]

## Rerun it
```
pip install -r requirements.txt
python src/get_data.py      # downloads the data
python src/analysis.py      # rebuilds the outputs
```

## Repository layout
- `data/` download script (raw data is not stored here)
- `src/` cleaning and analysis code
- `notebooks/` the analysis, step by step
- `output/` charts and tables
