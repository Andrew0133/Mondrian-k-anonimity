# Mondrian k-anonimity algorithm
## Introduction
Mondrian is a multidimensional k-anonymity model that anonymizes data through recursively splitting the attributes' dimensions with a median-partition strategy. This model is very fast and scalable.<br>
The proposed solution is a Top-down greedy data anonymization algorithm for relational dataset, proposed by Kristen LeFevre in his papers.<br>
The algorithm proposed by LeFevre imposes an intuitive ordering on each attribute. So, there are no generalization hierarchies for categorical attributes. This operation brings lower information loss, but worse semantic results.

## Key concepts
### Quasi-identifier (QI)
A QI set is a subset of attributes X<sub>1</sub>, ..., X<sub>d</sub> in table T that could potentially be used to re-identify individual records. Examples of quasi-identifiers are sex, age, zip code, and race. There is no specific rule for determining which attributes are quasi-identifiers; in practical applications, a domain expert might need to determine the QI set among all the attributes in a table.

### Equivalence class
With respect to attributes X<sub>1</sub>, ..., X<sub>d</sub> in table T, an equivalence class is the set of all records in T containing identical values (x<sub>1</sub>, ..., x<sub>d</sub>) for X<sub>1</sub>, ..., X<sub>d</sub>.

### Generalization
The method of generalization transforms QI values into less specific, but semantically useful values so that records with the same transformed QI values are indistinguishable.

### Local recoding
With local recoding, individual records are mapped to generalized forms. In this method, the data space is partitioned into different regions and then all records in the same region are mapped to the same generalized record. For example, a value of "60" for age in two records could possibly be mapped to two different intervals of "[55–60]" and "[60–65]" respectively if the two records are partitioned to different regions. Both multi-dimensional recoding (described above) and local recoding can improve the quality of anonymization without over-generalization and result in less information loss.

### Strict model
In the strict mode, the algorithm splits a partition in two parts, lhs and rhs, by using a split value (median of partition projected on a quasi-identifier). These parts can't contain common split value, so there is no intersection between the two parts.

### Performance metric
To asses the performance of the anonymization algorithm we used the concept of normalized average equivalence class size metric (C<sub>AVG</sub>). This metric measures how well partitioning approaches the best case (information loss). The formula is shown below:<br><br>
<img src="https://render.githubusercontent.com/render/math?math=\color{grey}\LARGE \frac{\frac{total\_records}{total\_equiv\_classes}}{k}">

## Algorithm explanation
The algorithm starts with choosing the dim, one heuristic, used in our implementation, chooses the dimension (quasi-identifier) with the widest (normalized) range of values. If there is no allowable cut for choosed dim and the partition is greater than 2*k the algorithm changes dimension (QI) with the next widest (normalized) range of values, until there is no allowable cut for partition considering all QI’s.<br>
After the value has been chosen it is calculated the frequency set of the dim.<br>
Then the split value is calculated using the standard median-finding algorithm. The split value is the median of the partition projected on dim.<br>
Then the current partition is splitted in two sub partitions based on a split_val parameter.<br>
In the end, the Anonymize algorithm is called recursively in both sub partitions.<br>

## Pseudo-code algorithm
The following pseudo-code is based on paper and it was the starting point for the implemented solution.
```python
Anonymize(partition)
    if (no allowable multidimensional cut for partition)
        return φ : partition → summary
    else
        dim ← choose_dimension()
        fs ← frequency_set(partition, dim)
        splitVal ← find_median(fs)
        lhs ← {t ∈ partition : t.dim ≤ splitVal}
        rhs ← {t ∈ partition : t.dim > splitVal}
        return Anonymize(rhs) ∪ Anonymize(lhs)
```

## Datasets
For testing purpose there are different datasets in data folder:
+ adult.csv
+ data_test.csv
+ db_100.csv

## Execution
### Arguments
--qi, Quasi Identifier, required<br>
--k, K-Anonimity, required<br>
--dataset, Dataset to be anonymized, required<br>
--rid, Remove id column, "y" otherwise "n"<br>
--plt, Graphical representation test for different K, "y" otherwise "n"<br>

### Run examples
```console
foo@bar:~$ python main.py --qi "age" "zip_code" "city_birth" --k 2 --dataset "data/db_100.csv"
...
foo@bar:~$ python main.py --qi "age" "work_class" "education_num" "marital_status" "occupation" "race" "sex" "native_country" --k 200 --dataset "data/adult.csv" --plt y
...
```

## Output
The anonymized result is saved on data/output.csv file.<br>
The file plot_output.jps will be generated if the argument --plt y is specified.

## References
Mondrian_Multidimensiona_K-Anonymity.pdf

## Authors
+ [Andrea Mercuri](https://github.com/ilmercu)
+ [Andrea Mazza](https://github.com/Andrew0133)
