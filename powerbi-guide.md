# دليل بناء الداشبورد في Power BI خطوة بخطوة 🇸🇦

هذا الدليل يخليك تبني نفس الداشبورد الموجود في ملف **dashboard.png** (هو المرجع البصري — افتحه جنبك وأنت تشتغل) باستخدام **Power BI Desktop** على لابتوبك خلال ~15 دقيقة.

البيانات الحقيقية موجودة في: `data/online_retail.csv`

أعمدة الملف الفعلية (احفظ أسماءها زي ما هي):
`Invoice` · `StockCode` · `Description` · `Quantity` · `InvoiceDate` · `Price` · `Customer ID` · `Country` · `LineTotal`

> **المتطلب المسبق:** ثبّت Python على جهازك مع مكتبتي `pandas` و `matplotlib`
> (`pip install pandas matplotlib`)، وفعّله في Power BI من
> **File ← Options and settings ← Options ← Python scripting**.

## الطريق الأسرع: فيجوال بايثون (صفحتين جاهزتين)

### الصفحة 1 — نظرة عامة (Overview)
1. **Get Data** ← حمّل `data/online_retail.csv`.
2. أنشئ صفحة جديدة وسمّها **Overview**، ومن **Insert** أضف **Python visual**.
3. اسحب إلى خانة **Values** هذه الأعمدة الخمسة بالضبط:
   `Invoice` ← `InvoiceDate` ← `LineTotal` ← `Country` ← `Customer ID`.
4. الصق كامل محتوى الملف `powerbi-page1-overview.py` ← اضغط Run.

### الصفحة 2 — التفاصيل (Details)
1. أنشئ صفحة ثانية وسمّها **Details**، وأضف **Python visual** جديد.
2. اسحب إلى خانة **Values** هذه الأعمدة الأربعة بالضبط:
   `Invoice` ← `InvoiceDate` ← `LineTotal` ← `Description`.
3. الصق كامل محتوى الملف `powerbi-page2-details.py` ← اضغط Run.

### إضافة Slicers (فلاتر تفاعلية)
أضف Slicers عادية وستُرشّح فيجوال بايثون تلقائياً:
- **Slicer** ← `Country` | **Slicer** ← `InvoiceDate` (نطاق تاريخ).

> **ملاحظة صادقة:** الـ Slicers **تُرشّح** فيجوال بايثون فعلاً — الصفوف المفلترة هي اللي توصل
> لمتغير `dataset` داخل السكربت. لكن فيجوال بايثون **لا يستقبل** التظليل التفاعلي (highlight)
> من الضغط على رسوم بيانية ثانية.

---
## الطريق الثاني: بناء يدوي بمقاييس DAX (اختياري)

---

## ١) تحميل البيانات (Get Data)

1. افتح Power BI Desktop ← **Get Data** ← **Text/CSV**.
2. اختر ملف `data/online_retail.csv` ← **Load**.
3. بيطلع لك جدول واحد اسمه `online_retail` — هذا هو كل اللي تحتاجه.

## ٢) نموذج البيانات (Data Model)

- **ما تحتاج أي علاقات (Relationships)** — الداشبورد كله مبني على جدول واحد `online_retail`.
- ملاحظة: عمود `Customer ID` فيه مسافة، ففي لغة DAX لازم تكتبه بين قوسين مربعين زي ما هو: `'online_retail'[Customer ID]`.

## ٣) أعمدة مساعدة (Calculated Columns)

روح على **Data view** ← اختر جدول `online_retail` ← **New column** وأضف هالأعمدة (انسخ والصق):

```DAX
Month = FORMAT('online_retail'[InvoiceDate], "yyyy-MM")
```

```DAX
WeekdayNum = WEEKDAY('online_retail'[InvoiceDate], 2)
```

```DAX
WeekdayName =
SWITCH(
    'online_retail'[WeekdayNum],
    1, "Monday", 2, "Tuesday", 3, "Wednesday",
    4, "Thursday", 5, "Friday", 6, "Saturday", 7, "Sunday"
)
```

```DAX
Hour = HOUR('online_retail'[InvoiceDate])
```

> رتّب عمود `WeekdayName` حسب `WeekdayNum`: حدّد العمود ← **Sort by column** ← `WeekdayNum`.

## ٤) مقاييس DAX (انسخ والصق كما هي)

روح على **Data view** ← **New measure** وأضف هالأربعة (هي نفس أرقام الـ KPI في الداشبورد):

```DAX
Total Revenue = SUM('online_retail'[LineTotal])
```

```DAX
Orders = DISTINCTCOUNT('online_retail'[Invoice])
```

