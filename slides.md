# Data management workshop

* Examine common data managment pitfalls
* Provide alternative way to manage data
* Transform a project one piece at a time

---

# Our project

A workflow of 4 stages.

## 1. Construct cages from precursors and topologies.

We have a collection of 5 tri-amines and 5 di-aldehydes precursors and 3
topologies. We construct cages for every combination of precursors and
topologies, giving a total of 75 cages.

| Amines | Aldehydes | Topologies |
| ------ | ------ | ------ |
| Nc1nc(N)nc(N)n1 | O=Cc1cccc(C=O)c1 | 4 + 6
 Cc1c(CN)c(C)c(CN)c(C)c1CN | CC(C)(C)c1cc(C=O)c(O)c(C=O)c1 | 8 + 12
 NCCN(CCN)CCN | O=Cc1cc2sc(C=O)cc2s1 | 20 + 30
 CCc1c(CN)c(CC)c(CN)c(CC)c1CN | O=Cc1ccc(C=O)cc1 |
 NCCCN(CCCN)CCCN | O=Cc1c(F)c(F)c(C=O)c(F)c1F |

## 2. Has a set of experimental NMR peaks for each cage.

We have a CSV file which holds the NMR peaks for each cage, giving the chemical
shift and intensity.

|index|amine|aldehyde|topology|aldehyde_peaks|aldehyde_amplitudes|imine_peaks|imine_amplitudes|aldehyde?|imine?|
|---|---|---|---|---|---|---|---|---|---|
0|Nc1nc(N)nc(N)n1|O=Cc1cccc(C=O)c1|FOUR_PLUS_SIX|"[146, 10.08704, ...]"|"[7.3406, 7.3378, ...]"|"[5798.33, 2298.025, ...]"|"[1213.123123, 14389, ...]"|true|true|

## 3. Has the computed diameters for each cage.

Which we calculate using a Python script from computationally constructed
structures.

## 4. Has a script to calculate the top peaks for each cage.

Calculated from the NMR peaks.

---

# Intial project

https://github.com/lukasturcani/data-management-workshop

```
   start
 ├─  top_peaks.py
 ├─  calc_diameters.py
 └─   data
    ├─ 󰈙 di_aldehydes.txt
    ├─ 󰈙 nmr_peaks.csv
    ├─ 󰈙 tri_amines.txt
    ├─  gen.py
    ├─   cages
    │  ├─ NCCCN(CCCN)CCCN_O=Cc1ccc(C=O)cc1_EIGHT_PLUS_TWELVE.mol
    │  ├─ Nc1nc(N)nc(N)n1_O=Cc1ccc(C=O)cc1_FOUR_PLUS_SIX.mol
    │  ├─ NCCCN(CCCN)CCCN_O=Cc1c(F)c(F)c(C=O)c(F)c1F_TWENTY_PLUS_THIRTY.mol
    │  ├─ NCCN(CCN)CCN_O=Cc1cccc(C=O)c1_FOUR_PLUS_SIX.mol
    │  └ ...
    └─   properties
       ├─ Cc1c(CN)c(C)c(CN)c(C)c1CN_O=Cc1c(F)c(F)c(C=O)c(F)c1F_TWENTY_PLUS_THIRTY.json
       ├─ Cc1c(CN)c(C)c(CN)c(C)c1CN_CC(C)(C)c1cc(C=O)c(O)c(C=O)c1_EIGHT_PLUS_TWELVE.json
       ├─ Cc1c(CN)c(C)c(CN)c(C)c1CN_O=Cc1cc2sc(C=O)cc2s1_TWENTY_PLUS_THIRTY.json
       ├─ NCCCN(CCCN)CCCN_O=Cc1cc2sc(C=O)cc2s1_EIGHT_PLUS_TWELVE.json
       └ ...
```

1. Scripts for calculating properties.
1. Data folder holding csv, JSON, precursor and cage structure files.
1. Additional script for creating cages.

## Questions

1. Does this project layout look familiar to you?
1. What are the challenges you have with this kind of layout?

---

# Initial project: Drawbacks

## No documentation of workflow

Unclear which scripts read and produce which data.

## No checks for adding, removing, editings files

Easy to open a file and edit it. Raw edits can introduce errors. Hard to
check if a file is missing or been added without writing custom scripts.

## Hard to connect all the pieces together

If I want to read CSV file and the JSON data how do I link all the data
relevant to a specific cage? I'll need to parse the file names.

## Hard to share all these files

