# ============================================================
# Power BI Python visual — PAGE 1: Overview
# صفحة 1: نظرة عامة — UK Online Retail Sales & Inventory
# ------------------------------------------------------------
# HOW TO USE / طريقة الاستخدام:
#  1) Get Data → load data/online_retail.csv
#  2) Insert → Python visual (صفحة جديدة اسمها "Overview")
#  3) Drag these EXACT 5 columns into the visual's Values well /
#     اسحب هذه الأعمدة الخمسة بالضبط إلى خانة Values:
#        - Invoice
#        - InvoiceDate
#        - LineTotal
#        - Country
#        - Customer ID
#  4) Paste this entire script / الصق هذا السكربت كاملاً
#
# Uses ONLY the `dataset` DataFrame injected by Power BI.
# No file loading, no plt.show() — Power BI renders the figure.
# Design: emerald + warm neutrals.
# ============================================================
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import pandas as pd

REQUIRED = ["Invoice", "InvoiceDate", "LineTotal", "Country", "Customer ID"]
missing = [c for c in REQUIRED if c not in dataset.columns]
if missing:
    raise ValueError("Missing columns — drag into Values: " + ", ".join(missing))

df = dataset.copy()
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
df = df.dropna(subset=["InvoiceDate"])
df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)

revenue = df["LineTotal"].sum()
n_orders = df["Invoice"].nunique()
n_customers = df["Customer ID"].nunique()
n_countries = df["Country"].nunique()

BG, EMERALD, EMERALD_D, MINT, AMBER, SLATE = "#F7F5F0", "#047857", "#065F46", "#D1FAE5", "#D97706", "#4A5568"

fig = plt.figure(figsize=(13, 8), facecolor=BG)
gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.15], hspace=0.5, wspace=0.35,
                      left=0.07, right=0.96, top=0.88, bottom=0.1)
fig.text(0.07, 0.95, "OVERVIEW  •  UK ONLINE RETAIL", fontsize=11, color=EMERALD_D, weight="bold", va="center")

def kpi_card(pos, label, value):
    ax = fig.add_subplot(pos); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.01, 0.04), 0.98, 0.92, boxstyle="round,pad=0.015,rounding_size=0.09",
                                facecolor=EMERALD_D, edgecolor="none", transform=ax.transAxes))
    ax.text(0.5, 0.60, value, ha="center", va="center", fontsize=17, fontweight="bold",
            color="white", transform=ax.transAxes)
    ax.text(0.5, 0.30, label, ha="center", va="center", fontsize=9, weight="bold",
            color=MINT, transform=ax.transAxes)

def style(ax):
    ax.set_facecolor("white")
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    for s in ("left", "bottom"): ax.spines[s].set_color("#E3DCCF")
    ax.grid(axis="y", alpha=0.25, linestyle="--"); ax.tick_params(colors=SLATE, labelsize=9)

kpi_card(gs[0, 0], "TOTAL REVENUE", f"£{revenue:,.0f}")
kpi_card(gs[0, 1], "ORDERS", f"{n_orders:,}")

ax = fig.add_subplot(gs[1, 0:2]); style(ax)
mrev = df.groupby("Month")["LineTotal"].sum()
ax.fill_between(mrev.index, mrev.values, alpha=0.18, color=EMERALD)
ax.plot(mrev.index, mrev.values, color=EMERALD, lw=2.5, marker="o", ms=5,
        markerfacecolor=AMBER, markeredgecolor=EMERALD)
ax.set_title("Monthly revenue trend", loc="left", fontsize=12, fontweight="bold", color=EMERALD_D, pad=8)
ax.set_ylabel("Revenue (£)", color=SLATE)
plt.setp(ax.get_xticklabels(), rotation=40, ha="right", fontsize=8)

# second KPI row inside overview: customers + countries as text cards
fig.text(0.28, 0.52, f"{n_customers:,}  customers   •   {n_countries}  countries",
         ha="center", fontsize=11, color=EMERALD_D, weight="bold",
         bbox=dict(facecolor="white", edgecolor="#E3DCCF", boxstyle="round,pad=0.4"))
