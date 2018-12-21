from os import listdir
from os.path import isfile, join
import re

data_set = "C:\\Users\\Hamed Khashehchi\\Downloads\\Telegram Desktop\\ProjectTextProcessing\\Data Set"
class1 = data_set + "\\1"
class2 = data_set + "\\2"
class3 = data_set + "\\3"
class4 = data_set + "\\4"
class5 = data_set + "\\5"
class6 = data_set + "\\6"

attribute1 = class1 + "\\BestAttributes_class1.txt"
attribute2 = class2 + "\\BestAttributes_class2.txt"
attribute3 = class3 + "\\BestAttributes_class3.txt"
attribute4 = class4 + "\\BestAttributes_class4.txt"
attribute5 = class5 + "\\BestAttributes_class5.txt"
attribute6 = class6 + "\\BestAttributes_class6.txt"


def all_train(paths):
    save = []
    for path in paths:
        path = path + "\\train"
        files = [f for f in listdir(path) if isfile(join(path, f))]
        for f in files:
            save.append(f)
    print(len(save))
    return save


def all_test(paths):
    save = []
    for path in paths:
        path = path + "\\test"
        files = [f for f in listdir(path) if isfile(join(path, f))]
        for f in files:
            save.append(f)
    print(len(save))
    return save


def readingAttributes(paths):
    save = []
    for path in paths:
        file = open(path, "r")
        save.append(file.read().splitlines())
    print(save)
    return save


def readingData(path, train=True):
    if train:
        path = path + "\\train"
    else:
        path = path + "\\test"
    print(path)
    files = [f for f in listdir(path) if isfile(join(path, f))]
    print(files)
    # unique_words = set([])
    # s = 0
    all_words = []
    for f in files:
        file = open(path + "\\" + f, "r")
        lines = file.readlines()
        # words = []
        for line in lines:
            # word = line.split()
            q = re.split(r'(?<!\d)[<>(),|*-_.?$!:\'`@"]|[<>()$,.!-_?|*`\':@"](?!\d)|\s+', line)
            mm = [x for x in q if x.__len__() > 0]
            # print("line is ", line)
            # print(q)
            # print(mm)
            word = mm
            # input()
            for w in word:
                # words.append(w)
                # unique_words.add(w)
                all_words.append(w)
        # print(words)
        # s += len(words)
    print(len(all_words))
    dict = {}
    unique_words = set(all_words)
    print(len(unique_words))
    for w in unique_words:
        dict[w] = all_words.count(w)
    print(dict)
    return dict, len(files)


def ensemble(dictionaries):
    words = {}
    for dictionary in dictionaries:
        print(dictionary)
        keys = dictionary.keys()
        for key in keys:
            # print("key ", key)
            # print(key in words)
            if key in words:
                words[key] = words[key]+dictionary[key]
            else:
                words[key] = dictionary[key]
    print(words.__len__())
    print(words)
    return words


def effective(dictionary, half):
    dict = {}
    # print()
    # print()
    # print()
    # print(half)
    # input()
    print()
    print()
    print()
    # print("effective")
    # print()
    for key in half.keys():
        dict[key] = 2*half[key] - dictionary[key]
    print(dict)
    # input()
    return dict


def get_attribute(prop):
    attr = []
    for item in prop:
        # print(item)
        x, y = item
        # print(x)
        attr.append(x)
    return attr


def grouping(attributes):
    attr = []
    for attribute in attributes:
        for attri in attribute:
            attr.append(attri)
    return attr


def probability(number_of_class, dictionary, attributes):
    probable = {}
    for w in attributes:
        probable[w] = 1
        if w in dictionary:
            probable[w] = probable[w] + dictionary[w]
        probable[w] = probable[w]/(number_of_class+len(attributes))
    print(probable)
    return probable


def run_down_naive(PC, PCI, path, true):
    print("running down")
    path = path + "\\test"
    files = [f for f in listdir(path) if isfile(join(path, f))]
    answers = []
    for f in files:
        file = open(path + "\\" + f, "r")
        lines = file.readlines()
        words = []
        for line in lines:
            q = re.split(r'(?<!\d)[<>(),|*-_.?$!:\'`@"]|[<>()$,.!-_?|*`\':@"](?!\d)|\s+', line)
            mm = [x for x in q if x.__len__() > 0]
            for w in mm:
                words.append(w)

        possible = {}
        for i in range(len(PC)):
            pc = PC[i]
            # print(pc)
            pci = PCI[i]
            # print(pci)
            result = pc
            for w in pci.keys():
                if w in words:
                    result *= pci[w]
            possible[i] = result
        # print(possible)
        answer = sorted(possible.items(), key=lambda kv: kv[1], reverse=True)[0]
        x, y = answer
        answers.append(x)
        # answers.append(possible)
    # print(answers)
    correct = answers.count(true)
    return answers, correct/len(answers)