Lots of files, to share them I'll probably have to make a tar or zip archive.
How will I explain how the data is organized to the person I send it to?

## No schema

How do I know what data I'm storing? What are the correct data types for each
CSV column? Which fields should I expect my JSON files to have?

---

# Goal

## All data in a single file

* Easy to share.
* All scripts read and write the same file without interference.
* Easy to checksum:
```bash
$ shasum end/workshop.db
5fa4370dc15731973a6dbec8c0166292c69d1564  end/workshop.db
```

## Workflow obvious from file names

In what order should we run our scripts? Can we make this super obvious to
other people?

## Checks for data validity

Can we prevent incorrect data from ever being stored? Can we avoid checks when
doing further processing?

## Well defined data schema

Can we easily understand and document what data we're storing?

## Unified interface for data access

Can people access and query our data without having having to study our
project?

---

# End project

```
  end
 ├─  01_make_db.py
 ├─  02_gen_cages.py
 ├─  03_add_nmr_peaks.py
 ├─  04_calc_diameters.py
 ├─  top_peaks.py
 ├─  workshop.db
 └─  raw_data
    └─ 󰈙 nmr_peaks.csv
```

1. `workshop.db` holds all data for the project
1. Numbered scripts create the database
1. Each numbered script adds new data into the database and may read generated by previous scripts
1. Remaining scripts for querying database

---

# Step 1: NMR Peaks

1. Examine `start/top_peaks.py`.
1. Prints cage and highest intensity NMR peaks.
1. Examine:
```python
for row in reader:
    print(row["amine"], row["aldehyde"], row["topology"])
    if not row["imine_peaks"]:
        row["imine_peaks"] = "[]"
    if not row["imine_amplitudes"]:
        row["imine_amplitudes"] = "[]"
    if not row["aldehyde_peaks"]:
        row["aldehyde_peaks"] = "[]"
    if not row["aldehyde_amplitudes"]:
        row["aldehyde_amplitudes"] = "[]"
    imine_peaks = sorted(
        get_peaks(eval(row["imine_peaks"]), eval(row["imine_amplitudes"])),
        key=lambda peak: peak.intensity,
        reverse=True,
    )
    print("imine", imine_peaks[:2])
    aldehyde_peaks = sorted(
        get_peaks(
            eval(row["aldehyde_peaks"]), eval(row["aldehyde_amplitudes"])
        ),
        key=lambda peak: peak.intensity,
        reverse=True,
    )
    print("aldehyde", aldehyde_peaks[:2])
```

## Question

What are some issues with the above code?

---

# Step 1: NMR Peaks - Issues

## Conditional checks

We have to check if a column has valid data before we use it.

## Data sanitization

If the data is invalid we have to edit it: `row["imine_peaks"] = "[]"`.

## Use of eval

Our column holds data a string. We want to access the numbers in the string.
This means we have to run eval on the string. This is bad for storage because
each digit is encoded using a separate byte. A float may easily be 12 digits
long and take up 12 digits as a result but would only be 4 bytes if encoded
directly a float.

Eval is also unsafe as it can execute arbitrary code. Lots of code quality
checks will rightfully complain that your code is bad if you use it.

## Unnecessary complexity

Our code is focusing on data sanitization, not on business logic. Worse, we
have to do this every time we want to access our data. Not so good for data
exploration!

## Complexity is due to complex data

The complexity of our code here is not due to our processing code being bad.
Our processing needs to be complex because the data we are dealing with is
complex. **Non-linear data requires nonlinear processing.**

## Data can have multiple null forms

* `,,`
* `"[]"`
* `None`

## Data hard to update, redundant columns

If we want to add a new peak, which columns do we have to update?

* Peaks
* Amplitudes
* Imine? / Aldehdye?

---

# Solution: SQL Databases

## Collections of tables

Each database is a collection of tables, you can think of it as multiple CSV
files in one.

## Each column has a type

Each column has a well defined type such as TEXT, INTEGER, REAL, DATETIME. This
ensures it is valid and removes the need for preprocessing.

## Each column can have constraints

Allows us to ensure that if the data is in the database it is valid. Prevents
the need to write runtime checks when reading and processing the data. Eg.
UNIQUE, CHECK

## Normalization

There are well established rules for how to structure your tables to prevent
errors when updating your database. These are called the normal forms.

## Performant

Reading and writing csv files line by line is slow. Querying data in those
formats is also slow and memory intensive.

## Standardized

SQL exists across many different databases (SQLite, MySQL, PostgreSQL), often
with minor variations but essentially the same.

