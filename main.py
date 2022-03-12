import argparse
import pandas as pd

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--qi', help='Quasi Identifier', required=True, type=str, nargs='+')
    parser.add_argument('--k', help='K-Anonimity', required=True, type=int)
    parser.add_argument('--dataset', help='Dataset to be anonymized', required=True, type=str)
    parser.add_argument('--dgh', help='Domain Generalization Hierarchy', required=True, type=str)
    args = parser.parse_args()

    K = args.k
    df = pd.read_csv(args.dataset)
    qi = [x for x in args.qi]