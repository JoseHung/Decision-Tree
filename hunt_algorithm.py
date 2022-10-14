

"""
    input:
        S: the training set
    return:
        the root of the decision tree
    
    hunt(S):
        if all the objects in S belong to the same class
            return a leaf node with the value of this class
        if (all the objects in S have the same attribute values) or 
        (|S| is too small)
            return a leaf node whose class value is the majority one in S
        find the 'best' split attribute A* and predicate P*
        S1 = the set of objects in S satisfying P*
        S2 = S - S1
        u1 = hunt(S1)
        u2 = hunt(S2)
        creat a root u with left child u1 and right child u2
        Au = A*
        Pu = P*
        return u
"""

"""
input: the path of the data file
function: To read the original data and preprocess the data with removing all the records containing '?' and
            the attribute "native-country". Then save the data to the dataset
output: dataset
"""
def load_dataset(filename):
    fr = open(filename)
    dataset = []
    label = []
    for line in fr.readlines():
        cutline = line.strip().split(', ')
        # Remove all the records containing '?'
        if '?' not in cutline and cutline != ['']:
            # remove the attribute "native-country"
            dataset.append(cutline[:-2] + cutline[-1:])
    return dataset


"""
input: dataset
function: calculate the gini value of the dataset
output: the gini value 
"""
def calc_gini(dataset):
    # the total number of the data
    num_of_data = len(dataset)
    label_cnt = {}
    for example in dataset:
        current_label = example[-1]
        if current_label not in label_cnt.keys():
            label_cnt[current_label] = 0
        label_cnt[current_label] += 1
    for key in label_cnt:
        label_cnt[key] /= num_of_data
        label_cnt[key] = label_cnt[key] * label_cnt[key]
    gini = 1 - sum(label_cnt.values())
    return gini


"""
input: dataset, index, value
function: split the dataset into two subsets based on whether the index attribute is value
output: sub_dataset
"""
def split_dataset(dataset, index, value):
    sub_dataset1 = []
    sub_dataset2 = []
    for example in dataset:
        current_list = []
        if example[index] == value:
            current_list = example[:index]
            current_list.extend(example[index + 1:])
            sub_dataset1.append(current_list)
        else:
            current_list = example[:index]
            current_list.extend(example[index + 1:])
            sub_dataset2.append(current_list)
    print(sub_dataset1)
    return sub_dataset1, sub_dataset2


"""
input: dataset
function: find the best split
output: index_of_best_feature, best_split_point
"""
def find_best_split(dataset):
    # the number of attributes
    num_attributes = len(dataset[0]) - 1
    if num_attributes == 1:
        return 0
    best_gini = 1
    index_of_best_split = -1
    for i in range(num_attributes):
        # duplicate removal
        unique_vals = set(example[i] for example in dataset)
        gini = {}
        for value in unique_vals:
            sub_dataset1, sub_dataset2 = split_dataset(dataset, i, value)
            # 建一个二叉树类，在递归处理数据时，实时构建出二叉树；
            # 根据离散和连续的两类数值写出对应分割点的函数
            # 递归函数注意终止条件



if __name__ == '__main__':
    training_data_path = "./training_set/adult.data"
    dataset = load_dataset(training_data_path)
    calc_gini(dataset)

