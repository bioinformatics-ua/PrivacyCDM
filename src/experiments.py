import os
import csv
from pprint import pprint


dataLocation = "../cohorts/data"
original = dict()
anonymised = dict()

for k in [2, 3, 4, 5]:
    anonymised[k] = dict()
    for (dirpath, dirnames, filenames) in os.walk(dataLocation):
        for file in filenames:
            with open(f"{dataLocation}/{file}", "r") as f:
                content = f.readlines()
            header = content[:1][0].split(",")
            original[file] = {
                "fields":len(header),
                "rows": len(content)-1
            }

            os.system(f"python3 main.py -dl {dataLocation}/{file} -ka -k {k} -el ../results/k_anonymity/")

    for (dirpath, dirnames, filenames) in os.walk("../results/k_anonymity/"):
        for file in filenames:
            if "k"+str(k) in file:
                originalFile = file.split("_")[-3]+"_cohort_rows.csv"
                with open(f"../results/k_anonymity/{file}", "r") as f:
                    content = f.readlines()
                header = content[:1][0].split(",")
                numRows = len(content)-1
                perShared = numRows*100/original[originalFile]["rows"]
                anonymised[k][originalFile] = {
                    "fields":len(header),
                    "rows": numRows,
                    "per shared": str(round(perShared, 2)),
                    "per lost": str(round(100 - perShared, 2))
                }

pprint(original)
pprint(anonymised)

##### LaTeX
for k in anonymised:
    print("\\textit{k} = " + str(k) + " && ", end="")
    print(f"{anonymised[k]['i_cohort_rows.csv']['rows']} ({anonymised[k]['i_cohort_rows.csv']['per shared']} \%) & ", end="")
    print(f"{anonymised[k]['ii_cohort_rows.csv']['rows']} ({anonymised[k]['ii_cohort_rows.csv']['per shared']} \%) & ", end="")
    print(f"{anonymised[k]['iii_cohort_rows.csv']['rows']} ({anonymised[k]['iii_cohort_rows.csv']['per shared']} \%) & ", end="")
    print(f"{anonymised[k]['iv_cohort_rows.csv']['rows']} ({anonymised[k]['iv_cohort_rows.csv']['per shared']} \%) & ", end="")
    print(f"{anonymised[k]['v_cohort_rows.csv']['rows']} ({anonymised[k]['v_cohort_rows.csv']['per shared']} \%) \\\\ ", end="")
    print()


######### l-Diversity
original = dict()
anonymised = dict()

for l in [2, 3, 4, 5]:
    anonymised[l] = dict()
    for (dirpath, dirnames, filenames) in os.walk(dataLocation):
        for file in filenames:
            with open(f"{dataLocation}/{file}", "r") as f:
                content = f.readlines()
            header = content[:1][0].split(",")
            original[file] = {
                "fields":len(header),
                "rows": len(content)-1
            }

            os.system(f"python3 main.py -dl {dataLocation}/{file} -ld -l {l} -el ../results/l_diversity/")

    for (dirpath, dirnames, filenames) in os.walk("../results/l_diversity/"):
        for file in filenames:
            if "l"+str(l) in file:
                originalFile = file.split("_")[-3]+"_cohort_rows.csv"
                with open(f"../results/l_diversity/{file}", "r") as f:
                    content = f.readlines()
                header = content[:1][0].split(",")
                numRows = len(content)-1
                perShared = numRows*100/original[originalFile]["rows"]
                anonymised[l][originalFile] = {
                    "fields":len(header),
                    "rows": numRows,
                    "per shared": str(round(perShared, 2)),
                    "per lost": str(round(100 - perShared, 2))
                }
pprint(original)
pprint(anonymised)

##### LaTeX
for l in anonymised:
    print("\\textit{l} = " + str(l) + " && ", end="")
    print(f"{anonymised[l]['i_cohort_rows.csv']['rows']} ({anonymised[l]['i_cohort_rows.csv']['per shared']} \%) & ", end="")
    print(f"{anonymised[l]['ii_cohort_rows.csv']['rows']} ({anonymised[l]['ii_cohort_rows.csv']['per shared']} \%) & ", end="")
    print(f"{anonymised[l]['iii_cohort_rows.csv']['rows']} ({anonymised[l]['iii_cohort_rows.csv']['per shared']} \%) & ", end="")
    print(f"{anonymised[l]['iv_cohort_rows.csv']['rows']} ({anonymised[l]['iv_cohort_rows.csv']['per shared']} \%) & ", end="")
    print(f"{anonymised[l]['v_cohort_rows.csv']['rows']} ({anonymised[l]['v_cohort_rows.csv']['per shared']} \%) \\\\ ", end="")
    print()

######### both
original = dict()
anonymised = dict()

for k in [2, 3]:
    anonymised[k] = dict()
    for l in [2, 3]:
        anonymised[k][l] = dict()
        for (dirpath, dirnames, filenames) in os.walk(dataLocation):
            for file in filenames:
                with open(f"{dataLocation}/{file}", "r") as f:
                    content = f.readlines()
                header = content[:1][0].split(",")
                original[file] = {
                    "fields":len(header),
                    "rows": len(content)-1
                }

                os.system(f"python3 main.py -dl {dataLocation}/{file} -ka -k {k} -ld -l {l} -el ../results/both/")

        for (dirpath, dirnames, filenames) in os.walk("../results/both/"):
            for file in filenames:
                if "l"+str(l) in file:
                    originalFile = file.split("_")[-3]+"_cohort_rows.csv"
                    with open(f"../results/both/{file}", "r") as f:
                        content = f.readlines()
                    header = content[:1][0].split(",")
                    numRows = len(content)-1
                    perShared = numRows*100/original[originalFile]["rows"]
                    anonymised[k][l][originalFile] = {
                        "fields":len(header),
                        "rows": numRows,
                        "per shared": str(round(perShared, 2)),
                        "per lost": str(round(100 - perShared, 2))
                    }
pprint(original)
pprint(anonymised)

##### LaTeX
for k in anonymised:
    for l in anonymised[k]:
        print("\\textit{k} = " + str(k) + ", \\textit{l} = " + str(l) + " && ", end="")
        print(f"{anonymised[k][l]['i_cohort_rows.csv']['rows']} ({anonymised[k][l]['i_cohort_rows.csv']['per shared']} \%) & ", end="")
        print(f"{anonymised[k][l]['ii_cohort_rows.csv']['rows']} ({anonymised[k][l]['ii_cohort_rows.csv']['per shared']} \%) & ", end="")
        print(f"{anonymised[k][l]['iii_cohort_rows.csv']['rows']} ({anonymised[k][l]['iii_cohort_rows.csv']['per shared']} \%) & ", end="")
        print(f"{anonymised[k][l]['iv_cohort_rows.csv']['rows']} ({anonymised[k][l]['iv_cohort_rows.csv']['per shared']} \%) & ", end="")
        print(f"{anonymised[k][l]['v_cohort_rows.csv']['rows']} ({anonymised[k][l]['v_cohort_rows.csv']['per shared']} \%) \\\\ ", end="")
        print()