def create(train, attributes, classes):
    if train:
        path = "train.arff"
        answer = "@relation train\n\n"
    else:
        path = "test.arff"
        answer = "@relation test\n\n"
    for attr in attributes:
        answer += "@attribute '" + attr + "' {0, 1}\n"
    answer += "@attribute 'classes' {"
    for adad, c in enumerate(classes, 1):
        print(c)
        print(adad)
        if adad is len(classes):
            answer += str(adad) + "}\n"
        else:
            answer += str(adad) + ", "
    answer += "\n@data\n"

    for adad, c in enumerate(classes, 1):
        if train:
            p = c + "\\train"
        else:
            p = c + "\\test"
        files = [f for f in listdir(p) if isfile(join(p, f))]
        for f in files:
            file = open(p + "\\" + f, "r")
            lines = file.readlines()
            all_words = []
            for line in lines:
                q = re.split(r'(?<!\d)[<>(),|*-_.?$!:\'`@"]|[<>()$,.!-_?|*`\':@"](?!\d)|\s+', line)
                mm = [x for x in q if x.__len__() > 0]
                word = mm
                for w in word:
                    all_words.append(w)
            for s, attr in enumerate(attributes):
                if attr in all_words:
                    answer += "1,"
                else:
                    answer += "0,"
            answer += str(adad) + "\n"
            # print(answer)
            # input()
    # print(answer)
    f = open(path, "w")
    f.write(answer)


if __name__ == '__main__':
    dict1_train, C1 = readingData(class1)
    dict2_train, C2 = readingData(class2)
    dict3_train, C3 = readingData(class3)
    dict4_train, C4 = readingData(class4)
    dict5_train, C5 = readingData(class5)
    dict6_train, C6 = readingData(class6)
    dict = ensemble([dict1_train, dict2_train, dict3_train, dict4_train, dict5_train, dict6_train])
    effect1 = effective(dict, dict1_train)
    effect2 = effective(dict, dict2_train)
    effect3 = effective(dict, dict3_train)
    effect4 = effective(dict, dict4_train)
    effect5 = effective(dict, dict5_train)
    effect6 = effective(dict, dict6_train)
    property1 = sorted(effect1.items(), key=lambda kv: kv[1], reverse=True)[0:20]
    property2 = sorted(effect2.items(), key=lambda kv: kv[1], reverse=True)[0:20]
    property3 = sorted(effect3.items(), key=lambda kv: kv[1], reverse=True)[0:20]
    property4 = sorted(effect4.items(), key=lambda kv: kv[1], reverse=True)[0:20]
    property5 = sorted(effect5.items(), key=lambda kv: kv[1], reverse=True)[0:20]
    property6 = sorted(effect6.items(), key=lambda kv: kv[1], reverse=True)[0:20]
    attr1 = get_attribute(property1)
    print(attr1)
    input()
    attr2 = get_attribute(property2)
    print(attr2)
    input()
    attr3 = get_attribute(property3)
    print(attr3)
    input()
    attr4 = get_attribute(property4)
    print(attr4)
    input()
    attr5 = get_attribute(property5)
    print(attr5)
    input()
    attr6 = get_attribute(property6)
    print(attr6)
    input()
    attributes = grouping([attr1, attr2, attr3, attr4, attr5, attr6])
    # print(attr1)
    sum = C1 + C2 + C3 + C4 + C5 + C6
    # print(attributes)
    PC = [C1/sum, C2/sum, C3/sum, C4/sum, C5/sum, C6/sum]
    PC1 = probability(C1, dict1_train, attributes)
    PC2 = probability(C2, dict2_train, attributes)
    PC3 = probability(C3, dict3_train, attributes)
    PC4 = probability(C4, dict4_train, attributes)
    PC5 = probability(C5, dict5_train, attributes)
    PC6 = probability(C6, dict6_train, attributes)
    _, accuracy1 = run_down_naive(PC, [PC1, PC2, PC3, PC4, PC5, PC6], class1, 0)
    _, accuracy2 = run_down_naive(PC, [PC1, PC2, PC3, PC4, PC5, PC6], class2, 1)
    _, accuracy3 = run_down_naive(PC, [PC1, PC2, PC3, PC4, PC5, PC6], class3, 2)
    _, accuracy4 = run_down_naive(PC, [PC1, PC2, PC3, PC4, PC5, PC6], class4, 3)
    _, accuracy5 = run_down_naive(PC, [PC1, PC2, PC3, PC4, PC5, PC6], class5, 4)
    _, accuracy6 = run_down_naive(PC, [PC1, PC2, PC3, PC4, PC5, PC6], class6, 5)
    print(accuracy1)
    print(accuracy2)
    print(accuracy3)
    print(accuracy4)
    print(accuracy5)
    print(accuracy6)
    print(attributes)
    create(train=True, attributes=attributes, classes=[class1, class2, class3, class4, class5, class6])
    create(train=False, attributes=attributes, classes=[class1, class2, class3, class4, class5, class6])
    # print(PC)
    # print()
    # print()
    # print(property1)
    # print()
    # # input()
    # print(property2)
    # print()
    # print(property3)
    # print()
    # print(property4)
    # print()
    # print(property5)
    # print()
    # print(property6)
    # dick1 = {"ali":2, "Ali":3, "marry":1}
    # dick2 = {"reza":5, "ali":3, "marry":2}
    # dick3 = {"ali":2, "Ali":3, "ford":1}
    # dick = ensemble([dick1, dick2, dick3])
    # eff1 = effective(dick, dick1)
    # eff2 = effective(dick, dick2)
    # eff3 = effective(dick, dick3)
    # sorted_by_value = sorted(eff2.items(), key=lambda kv: kv[1], reverse=True)
    # print(sorted_by_value)
    # train = all_train([class1, class2, class3, class4, class5, class6])
    # test = all_test([class1, class2, class3, class4, class5, class6])
    # attributes = readingAttributes([attribute1, attribute2, attribute3, attribute4, attribute5, attribute6])

