# Decision-Tree
### How to use the program

After opening the folder path in the terminal, use the following command to run the program.

```bash
python3 hunt_algorithm.py
```



### Goal

Implement Hung's algorithm for decision tree classification



### Dataset

The training set is [adult.data](./training_set/adult.data) and evaluation set is [adult.test](./evaluation_set/adult.test).



### Preprocessing

Remove all the records containing '?' (i.e., missing values). Also, remove the attribute "native-country".



### Deliverables

- An executable program, which should output a decision tree to the disk when given an input training set. 
- A readme file detailing how to use the program.
- [Source code](./hunt_algorithm.py).
- A [document](./Project Report.md) describing (i) the [decision tree](./decision_tree.txt) built from the *Adult* training set, and (ii) a [report](./predict_result.txt) on using the tree to classify the records of the evaluation set. The report should indicate, for each record in the evaluation set, its attributes and whether it has been classified successfully.

