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
Based on 1,000 books across 50 categories scraped from books.toscrape.com:

- Value is concentrated: the 3 biggest categories hold 33% of the catalogue's total list value.
- Ratings are middling: the mean rating is 2.92 stars and only 38% of books are rated 4-5 stars.
- The median price is £35.98. Suspense has the highest average price (£58.33), but it is a tiny category (one book), so this is not a reliable pattern.
- Price and rating are essentially unrelated (Spearman correlation 0.03): expensive books are not rated higher.
- Takeaway: a few large categories drive the catalogue's value, and price alone says nothing about quality.