## Widely used

It is *the* standard way to store and query data. Default in industry.

## Easy to write with AI

I don't think you need to know how to write SQL from scratch, ChatGPT can do it
well. Reading it is easy once your know the basics.


---

# SQL Databases: Setting up

```python

import sqlite3
connection = sqlite3.connect("example.db")
connection.execute("""
CREATE TABLE IF NOT EXISTS teachers (
    teacher_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    employment_type TEXT NOT NULL,
    salary REAL NOT NULL
)
""")
connection.commit()
```

---

# SQL Databases: Creating tables

## Simple

```sql
CREATE TABLE IF NOT EXISTS teachers (
    teacher_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    employment_type TEXT NOT NULL,
    salary REAL NOT NULL
)
```

## With constraints


```sql
CREATE TABLE IF NOT EXISTS teachers (
    teacher_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    employment_type TEXT NOT NULL CHECK (employment_type IN ('FULL_TIME', 'PART_TIME')),
    salary REAL NOT NULL,
    UNIQUE(first_name, last_name)
)
```

## Foreign keys

```sql
CREATE TABLE IF NOT EXISTS pets (
    pet_id INTEGER PRIMARY KEY,
    teacher_id INTEGER,
    name TEXT NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
)
```

---

# SQL Databases: Creating tables

## Exercise

Go on ChatGPT and ask it to create tables for the following scenarios

### Molecules

You have some molecules, each molecule is defined by a SMILES, a cavity
size. Molecules may fall into one of inorganic, organic or drug-like categories.
Molecules may be also be either synthesized or hypothetical.

### Peaks

You have a bunch of NMR peaks, each peak has a chemical shift and an intensity.
Peaks can either be aldehyde or imine peaks.

### Project

We have cages built from amine and aldehyde precursors and a topology. Each
cage should be a unique combination of amine, aldehyde and topology. Topologies
are limited to 4+6, 8+12, 20+30. For each cage we also want to store a cavity
size.

We have a collection of aldehyde peaks and imine peaks, each associated with a
specific cage.


---

# SQL Databases: Querying tables

* SQL:

```sql
SELECT * FROM teachers;
```

* Python:

```python
import sqlite3
connection = sqlite3.connect("example.db")
for row in connection.execute("SELECT * FROM teachers"):
    print(row)

```
```
(0, "Jane", "Doe", "FULL_TIME", 100.103)
```

---


# SQL Databases: Querying tables (Polars)

* Like pandas but better in every way.
* API is human readable, more clear, mimicks SQL,
* Faster.
* Interconvertible from pandas.

```python
import polars as pl
import sqlite3

connection = sqlite3.connect("example.db")
df = pl.read_database("SELECT * FROM teachers", connection)
```

```
shape: (1, 5)
┌────────────┬────────────┬───────────┬─────────────────┬────────┐
│ teacher_id ┆ first_name ┆ last_name ┆ employment_type ┆ salary │
│ ---        ┆ ---        ┆ ---       ┆ ---             ┆ ---    │
│ i64        ┆ str        ┆ str       ┆ str             ┆ f64    │
╞════════════╪════════════╪═══════════╪═════════════════╪════════╡
│ 1          ┆ one        ┆ two       ┆ PART_TIME       ┆ 100.0  │
└────────────┴────────────┴───────────┴─────────────────┴────────┘
```

## Exercise

Write a Python script which prints the tables in `end/workshop.db` as
Polars dataframes.

*Hint: Can any of the other files in folder help you determine the table names?*

---

# SQL Databases: 1st Normal Form

* Each column holds a single value.
* If you have multiple values in a column, create a new table.
* We can update and query each value individually.

Before:
```sql
CREATE TABLE IF NOT EXISTS cages (
    cage_id INTEGER PRIMARY KEY,
    amine TEXT NOT NULL,
    aldehyde TEXT NOT NULL,
    topology TEXT NOT NULL CHECK (topology IN ('FOUR_PLUS_SIX', 'EIGHT_PLUS_TWELVE', 'TWENTY_PLUS_THIRTY')),
    imine_peaks TEXT NOT NULL,
    UNIQUE(amine, aldehyde, topology)
)
```

