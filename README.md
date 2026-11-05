# CodeAlpha_DataVisualization

Task 3 of the CodeAlpha Data Analytics Internship: turn raw data into clear visuals
that support a decision.

## The story
Using the book catalogue scraped in `CodeAlpha_WebScraping`: **where does the value in
the catalogue sit, and does price relate to how customers rate books?**

## Dashboard
`outputs/dashboard.png` combines five KPIs with five charts:
1. Total list value by category (concentration of the catalogue)
2. Category map: average price vs average rating, bubble size = book count
3. Price by rating (boxplot)
4. Books by rating and price band (heatmap)
5. Price distribution with the median marked

Each chart is also saved on its own (`outputs/1_...` to `5_...`) and `outputs/insights.md`
lists the key numbers. Chart titles are generated from the data, so they stay true when the
dataset changes.

## Design choices
- One colour family plus a single accent, so colour carries meaning.
- Titles state the takeaway, not just the topic.
- Direct value labels on bars, minimal gridlines, no chart junk.

## Run
```bash
pip install -r requirements.txt
python visualize.py        # uses data/books.csv, falls back to data/sample_books.csv
```

## Findings
**Fill in from `outputs/insights.md` after running on the real scraped data.**
The bundled `sample_books.csv` is synthetic, so its numbers are not real results.
