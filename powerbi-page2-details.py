# ============================================================
# Power BI Python visual — PAGE 2: Details
# صفحة 2: التفاصيل — UK Online Retail Sales & Inventory
# ------------------------------------------------------------
# HOW TO USE / طريقة الاستخدام:
#  1) Get Data → load data/online_retail.csv (نفس الجدول)
#  2) Insert → Python visual (صفحة جديدة اسمها "Details")
#  3) Drag these EXACT 4 columns into the visual's Values well /
#     اسحب هذه الأعمدة الأربعة بالضبط إلى خانة Values:
#        - Invoice
#        - InvoiceDate
#        - LineTotal
#        - Description
#  4) Paste this entire script / الصق هذا السكربت كاملاً
#
# Uses ONLY the `dataset` DataFrame injected by Power BI.
# No file loading, no plt.show() — Power BI renders the figure.
# Design: emerald + warm neutrals.
# ============================================================
import matplotlib.pyplot as plt
import pandas as pd

REQUIRED = ["Invoice", "InvoiceDate", "LineTotal", "Description"]
missing = [c for c in REQUIRED if c not in dataset.columns]
if missing:
    raise ValueError("Missing columns — drag into Values: " + ", ".join(missing))

NON_PRODUCTS = {"Manual", "DOTCOM POSTAGE", "POSTAGE", "AMAZON FEE"}
df = dataset.copy()
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
df = df.dropna(subset=["InvoiceDate"])
df["Weekday"] = df["InvoiceDate"].dt.dayofweek
df["Hour"] = df["InvoiceDate"].dt.hour

BG, EMERALD, EMERALD_D, AMBER, SLATE = "#F7F5F0", "#047857", "#065F46", "#D97706", "#4A5568"

fig = plt.figure(figsize=(13, 8), facecolor=BG)
gs = fig.add_gridspec(2, 2, hspace=0.55, wspace=0.4, left=0.09, right=0.95, top=0.88, bottom=0.1)
fig.text(0.09, 0.95, "DETAILS  •  UK ONLINE RETAIL", fontsize=11, color=EMERALD_D, weight="bold", va="center")

def style(ax):
    ax.set_facecolor("white")
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    for s in ("left", "bottom"): ax.spines[s].set_color("#E3DCCF")
    ax.grid(axis="y", alpha=0.25, linestyle="--"); ax.tick_params(colors=SLATE, labelsize=9)

ax = fig.add_subplot(gs[0, :]); style(ax)
top_prd = (df[~df["Description"].isin(NON_PRODUCTS)]
           .groupby("Description")["LineTotal"].sum().nlargest(10).sort_values())
bars = ax.barh([p[:30] for p in top_prd.index], top_prd.values, color=EMERALD, height=0.6)
bars[-1].set_color(AMBER)
ax.set_title("Top 10 products by revenue", loc="left", fontsize=12, fontweight="bold", color=EMERALD_D, pad=8)
ax.set_xlabel("Revenue (£)", color=SLATE); ax.tick_params(labelsize=8)

ax = fig.add_subplot(gs[1, 0])
heat = df.groupby(["Weekday", "Hour"])["Invoice"].nunique().unstack(fill_value=0)
im = ax.imshow(heat.values, aspect="auto", cmap="YlGn")
ax.set_facecolor(BG)
ax.set_title("Orders by weekday × hour", loc="left", fontsize=12, fontweight="bold", color=EMERALD_D, pad=8)
ax.set_xticks(range(0, 24, 4)); ax.set_xticklabels(range(0, 24, 4), fontsize=8, color=SLATE)
ax.set_yticks(range(7))
ax.set_yticklabels(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], fontsize=8.5, color=SLATE)
ax.set_xlabel("Hour of day", color=SLATE)
plt.colorbar(im, ax=ax, shrink=0.85, label="Orders")

ax = fig.add_subplot(gs[1, 1]); style(ax)
order_rev = df.groupby("Invoice")["LineTotal"].sum()
ax.hist(order_rev.values, bins=50, range=(0, 500), color=AMBER, edgecolor="white", linewidth=0.4)
ax.axvline(order_rev.median(), color=EMERALD_D, lw=2, ls="--", label=f"Median £{order_rev.median():.0f}")
ax.set_title("Revenue per order (≤ £500)", loc="left", fontsize=12, fontweight="bold", color=EMERALD_D, pad=8)
ax.set_xlabel("Order revenue (£)", color=SLATE); ax.set_ylabel("Orders", color=SLATE)
ax.legend(fontsize=9, frameon=False)