After:
```sql
CREATE TABLE IF NOT EXISTS cages (
    cage_id INTEGER PRIMARY KEY,
    amine TEXT NOT NULL,
    aldehyde TEXT NOT NULL,
    topology TEXT NOT NULL CHECK (topology IN ('FOUR_PLUS_SIX', 'EIGHT_PLUS_TWELVE', 'TWENTY_PLUS_THIRTY')),
    UNIQUE(amine, aldehyde, topology)
);

CREATE TABLE IF NOT EXISTS imine_peaks (
    peak_id INTEGER PRIMARY KEY,
    cage_id INTEGER NOT NULL,
    ppm REAL NOT NULL,
    intensity REAL NOT NULL,
    FOREIGN KEY (cage_id) REFERENCES cages(cage_id)
)
```



---

# SQL Databases: Joins

Joins allows us to combine data from multiple tables.

## SQL

```sql
SELECT * FROM teachers
JOIN pets ON teachers.teacher_id = pets.teacher_id;
```

## Polars

```python
import polars as pl
import sqlite3

connection = sqlite3.connect("example.db")
teachers = pl.read_database("SELECT * FROM teachers", connection)
pets = pl.read_database("SELECT * FROM pets", connection)
df = teachers.join(pets, on="teacher_id")
```

```
shape: (3, 7)
┌────────────┬────────────┬───────────┬─────────────────┬────────┬────────┬───────┐
│ teacher_id ┆ first_name ┆ last_name ┆ employment_type ┆ salary ┆ pet_id ┆ name  │
│ ---        ┆ ---        ┆ ---       ┆ ---             ┆ ---    ┆ ---    ┆ ---   │
│ i64        ┆ str        ┆ str       ┆ str             ┆ f64    ┆ i64    ┆ str   │
╞════════════╪════════════╪═══════════╪═════════════════╪════════╪════════╪═══════╡
│ 1          ┆ one        ┆ two       ┆ PART_TIME       ┆ 100.0  ┆ 1      ┆ dog   │
│ 1          ┆ one        ┆ two       ┆ PART_TIME       ┆ 100.0  ┆ 3      ┆ mouse │
│ 2          ┆ three      ┆ four      ┆ FULL_TIME       ┆ 200.0  ┆ 2      ┆ cat   │
└────────────┴────────────┴───────────┴─────────────────┴────────┴────────┴───────┘
```

## Also

```python
import polars as pl
import sqlite3

connection = sqlite3.connect("example.db")
df = pl.read_database("""
    SELECT * FROM teachers
    JOIN pets ON teachers.teacher_id = pets.teacher_id
""", connection)
```

## Exercise

Create data frames for imine peaks and aldehyde peaks tables in
`end/workshop.db`. Join them with the cages table.

---

# SQL Databases: Grouping

What if we want to calculate the average peak intensity for each cage?

* Get the combined cages and peaks table.

```python
cages = pl.read_database("SELECT * FROM cages", connection)
imine_peaks = pl.read_database("SELECT * FROM imine_peaks", connection)
imine_peaks = cages.join(imine_peaks, on="cage_id")
```

```
shape: (1_090, 7)
┌─────────┬─────────────────┬────────────────────────────┬────────────────────┬─────────┬──────────┬───────────────┐
│ cage_id ┆ amine           ┆ aldehyde                   ┆ topology           ┆ peak_id ┆ ppm      ┆ intensity     │
│ ---     ┆ ---             ┆ ---                        ┆ ---                ┆ ---     ┆ ---      ┆ ---           │
│ i64     ┆ str             ┆ str                        ┆ str                ┆ i64     ┆ f64      ┆ f64           │
╞═════════╪═════════════════╪════════════════════════════╪════════════════════╪═════════╪══════════╪═══════════════╡
│ 1       ┆ Nc1nc(N)nc(N)n1 ┆ O=Cc1cccc(C=O)c1           ┆ FOUR_PLUS_SIX      ┆ 1       ┆ 8.258177 ┆ 405757.390625 │
│ 1       ┆ Nc1nc(N)nc(N)n1 ┆ O=Cc1cccc(C=O)c1           ┆ FOUR_PLUS_SIX      ┆ 2       ┆ 8.248397 ┆ 10120.34375   │
│ 1       ┆ Nc1nc(N)nc(N)n1 ┆ O=Cc1cccc(C=O)c1           ┆ FOUR_PLUS_SIX      ┆ 3       ┆ 8.247174 ┆ 34266.3125    │
│ 1       ┆ Nc1nc(N)nc(N)n1 ┆ O=Cc1cccc(C=O)c1           ┆ FOUR_PLUS_SIX      ┆ 4       ┆ 8.230059 ┆ 1.8782e6      │
│ 1       ┆ Nc1nc(N)nc(N)n1 ┆ O=Cc1cccc(C=O)c1           ┆ FOUR_PLUS_SIX      ┆ 5       ┆ 8.192161 ┆ 90943.367188  │
│ …       ┆ …               ┆ …                          ┆ …                  ┆ …       ┆ …        ┆ …             │
│ 75      ┆ NCCCN(CCCN)CCCN ┆ O=Cc1c(F)c(F)c(C=O)c(F)c1F ┆ TWENTY_PLUS_THIRTY ┆ 1086    ┆ 6.921977 ┆ 4.7586e6      │
│ 75      ┆ NCCCN(CCCN)CCCN ┆ O=Cc1c(F)c(F)c(C=O)c(F)c1F ┆ TWENTY_PLUS_THIRTY ┆ 1087    ┆ 6.830289 ┆ 3.9482e6      │
│ 75      ┆ NCCCN(CCCN)CCCN ┆ O=Cc1c(F)c(F)c(C=O)c(F)c1F ┆ TWENTY_PLUS_THIRTY ┆ 1088    ┆ 6.789335 ┆ 10370.679688  │
│ 75      ┆ NCCCN(CCCN)CCCN ┆ O=Cc1c(F)c(F)c(C=O)c(F)c1F ┆ TWENTY_PLUS_THIRTY ┆ 1089    ┆ 6.712317 ┆ 20498.773438  │
│ 75      ┆ NCCCN(CCCN)CCCN ┆ O=Cc1c(F)c(F)c(C=O)c(F)c1F ┆ TWENTY_PLUS_THIRTY ┆ 1090    ┆ 6.692757 ┆ 4.6947e6      │
└─────────┴─────────────────┴────────────────────────────┴────────────────────┴─────────┴──────────┴───────────────┘
```