```DAX
Customers = DISTINCTCOUNT('online_retail'[Customer ID])
```

```DAX
Countries = DISTINCTCOUNT('online_retail'[Country])
```

تحقق سريع: `Total Revenue` لازم يطلع **£3,077,973** و `Orders` = **18,216** و `Customers` = **4,145** و `Countries` = **40**. لو طلعت هالأرقام، بياناتك سليمة ✅

## ٥) بناء الصفحة — الفيجوالز (Visuals)

رتّب الصفحة زي `dashboard.png`: صف KPIs فوق، ثم صفّين من الرسوم.

### صف الـ KPI (٤ بطاقات)
- أضف ٤ فيجوالز من نوع **Card**.
- كل بطاقة: ضع في خانة **Fields** مقياس واحد: `Total Revenue` / `Orders` / `Customers` / `Countries`.

### ١. Monthly Revenue Trend — رسم خطي
- الفيجوال: **Line chart**
- **X-axis** ← `Month` · **Y-axis** ← `Total Revenue`
- تنسيق: سمّك الخط وفعّل **Markers** من Format.

### ٢. Top Countries by Revenue (بدون بريطانيا) — أعمدة أفقية
- الفيجوال: **Bar chart** (أفقي)
- **Y-axis** ← `Country` · **X-axis** ← `Total Revenue`
- الفلاتر: **Filters on this visual** ← `Country` ← أزل `United Kingdom`
- **Top N**: فعّل Top N = 10 حسب `Total Revenue`.

### ٣. Top 10 Products by Revenue — أعمدة أفقية
- الفيجوال: **Bar chart**
- **Y-axis** ← `Description` · **X-axis** ← `Total Revenue`
- الفلاتر: استبعد هالقيم من `Description` (سطور داخلية مو منتجات حقيقية):
  `Manual` · `DOTCOM POSTAGE` · `POSTAGE` · `AMAZON FEE`
- **Top N** = 10 حسب `Total Revenue`.

### ٤. Orders by Weekday × Hour — خريطة حرارية (Heatmap)
- الفيجوال: **Matrix**
- **Rows** ← `WeekdayName` · **Columns** ← `Hour` · **Values** ← `Orders`
- من **Format** ← **Cell elements** ← فعّل **Background color** ← اختر تدرج أزرق/أخضر.
- رتّب الصفوف: تأكد أن `WeekdayName` مرتب حسب `WeekdayNum` (خطوة ٣).

### ٥. Revenue Distribution per Order — هستوجرام
- أول شي أنشئ جدول ملخص (عشان الإيراد على مستوى الطلب مو السطر): **Modeling** ← **New table** والصق:

```DAX
OrderRevenue =
SUMMARIZE(
    'online_retail',
    'online_retail'[Invoice],
    "Revenue", SUM('online_retail'[LineTotal])
)
```

- الفيجوال: **Column chart**
- **X-axis** ← عمود `Revenue` من جدول `OrderRevenue` ← كليك يمين عليه ← **New group** ← نوع **Bin** ← حجم الـ Bin = **10**.
- **Y-axis** ← Count of `Invoice` (عدد الطلبات).
- خط الوسيط: من **Analytics pane** ← **Constant line** ← القيمة **89**.

### إضافات اختيارية (Slicers)
- أضف **Slicer** لعمود `Country` وآخر لـ `Month` فوق الصفحة — يخلي الداشبورد تفاعلي.

## ٦) خطوات التنظيف في Power Query (لو حملت الملف الخام)

ملف `data/online_retail.csv` **جاهز ونظيف** — هالخطوات بس لو رجعت للملف الخام `online_retail_II.csv` (٥٢٥ ألف صف):

1. **Transform Data** ← حدد نوع الأعمدة: `InvoiceDate` ← Date/Time، و `Quantity` و `Price` أرقام.
2. احذف الصفوف اللي `Description` فيها فاضي (Filter ← Remove Empty).
3. احذف المرتجعات: فلتر عمود `Invoice` ← **Text Filters** ← **Does Not Begin With** ← `C`.
4. احذف الصفوف اللي `Quantity <= 0` أو `Price <= 0` (Number Filters ← Greater Than ← 0).
5. أضف عمود مخصص: **Add Column** ← **Custom Column** ← الاسم `LineTotal` ← الصيغة:

```
[Quantity] * [Price]
```

6. **Close & Apply**.

---

بالتوفيق يا وليد! أي رقم ما طابق الأرقام اللي فوق، راجع خطوة الفلاتر — غالبًا نسيت تستبعد بريطانيا أو سطور الـ Manual 💪
