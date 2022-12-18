# -*- coding: utf-8 -*-
"""

Q&A generator using Pandas and Random.

"""

import pandas
import random

qna = pandas.read_excel("resources/Millionaire-Questions.xlsx", "sheet", usecols = "A,B,C,D,E")
qnad = qna.to_dict('index')

while True:
    r = random.randint(0, len(qnad))
    print(qnad[r]["PITANJE"])

    a = input()
    if(a == ""):
        print(qnad[r]["OPCIJA1"])
        print(qnad[r]["OPCIJA2"])
        print(qnad[r]["OPCIJA3"])
        print(qnad[r]["OPCIJA4"])