---

# SQL Databases: Grouping

* Group by cage.

```python
imine_peaks.group_by("cage_id").agg(
    pl.col("peak_id"),
    pl.col("peak_id").count().alias("peak_count"),
    pl.col("intensity"),
    pl.col("intensity").mean().alias("mean_intensity"),
    pl.col("ppm"),
    pl.col("ppm").max().alias("max_ppm"),
    pl.col("ppm").min().alias("min_ppm"),
)
```

```
shape: (75, 8)
┌─────────┬───────────────────┬────────────┬─────────────────────────────────┬────────────────┬─────────────────────────────────┬──────────┬──────────┐
│ cage_id ┆ peak_id           ┆ peak_count ┆ intensity                       ┆ mean_intensity ┆ ppm                             ┆ max_ppm  ┆ min_ppm  │
│ ---     ┆ ---               ┆ ---        ┆ ---                             ┆ ---            ┆ ---                             ┆ ---      ┆ ---      │
│ i64     ┆ list[i64]         ┆ u32        ┆ list[f64]                       ┆ f64            ┆ list[f64]                       ┆ f64      ┆ f64      │
╞═════════╪═══════════════════╪════════════╪═════════════════════════════════╪════════════════╪═════════════════════════════════╪══════════╪══════════╡
│ 12      ┆ [715, 716, … 721] ┆ 7          ┆ [10192.625, 43773.078125, … 2.… ┆ 405137.783482  ┆ [7.4012, 7.397532, … 6.721486]  ┆ 7.4012   ┆ 6.721486 │
│ 24      ┆ [608, 609, … 630] ┆ 23         ┆ [1.8444e6, 1.4968e6, … 54105.6… ┆ 1.1098e6       ┆ [8.288128, 8.10353, … 6.502657… ┆ 8.288128 ┆ 6.502657 │
│ 27      ┆ [743, 744, … 752] ┆ 10         ┆ [3.8193e6, 10291.023438, … 1.1… ┆ 2.7230e6       ┆ [8.170767, 8.102307, … 6.88530… ┆ 8.170767 ┆ 6.885302 │
│ 9       ┆ [581, 582, … 588] ┆ 8          ┆ [407993.273438, 426312.789062,… ┆ 318827.628906  ┆ [7.707136, 7.690032, … 7.15371… ┆ 7.707136 ┆ 7.153714 │
│ 45      ┆ [980, 981]        ┆ 2          ┆ [64904.382812, 189849.882812]   ┆ 127377.132812  ┆ [7.436652, 7.183593]            ┆ 7.436652 ┆ 7.183593 │
│ …       ┆ …                 ┆ …          ┆ …                               ┆ …              ┆ …                               ┆ …        ┆ …        │
│ 41      ┆ [756, 757, … 764] ┆ 9          ┆ [20793.617188, 74953.179688, …… ┆ 34017.252604   ┆ [7.401811, 7.396309, … 7.16953… ┆ 7.401811 ┆ 7.169535 │
│ 68      ┆ [678, 679, … 682] ┆ 5          ┆ [2.4305e6, 20578.0, … 10533.76… ┆ 514449.3       ┆ [7.451934, 7.369414, … 7.19948… ┆ 7.451934 ┆ 7.199486 │
│ 53      ┆ [648, 649, … 653] ┆ 6          ┆ [10583.8125, 10000.039062, … 5… ┆ 2.8790e6       ┆ [7.499, 7.497166, … 7.115133]   ┆ 7.499    ┆ 7.115133 │
│ 71      ┆ [848, 849, … 861] ┆ 14         ┆ [319501.195312, 650741.15625, … ┆ 2.2848e6       ┆ [8.222113, 8.028345, … 6.59434… ┆ 8.222113 ┆ 6.594345 │
│ 50      ┆ [461, 462, … 475] ┆ 15         ┆ [64264.195312, 168296.21875, …… ┆ 2.5861e6       ┆ [8.034458, 8.015509, … 6.80950… ┆ 8.034458 ┆ 6.809506 │
└─────────┴───────────────────┴────────────┴─────────────────────────────────┴────────────────┴─────────────────────────────────┴──────────┴──────────┘
```

