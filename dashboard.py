"""UK Online Retail Sales & Inventory dashboard — real UCI data.

Builds one 1600x1000 dashboard.png from data/online_retail.csv.
Design: emerald + warm neutrals, KPI sidebar layout. Run: python dashboard.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib.ticker as mtick
import pandas as pd
import textwrap

DATA = "data/online_retail.csv"
NON_PRODUCTS = {"Manual", "DOTCOM POSTAGE", "POSTAGE", "AMAZON FEE"}

BG, EMERALD, EMERALD_D, MINT, AMBER, SLATE, TEAL2 = (
    "#F7F5F0", "#047857", "#065F46", "#D1FAE5", "#D97706", "#4A5568", "#0E9F8A")

df = pd.read_csv(DATA, dtype={"Invoice": "str", "StockCode": "str",
                              "Description": "str", "Country": "str"})
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
df = df.dropna(subset=["InvoiceDate"])
df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)
df["Weekday"] = df["InvoiceDate"].dt.dayofweek
df["Hour"] = df["InvoiceDate"].dt.hour

revenue = df["LineTotal"].sum()
n_orders = df["Invoice"].nunique()
n_customers = df["Customer ID"].nunique()
n_countries = df["Country"].nunique()

fig = plt.figure(figsize=(16, 10), facecolor=BG)
gs = fig.add_gridspec(3, 4, height_ratios=[1, 1, 1], hspace=0.55, wspace=0.6,
                      left=0.05, right=0.97, top=0.92, bottom=0.07,
                      width_ratios=[0.85, 1, 1, 1])

# ---- KPI sidebar ----
sax = fig.add_subplot(gs[:, 0]); sax.set_xlim(0, 1); sax.set_ylim(0, 1); sax.axis("off")
sax.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.01,rounding_size=0.05",
                             facecolor=EMERALD_D, edgecolor="none", transform=sax.transAxes))
sax.text(0.5, 0.95, "UK ONLINE RETAIL", ha="center", va="center", fontsize=11,
         weight="bold", color=MINT, transform=sax.transAxes)
sax.text(0.5, 0.915, "Sales & Inventory", ha="center", va="center", fontsize=10,
         color="white", alpha=0.85, transform=sax.transAxes)
for i, (val, label) in enumerate([(f"£{revenue:,.0f}", "TOTAL REVENUE"),
                                  (f"{n_orders:,}", "ORDERS"),
                                  (f"{n_customers:,}", "CUSTOMERS"),
                                  (f"{n_countries}", "COUNTRIES")]):
    y = 0.80 - i * 0.19
    sax.add_patch(FancyBboxPatch((0.07, y - 0.155), 0.86, 0.15,
                                 boxstyle="round,pad=0.008,rounding_size=0.06",
                                 facecolor="white", edgecolor="none", alpha=0.14, transform=sax.transAxes))
    sax.text(0.5, y - 0.045, val, ha="center", va="center", fontsize=16.5, fontweight="bold",
             color="white", transform=sax.transAxes)
    sax.text(0.5, y - 0.115, label, ha="center", va="center", fontsize=9, weight="bold",
             color=MINT, transform=sax.transAxes)
sax.text(0.5, 0.035, "Dec 2009 – Dec 2010\n150k sampled transactions", ha="center", va="center",
         fontsize=8.5, color="white", alpha=0.75, transform=sax.transAxes)

def style(ax):
    ax.set_facecolor("white")
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    for s in ("left", "bottom"): ax.spines[s].set_color("#E3DCCF")
    ax.grid(axis="y", alpha=0.25, linestyle="--"); ax.tick_params(colors=SLATE, labelsize=9)

# ---- Monthly trend ----
ax = fig.add_subplot(gs[0, 1:4]); style(ax)
mrev = df.groupby("Month")["LineTotal"].sum()
ax.fill_between(mrev.index, mrev.values, alpha=0.18, color=EMERALD)
ax.plot(mrev.index, mrev.values, color=EMERALD, lw=2.5, marker="o", ms=5,
        markerfacecolor=AMBER, markeredgecolor=EMERALD)
peak = mrev.idxmax()
ax.annotate(f"Peak {peak}\n£{mrev.max():,.0f}", xy=(peak, mrev.max()),
            xytext=(0.72, 0.78), textcoords="axes fraction", fontsize=9, color=EMERALD_D, weight="bold",
            arrowprops=dict(arrowstyle="->", color=EMERALD_D),
            bbox=dict(facecolor="white", edgecolor="#E3DCCF", boxstyle="round,pad=0.3"))
ax.set_title("Monthly revenue trend", loc="left", fontsize=12, fontweight="bold", color=EMERALD_D, pad=10)
ax.set_ylabel("Revenue (£)", color=SLATE)
plt.setp(ax.get_xticklabels(), rotation=40, ha="right", fontsize=8)

# ---- Top countries ----
ax = fig.add_subplot(gs[1, 1:2]); style(ax)
cty = df[df["Country"] != "United Kingdom"].groupby("Country")["LineTotal"].sum().nlargest(8).sort_values()
bars = ax.barh(cty.index, cty.values, color=TEAL2, height=0.6)
bars[-1].set_color(EMERALD)
ax.set_title("Top countries by revenue (excl. UK)", loc="left", fontsize=12, fontweight="bold", color=EMERALD_D, pad=10)
ax.set_xlabel("Revenue (£)", color=SLATE); ax.tick_params(labelsize=8.5)
ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f"£{v/1000:.0f}k"))

# ---- Top products ----
ax = fig.add_subplot(gs[1, 2:4]); style(ax)
top_prd = (df[~df["Description"].isin(NON_PRODUCTS)]
           .groupby("Description")["LineTotal"].sum().nlargest(10).sort_values())
labels = [p[:26] for p in top_prd.index]
bars = ax.barh(labels, top_prd.values, color=EMERALD, height=0.62)
bars[-1].set_color(AMBER)
ax.set_title("Top 10 products by revenue", loc="left", fontsize=12, fontweight="bold", color=EMERALD_D, pad=10)
ax.set_xlabel("Revenue (£)", color=SLATE); ax.tick_params(labelsize=7)
ax.set_xlim(0, top_prd.values.max() * 1.04)
ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f"£{v/1000:.0f}k"))

# ---- Weekday x hour heatmap ----
ax = fig.add_subplot(gs[2, 1:3])
heat = df.groupby(["Weekday", "Hour"])["Invoice"].nunique().unstack(fill_value=0)
im = ax.imshow(heat.values, aspect="auto", cmap="YlGn")
ax.set_facecolor(BG)
ax.set_title("Orders by weekday × hour", loc="left", fontsize=12, fontweight="bold", color=EMERALD_D, pad=10)
ax.set_xticks(range(0, 24, 3)); ax.set_xticklabels(range(0, 24, 3), fontsize=8, color=SLATE)
ax.set_yticks(range(7)); ax.set_yticklabels(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                                            fontsize=8.5, color=SLATE)
ax.set_xlabel("Hour of day", color=SLATE)
cb = plt.colorbar(im, ax=ax, shrink=0.85); cb.set_label("Orders", color=SLATE); cb.ax.tick_params(colors=SLATE)

# ---- Revenue per order ----
ax = fig.add_subplot(gs[2, 3:4]); style(ax)
order_rev = df.groupby("Invoice")["LineTotal"].sum()
ax.hist(order_rev.values, bins=50, range=(0, 500), color=AMBER, edgecolor="white", linewidth=0.4)
ax.axvline(order_rev.median(), color=EMERALD_D, lw=2, ls="--", label=f"Median £{order_rev.median():.0f}")
ax.set_title("Revenue per order (≤ £500)", loc="left", fontsize=12, fontweight="bold", color=EMERALD_D, pad=10)
ax.set_xlabel("Order revenue (£)", color=SLATE); ax.set_ylabel("Orders", color=SLATE)
ax.legend(fontsize=8.5, frameon=False)

fig.text(0.62, 0.015, "Source: UCI Online Retail dataset (Dr Daqing Chen), CC BY 4.0 — real UK gift-retailer transactions",
         ha="center", fontsize=8, color=SLATE)
fig.savefig("dashboard.png", dpi=100, facecolor=BG)
print("saved dashboard.png", df.shape, f"revenue=£{revenue:,.0f}")
