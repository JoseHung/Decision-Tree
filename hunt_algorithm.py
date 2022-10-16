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


# data structure of the node
class node:
    def __init__(self, left_node=None, right_node=None, attribute=None, label=None, condition=None):
        self.left_node = left_node  # left node
        self.right_node = right_node  # right node
        self.attribute = attribute  # the split attribute
        self.label = label  # the predicate label
        self.condition = condition  # the split condition


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


def split_dataset(dataset, index):
    value = []
    best_gini = 1
    best_condition = None
    sub_dataset1 = []
    sub_dataset2 = []
    if not isinstance(dataset[0][index], int):
        for element in dataset:
            if element[index] not in value:
                value.append(element[index])
        num_attributes = len(value)
        for i in range(num_attributes):
            left = []
            right = []
            condition = value[i]
            for data in dataset:
                if data[index] == condition:
                    left.append(data)
                else:
                    right.append(data)
            left_gini = calc_gini(left)
            right_gini = calc_gini(right)
            temp_gini = left_gini * (len(left) / len(dataset)) + right_gini * (len(right) / len(dataset))
            if temp_gini < best_gini:
                best_gini = temp_gini
                sub_dataset1 = left
                sub_dataset2 = right
                best_condition = condition
    else:
        dataset = sorted(dataset, key=lambda x: x[index])
        for i in range(1, len(dataset)):
            if dataset[i][index] == dataset[i - 1][index]:
                continue
            else:
                left_gini = calc_gini(dataset[:i])
                right_gini = calc_gini(dataset[i:])
                temp_gini = left_gini * (i + 1) / len(dataset) + right_gini * (len(dataset) - i - 1) / len(dataset)
                if temp_gini < best_gini:
                    best_gini = temp_gini
                    sub_dataset1 = dataset[:i]
                    sub_dataset2 = dataset[i:]
                    best_condition = dataset[i][index]
    return [sub_dataset1, sub_dataset2], best_condition, best_gini


"""
input: dataset
function: according to hunt algorithm to recursively process the data to generate a decision tree
output: a decision tree
"""


def hunt(dataset):
    # if all the objects in S belong to the same class
    # return a leaf node with the value of this class
    current_label = dataset[0][-1]
    flag = 0
    for data in dataset:
        if data[-1] != current_label:
            flag = 1
            break
        else:
            continue
    if flag == 0:
        return node(label=current_label)

    # if (all the objects in S have the same attribute values)
    # return a leaf node whose class value is the majority one in S
    flag_1 = 0
    for i in range(1, len(dataset)):
        for j in range(len(dataset[0]) - 1):
            if dataset[i][j] != dataset[i - 1][j]:
                flag_1 = 1
                break
            else:
                continue
    if len(dataset) <= 300:
        flag_1 = 0
    if flag_1 == 0:
        dict = {}
        for data in dataset:
            if data[-1] not in dict.keys():
                dict[data[-1]] = 1
            else:
                dict[data[-1]] += 1
        value_list = list(dict.values())
        key = list(dict.keys())[value_list.index(max(value_list))]
        return node(label=key)
    # find the 'best' split attribute A* and predicate P*
    best_gini = 0.5
    best_split = None
    best_attribute = None
    best_condition = None
    for i in range(len(dataset[0]) - 1):
        current_split, current_condition, current_gini = split_dataset(dataset, i)
        if current_gini < best_gini:
            best_gini = current_gini
            best_split = current_split
            best_condition = current_condition
            best_attribute = i
    sub_left = hunt(best_split[0])
    sub_right = hunt(best_split[1])
    return node(left_node=sub_left, right_node=sub_right, attribute=best_attribute, condition=best_condition)


"""
input: root, data
function: according to the decision tree, predict the label category of the input data
output: the prediction label
"""


def predict(root, record):
    current_node = root
    while not current_node.label:
        if isinstance(current_node.condition, int):
            if record[current_node.attribute] < current_node.condition:
                current_node = current_node.left_node
            else:
                current_node = current_node.right_node
        else:
            if record[current_node.attribute] == current_node.condition:
                current_node = current_node.left_node
            else:
                current_node = current_node.right_node
    return current_node.label


"""
input: the root of the decision tree
function: print the decision tree generated by layer order traversal,
          and the content to the decision_tree.txt file
output: the decision tree 
"""


def print_tree(node):
    layer = 0
    queue = [node]
    f = open("decision_tree.txt", 'w')
    while len(queue):
        length = len(queue)
        layer += 1
        for i in range(length):
            tmp = queue.pop(0)
            print("layer:", layer, "label:", tmp.label, "attribute:", tmp.attribute, "condition:", tmp.condition)
            content = "layer:" + str(layer) + ", label:" + str(tmp.label) + ", attribute" + str(
                tmp.attribute) + ", condition" + str(tmp.condition)
            f.write(content)
            f.write('\n')
            if tmp.left_node:
                queue.append(tmp.left_node)
            if tmp.right_node:
                queue.append(tmp.right_node)
    f.close()


if __name__ == '__main__':
    training_data_path = "./training_set/adult.data"
    evaluation_data_path = "./evaluation_set/adult.test"
    dataset = load_dataset(training_data_path)
    testset = load_dataset(evaluation_data_path)
    root = hunt(dataset)
    correct = 0
    num = 0
    for record in testset:
        num += 1
        predict_label = predict(root, record)
        if predict_label == record[-1][:-1]:
            correct += 1
    print_tree(root)
    print(correct, num, float(correct / num))