## Exercise

Get the top 2 most intense peak for each cage.

---

# SQL Databases: Exploding

Expanding collections into multiple rows.

```python
imine_peaks.group_by("cage_id").agg(
    pl.col("peak_id"),
)
```

```
shape: (75, 2)
┌─────────┬────────────────────┐
│ cage_id ┆ peak_id            │
│ ---     ┆ ---                │
│ i64     ┆ list[i64]          │
╞═════════╪════════════════════╡
│ 6       ┆ [284, 285, … 315]  │
│ 45      ┆ [980, 981]         │
│ 48      ┆ [182, 183, … 189]  │
│ 24      ┆ [608, 609, … 630]  │
│ 27      ┆ [743, 744, … 752]  │
│ …       ┆ …                  │
│ 59      ┆ [996, 997, … 1016] │
│ 41      ┆ [756, 757, … 764]  │
│ 56      ┆ [802, 803, … 814]  │
│ 44      ┆ [975, 976, … 979]  │
│ 47      ┆ [172, 173, … 181]  │
└─────────┴────────────────────┘
```


```python
imine_peaks.group_by("cage_id").agg(
    pl.col("peak_id"),
).explode("peak_id")
```

```
shape: (1_090, 2)
┌─────────┬─────────┐
│ cage_id ┆ peak_id │
│ ---     ┆ ---     │
│ i64     ┆ i64     │
╞═════════╪═════════╡
│ 12      ┆ 715     │
│ 12      ┆ 716     │
│ 12      ┆ 717     │
│ 12      ┆ 718     │
│ 12      ┆ 719     │
│ …       ┆ …       │
│ 44      ┆ 975     │
│ 44      ┆ 976     │
│ 44      ┆ 977     │
│ 44      ┆ 978     │
│ 44      ┆ 979     │
└─────────┴─────────┘
```
---

# Exercise

Get the top 2 imine and aldehyde peaks for each cage.

