"""CodeAlpha Data Analytics Internship - Task 3: Data Visualization

Turns the scraped book catalogue into a dashboard and a set of stand-alone charts
that tell one story: where the value in the catalogue sits and what customers rate.

Usage:
    python visualize.py                  # data/books.csv, else data/sample_books.csv
    python visualize.py path/to/books.csv
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

BASE = Path(__file__).parent
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

INK, MUTED, TEAL, BLUE, ORANGE = "#1d3557", "#6c757d", "#2a9d8f", "#457b9d", "#e76f51"
sns.set_theme(style="whitegrid", rc={
    "axes.edgecolor": "#dee2e6", "axes.titleweight": "bold", "axes.titlesize": 12,
    "axes.titlecolor": INK, "axes.spines.top": False, "axes.spines.right": False,
})

arg = Path(sys.argv[1]) if len(sys.argv) > 1 else None
path = arg or next(p for p in [BASE / "data" / "books.csv", BASE / "data" / "sample_books.csv"] if p.exists())
df = pd.read_csv(path)
df["price_band"] = pd.cut(df["price_gbp"], [0, 20, 30, 40, 50, 100], labels=["<£20", "£20-30", "£30-40", "£40-50", "£50+"])

# ---------------------------------------------------------- aggregates ---
cat = df.groupby("category").agg(books=("title", "count"), value=("price_gbp", "sum"),
                                 avg_price=("price_gbp", "mean"), avg_rating=("rating", "mean"))
top_value = cat.sort_values("value", ascending=False).head(10)
share_top3 = top_value["value"].head(3).sum() / cat["value"].sum()
good = (df["rating"] >= 4).mean()
kpis = [("Books", f"{len(df):,}"), ("Categories", f"{df['category'].nunique()}"),
        ("Avg price", f"£{df['price_gbp'].mean():.2f}"), ("Avg rating", f"{df['rating'].mean():.2f} ★"),
        ("Rated 4-5★", f"{good:.0%}")]


# --------------------------------------------------------- chart makers ---
def c_value(ax):
    d = top_value.iloc[::-1]
    ax.barh(d.index, d["value"], color=BLUE)
    for i, v in enumerate(d["value"]):
        ax.text(v, i, f" £{v:,.0f}", va="center", fontsize=8, color=MUTED)
    ax.set(title=f"Top 3 categories hold {share_top3:.0%} of catalogue value", xlabel="Total list price (£)", ylabel="")
    ax.set_xlim(0, d["value"].max() * 1.18)


def c_price_rating(ax):
    sns.boxplot(data=df, x="rating", y="price_gbp", color="#a8dadc", fliersize=2, ax=ax)
    rho = df["price_gbp"].corr(df["rating"], method="spearman")
    title = ("Price barely moves with rating" if abs(rho) < 0.1
             else f"Higher-rated books tend to cost {'more' if rho > 0 else 'less'}")
    ax.set(title=title, xlabel="Rating (stars)", ylabel="Price (£)")


def c_band(ax):
    t = pd.crosstab(df["rating"], df["price_band"])
    sns.heatmap(t, annot=True, fmt="d", cmap="GnBu", cbar=False, ax=ax)
    ax.set(title="Books by rating and price band", xlabel="Price band", ylabel="Rating")


def c_bubble(ax):
    big = cat[cat["books"] >= 10]
    ax.scatter(big["avg_price"], big["avg_rating"], s=big["books"] * 6, color=TEAL, alpha=0.55, edgecolor="white")
    for name, r in big.nlargest(5, "books").iterrows():
        ax.annotate(name, (r["avg_price"], r["avg_rating"]), fontsize=8, color=INK, xytext=(5, 5), textcoords="offset points")
    ax.set(title="Category map: price vs rating (bubble = book count)", xlabel="Average price (£)", ylabel="Average rating")


def c_hist(ax):
    sns.histplot(df["price_gbp"], bins=25, color=ORANGE, ax=ax)
    ax.axvline(df["price_gbp"].median(), color=INK, ls="--", lw=1)
    ax.text(df["price_gbp"].median(), ax.get_ylim()[1] * 0.92, f" median £{df['price_gbp'].median():.0f}", color=INK, fontsize=9)
    ax.set(title=f"Prices run £{df['price_gbp'].min():.0f} to £{df['price_gbp'].max():.0f}", xlabel="Price (£)", ylabel="Books")


charts = {"1_value_by_category": c_value, "2_price_by_rating": c_price_rating,
          "3_rating_price_band_heatmap": c_band, "4_category_bubble": c_bubble, "5_price_histogram": c_hist}

# stand-alone charts
for name, fn in charts.items():
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fn(ax)
    fig.tight_layout()
    fig.savefig(OUT / f"{name}.png", dpi=150)
    plt.close(fig)

# --------------------------------------------------------------- dashboard
fig = plt.figure(figsize=(16, 11), facecolor="white")
gs = fig.add_gridspec(3, 10, height_ratios=[0.45, 3, 3], hspace=0.5, wspace=1.2,
                      top=0.91, bottom=0.09, left=0.06, right=0.98)
fig.suptitle("Book Catalogue Dashboard", x=0.06, y=0.97, ha="left", fontsize=20, fontweight="bold", color=INK)
for i, (label, val) in enumerate(kpis):
    ax = fig.add_subplot(gs[0, i * 2:i * 2 + 2])
    ax.axis("off")
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes, color="#f1f5f9"))
    ax.text(0.5, 0.58, val, ha="center", va="center", fontsize=18, fontweight="bold", color=INK, transform=ax.transAxes)
    ax.text(0.5, 0.18, label, ha="center", va="center", fontsize=9, color=MUTED, transform=ax.transAxes)
panels = [(gs[1, 0:5], c_value), (gs[1, 5:10], c_bubble), (gs[2, 0:3], c_price_rating),
          (gs[2, 3:7], c_band), (gs[2, 7:10], c_hist)]
for spec, fn in panels:
    fn(fig.add_subplot(spec))
note = ("SYNTHETIC SAMPLE DATA - re-run on the real scrape" if "sample" in path.name
        else "books scraped from books.toscrape.com")
fig.text(0.06, 0.005, f"Source: {path.name} ({len(df):,} books, {note})", fontsize=8,
         color=ORANGE if "sample" in path.name else MUTED)
fig.savefig(OUT / "dashboard.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# --------------------------------------------------------------- insights
text = f"""# Key insights
- The 3 biggest categories hold {share_top3:.0%} of the catalogue's total list value.
- {good:.0%} of books are rated 4-5 stars; mean rating is {df['rating'].mean():.2f}.
- Median price £{df['price_gbp'].median():.2f}; priciest category on average: {cat['avg_price'].idxmax()} (£{cat['avg_price'].max():.2f}).
- Correlation between price and rating: {df['price_gbp'].corr(df['rating'], method='spearman'):.2f} (Spearman).
"""
(OUT / "insights.md").write_text(text, encoding="utf-8")
print(text)
print(f"Saved dashboard and {len(charts)} charts to {OUT}")
