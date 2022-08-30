import sys
import os
import numpy as np
import pandas as pd
import time
import csv
import psutil
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, fpgrowth

def Apriori(ds, thold, m, num, rt, pc, o, pf):
    data = pd.read_csv(ds, header=None)
    data = pd.DataFrame(data)
    data.columns = ['item']
    data['item'] = data['item'].str.strip()
    data['item'] = data.item.apply(lambda x: x.split(' '))
    t_encoder = TransactionEncoder()
    te_ary = t_encoder.fit(data['item']).transform(data['item'])
    df = pd.DataFrame(te_ary, columns=t_encoder.columns_)

    # Start Time
    start = time.process_time()
    apriori_patterns = apriori(df, min_support=float(thold), use_colnames=True)

    # Calculate Memory
    process = psutil.Process(os.getpid())
    memory = process.memory_info().rss / (1024 * 1024)

    # End Time
    end = time.process_time()
    run_time = 1000 * (end - start)

    num_of_patterns = len(apriori_patterns)

    # Checking parameters
    if m:
        print("Total memory usage (mb): ", memory, "mb")
    if num:
        print("Total number of frequent patterns : ", num_of_patterns)
    if rt:
        print("Total runtime (ms): ", run_time, "ms")
    if pc:
        print("The frequent patterns are: \n", apriori_patterns)
    if o:
        csv_output = algoName + '_' + ds + '.csv'
        exist = os.path.exists(csv_output)
        if exist:
            data = [float(thold), run_time, memory]
            with open(csv_output, 'a') as f:
                writer = csv.writer(f)
                writer.writerow(data)
        else:
            data = [float(thold), run_time, memory]
            with open(csv_output, 'w+', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(data)
    if pf:
        pattern_file_name = algoName + '_' + ds + '_' + str(thold) + '.txt'
        pattern_file = open(pattern_file_name, "w+")
        str_patterns = apriori_patterns.to_string(header=True, index=True)
        pattern_file.write(str_patterns)
        pattern_file.close()

def FPgrowth(ds, thold, m, num, rt, pc, o, pf):
    data = pd.read_csv(ds, header=None)
    data = pd.DataFrame(data)
    data.columns = ['item']
    data['item'] = data['item'].str.strip()
    data['item'] = data.item.apply(lambda x: x.split(' '))
    t_encoder = TransactionEncoder()
    te_ary = t_encoder.fit(data['item']).transform(data['item'])
    df = pd.DataFrame(te_ary, columns=t_encoder.columns_)

    # Start Time
    start = time.process_time()

    # FP-growth algorithm
    fp_patterns = fpgrowth(df, min_support=float(thold), use_colnames=True)

    # Calculate memory
    process = psutil.Process(os.getpid())
    memory = process.memory_info().rss / (1024 * 1024)

    # End time
    end = time.process_time()
    run_time = 1000 * (end - start)
    num_of_patterns = len(fp_patterns)

    #Checking parameters
    if m:
        print("Total memory usage (mb): ", memory, "mb")
    if num:
        print("Total number of frequent patterns: ", num_of_patterns)
    if rt:
        print("Total runtime (ms): ", run_time, "ms")
    if pc:
        print("The frequent patterns are: \n", fp_patterns)
    if o:
        csv_output = algoName + '_' + ds + '.csv'
        exist = os.path.exists(csv_output)
        if exist:
            data = [float(thold), run_time, memory]
            with open(csv_output, 'a') as f:
                writer = csv.writer(f)
                writer.writerow(data)
        else:
            data = [float(thold), run_time, memory]
            with open(csv_output, 'w+', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(data)

    if pf:
        pattern_file_name = algoName + '_' + ds + '_' + str(thold) + '.txt'
        pattern_file = open(pattern_file_name, "w+")
        str_patterns = fp_patterns.to_string(header=True, index=True)
        pattern_file.write(str_patterns)
        pattern_file.close()

# main function

if __name__ == '__main__':
    n = len(sys.argv)
    algoName = "AP"
    dataset = "Toy.txt"
    threshold = 0.2
    m = False
    num = False
    rt = False
    pc = False
    o = False
    pf = False
    if n > 1:
        for i in range(1, n):
            parameter = sys.argv[i]

            if parameter == "-a":
                algoName = sys.argv[i + 1]
                if algoName != "AP" and algoName != "FP":
                    print("The input is incorrect!!! please try again!")

            if parameter == "-d":
                dataset = sys.argv[i + 1]
                if dataset != 'Toy.txt' and dataset != "chess.dat" and dataset != "mushroom.dat" and dataset != "retail.dat" and  dataset != "kosarak.dat":
                    print("The input is incorrect!! please try again!")
            if parameter == "-t":
                threshold = sys.argv[i + 1]
            if parameter == "-m":
                m = True
            if parameter == "-n":
                num = True
            if parameter == "-rt":
                rt = True
            if parameter == "-pc":
                pc = True
            if parameter == "-o":
                o = True
            if parameter == "-pf":
                pf = True

    if algoName == "AP":
        Apriori(dataset, threshold, m, num, rt, pc, o, pf)
    if algoName == "FP":
        FPgrowth(dataset, threshold, m, num, rt, pc, o, pf)