```
shape: (150, 8)
┌─────────┬─────────┬───────────────┬─────────────────┬────────────────────────────┬────────────────────┬──────────┬───────────────┐
│ cage_id ┆ peak_id ┆ cage_id_right ┆ amine           ┆ aldehyde                   ┆ topology           ┆ ppm      ┆ intensity     │
│ ---     ┆ ---     ┆ ---           ┆ ---             ┆ ---                        ┆ ---                ┆ ---      ┆ ---           │
│ i64     ┆ i64     ┆ i64           ┆ str             ┆ str                        ┆ str                ┆ f64      ┆ f64           │
╞═════════╪═════════╪═══════════════╪═════════════════╪════════════════════════════╪════════════════════╪══════════╪═══════════════╡
│ 1       ┆ 12      ┆ 1             ┆ Nc1nc(N)nc(N)n1 ┆ O=Cc1cccc(C=O)c1           ┆ FOUR_PLUS_SIX      ┆ 7.892647 ┆ 1.0535e7      │
│ 1       ┆ 19      ┆ 1             ┆ Nc1nc(N)nc(N)n1 ┆ O=Cc1cccc(C=O)c1           ┆ FOUR_PLUS_SIX      ┆ 7.696435 ┆ 7.7622e6      │
│ 2       ┆ 33      ┆ 2             ┆ Nc1nc(N)nc(N)n1 ┆ O=Cc1cccc(C=O)c1           ┆ EIGHT_PLUS_TWELVE  ┆ 8.397542 ┆ 4.5901e6      │
│ 2       ┆ 39      ┆ 2             ┆ Nc1nc(N)nc(N)n1 ┆ O=Cc1cccc(C=O)c1           ┆ EIGHT_PLUS_TWELVE  ┆ 7.781399 ┆ 4.7450e6      │
│ 3       ┆ 45      ┆ 3             ┆ Nc1nc(N)nc(N)n1 ┆ O=Cc1cccc(C=O)c1           ┆ TWENTY_PLUS_THIRTY ┆ 8.457445 ┆ 681756.976562 │
│ …       ┆ …       ┆ …             ┆ …               ┆ …                          ┆ …                  ┆ …        ┆ …             │
│ 73      ┆ 1055    ┆ 73            ┆ NCCCN(CCCN)CCCN ┆ O=Cc1c(F)c(F)c(C=O)c(F)c1F ┆ FOUR_PLUS_SIX      ┆ 6.767941 ┆ 2.4490e6      │
│ 74      ┆ 1059    ┆ 74            ┆ NCCCN(CCCN)CCCN ┆ O=Cc1c(F)c(F)c(C=O)c(F)c1F ┆ EIGHT_PLUS_TWELVE  ┆ 8.349253 ┆ 446451.890625 │
│ 74      ┆ 1060    ┆ 74            ┆ NCCCN(CCCN)CCCN ┆ O=Cc1c(F)c(F)c(C=O)c(F)c1F ┆ EIGHT_PLUS_TWELVE  ┆ 7.745946 ┆ 1.0738e6      │
│ 75      ┆ 1081    ┆ 75            ┆ NCCCN(CCCN)CCCN ┆ O=Cc1c(F)c(F)c(C=O)c(F)c1F ┆ TWENTY_PLUS_THIRTY ┆ 7.543622 ┆ 9.8546e6      │
│ 75      ┆ 1086    ┆ 75            ┆ NCCCN(CCCN)CCCN ┆ O=Cc1c(F)c(F)c(C=O)c(F)c1F ┆ TWENTY_PLUS_THIRTY ┆ 6.921977 ┆ 4.7586e6      │
└─────────┴─────────┴───────────────┴─────────────────┴────────────────────────────┴────────────────────┴──────────┴───────────────┘
shape: (51, 8)
┌─────────┬─────────┬───────────────┬───────────────────────────┬────────────────────────────┬────────────────────┬───────────┬───────────────┐
│ cage_id ┆ peak_id ┆ cage_id_right ┆ amine                     ┆ aldehyde                   ┆ topology           ┆ ppm       ┆ intensity     │
│ ---     ┆ ---     ┆ ---           ┆ ---                       ┆ ---                        ┆ ---                ┆ ---       ┆ ---           │
│ i64     ┆ i64     ┆ i64           ┆ str                       ┆ str                        ┆ str                ┆ f64       ┆ f64           │
╞═════════╪═════════╪═══════════════╪═══════════════════════════╪════════════════════════════╪════════════════════╪═══════════╪═══════════════╡
│ 1       ┆ 1       ┆ 1             ┆ Nc1nc(N)nc(N)n1           ┆ O=Cc1cccc(C=O)c1           ┆ FOUR_PLUS_SIX      ┆ 10.145727 ┆ 1.6102e6      │
│ 1       ┆ 3       ┆ 1             ┆ Nc1nc(N)nc(N)n1           ┆ O=Cc1cccc(C=O)c1           ┆ FOUR_PLUS_SIX      ┆ 10.115164 ┆ 392924.320312 │
│ 16      ┆ 5       ┆ 16            ┆ Cc1c(CN)c(C)c(CN)c(C)c1CN ┆ O=Cc1cccc(C=O)c1           ┆ FOUR_PLUS_SIX      ┆ 10.124944 ┆ 103388.335938 │
│ 17      ┆ 6       ┆ 17            ┆ Cc1c(CN)c(C)c(CN)c(C)c1CN ┆ O=Cc1cccc(C=O)c1           ┆ EIGHT_PLUS_TWELVE  ┆ 10.219688 ┆ 69940.921875  │
│ 17      ┆ 7       ┆ 17            ┆ Cc1c(CN)c(C)c(CN)c(C)c1CN ┆ O=Cc1cccc(C=O)c1           ┆ EIGHT_PLUS_TWELVE  ┆ 10.145115 ┆ 10033.234375  │
│ …       ┆ …       ┆ …             ┆ …                         ┆ …                          ┆ …                  ┆ …         ┆ …             │
│ 68      ┆ 72      ┆ 68            ┆ NCCCN(CCCN)CCCN           ┆ O=Cc1cc2sc(C=O)cc2s1       ┆ EIGHT_PLUS_TWELVE  ┆ 10.528983 ┆ 1.0481e6      │
│ 68      ┆ 73      ┆ 68            ┆ NCCCN(CCCN)CCCN           ┆ O=Cc1cc2sc(C=O)cc2s1       ┆ EIGHT_PLUS_TWELVE  ┆ 10.499642 ┆ 971561.828125 │
│ 71      ┆ 74      ┆ 71            ┆ NCCCN(CCCN)CCCN           ┆ O=Cc1ccc(C=O)cc1           ┆ EIGHT_PLUS_TWELVE  ┆ 9.882277  ┆ 56763.507812  │
│ 30      ┆ 75      ┆ 30            ┆ Cc1c(CN)c(C)c(CN)c(C)c1CN ┆ O=Cc1c(F)c(F)c(C=O)c(F)c1F ┆ TWENTY_PLUS_THIRTY ┆ 10.335827 ┆ 133951.320312 │
│ 75      ┆ 76      ┆ 75            ┆ NCCCN(CCCN)CCCN           ┆ O=Cc1c(F)c(F)c(C=O)c(F)c1F ┆ TWENTY_PLUS_THIRTY ┆ 9.882277  ┆ 10054.632812  │
└─────────┴─────────┴───────────────┴───────────────────────────┴────────────────────────────┴────────────────────┴───────────┴───────────────┘
```

---

# AtomLite: Storing molecular structures

You can store molecules in a SQLite database with `atomlite`.

```python
import atomlite
import sqlite3

connection = sqlite3.connect("workshop.db")
db = atomlite.Database("workshop.db")

# Insert an entry into the cage table
cursor = db.connection.execute(
    """
    INSERT INTO cages(amine, aldehyde, topology)
    VALUES (?,?,?)
    """,
    (smiles(amine), smiles(aldehyde), topology.name),
)

# Store the structure using AtomLite
db.add_entries(
    atomlite.Entry.from_rdkit(
        key=str(cursor.lastrowid),
        molecule=cage.to_rdkit_mol(),
    ),
)

```

---

# Calculating Diameters

```python
def main() -> None:
    args = parse_args()
    args.output.mkdir(exist_ok=True, parents=True)
    for cage in args.cage:
        output = args.output / cage.with_suffix(".json").name
        molecule = stk.BuildingBlock.init_from_file(cage)
        with open(output, "w") as f:
            json.dump({"diameter": molecule.get_maximum_diameter()}, f)
```

## Questions

* What are some issues with the above code?

---

# Calculating Diameters

## New file for each cage

## Editing requires re-writing a file

## Knowledge of file system required

## Exercise

* Iterate through all cage entries in `workshop.db`.
* Create an `stk.BuildingBlock` from the entry.
* Insert the cavity size into the database.

Hint:

```python
connection.execute(
    "INSERT INTO cavity_sizes(cage_id, size) VALUES (?,?)",
    (
        int(entry.key),
        molecule.get_maximum_diameter(),
    ),
)
```

---



---

# Outcomes

#. Build robust data schema
#. Understand trade-offs between different schema
#. Understand the impact of schema design on workflows
#. Use tooling to simplify data management

# Outline

#. Motivation
#. Schema design
#. Tools for data management
#. Data management & design excercise

# Motivation

* FAIR: findable, accessible, interoperable and reusable
* Data managment is a solved problem
* Data management is integral to science

# Schema design

* SQL vs NoSQL
* Complex schema implies complex processing

# Schema complexity and processing complexity

* Optional columns
* Dependent columns
* Multiple values in column

# SQL: Just a bunch of tables

* Normalization
* Constraints
* Joins
* Filtering
* Denormalization


# Tools for data management: SQLite

* Comes with Python
* All data in a single file
* Fast
* Runs everywhere

# Excercise

* SQLite
* AtomLite

# NMR Peaks

* Multiple represantations for empty (do they mean different things?)
* Multiple values per column
* Columns encoded as strings, eval + size of data
* Dependent data (imine?)
* Dupolicate rows? No primary key, constraints