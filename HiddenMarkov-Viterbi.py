from decimal import *

train_data = open("HiddenMarkovTag.txt", mode="r", encoding="utf-8").read().splitlines()

hidden_set = set()
observer_set = set()
train_observer = []
train_hidden = []

for i in range(0, len(train_data)):
    temp = train_data[i].strip().split(" ")
    train_observer.append([])
    train_hidden.append([])
    for j in temp:
        word = j.split("/")

        observer_set.add(word[0].lower())
        hidden_set.add(word[1])
        train_observer[i].append(word[0].lower())
        train_hidden[i].append(word[1])

hidden_set = list(hidden_set)
hidden_set.sort()
hidden_list = ["S"] + hidden_set
observer_list = list(observer_set)
observer_list.sort()
observer_list.append("unk1")
observer_list.append("unk2")
list_map_pos_A = {}
list_map_pos_B = {}

# create matrix A
matrix_A = []
for i in range(0, len(hidden_list)):
    matrix_A.append([Decimal(1)])
    for j in range(1, len(hidden_list)):
        matrix_A[i].append(Decimal(1))
        list_map_pos_A.update({(hidden_list[i], hidden_list[j]): (i, j - 1)})

for item in train_hidden:
    matrix_A[list_map_pos_A[("S", item[0])][0]][list_map_pos_A[("S", item[0])][1]] += 1
    for i in range(0, len(item) - 1):
        cur_pos = list_map_pos_A[(item[i], item[i + 1])]
        matrix_A[cur_pos[0]][cur_pos[1]] += 1

len_item = len(matrix_A[0])
for i in range(0, len(matrix_A)):
    matrix_A[i][len_item - 1] = sum(matrix_A[i][0:len_item - 1])
for i in range(0, len(matrix_A)):
    for j in range(0, len_item - 1):
        matrix_A[i][j] = matrix_A[i][j] / matrix_A[i][len_item - 1]
    matrix_A[i].pop()

# create matrix B
matrix_B = []

for i in range(1, len(hidden_list)):
    matrix_B.append([Decimal(1)])
    for j in range(0, len(observer_list)):
        matrix_B[i - 1].append(Decimal(1))
        list_map_pos_B.update({(hidden_list[i], observer_list[j]): (i - 1, j)})

for i in range(0, len(train_observer)):
    for j in range(0, len(train_observer[i])):
        cur_pos = list_map_pos_B[(train_hidden[i][j], train_observer[i][j])]
        matrix_B[cur_pos[0]][cur_pos[1]] += 1

len_item = len(matrix_B[0])
for i in range(0, len(matrix_B)):
    matrix_B[i][len_item - 1] = sum(matrix_B[i][0:len_item - 1])
for i in range(0, len(matrix_B)):
    for j in range(0, len_item - 1):
        matrix_B[i][j] = matrix_B[i][j] / matrix_B[i][len_item - 1]
    matrix_B[i].pop()


# for item in matrix_A:
#     print(item)
# print()
# for item in matrix_B:
#     print(item)


# viterbi


# sentences = ["mới", "thông_báo", "thời_gian", "học"]
def viterbi_sentences(sentences):
    sentences = sentences.split(" ")
    copy_sentences = sentences.copy()
    unk_pos = "1"
    for i in range(0, len(sentences)):
        sentences[i] = sentences[i].lower()
        if sentences[i] not in observer_set:
            sentences[i] = "unk" + unk_pos
            unk_pos = str(int(unk_pos) + 1)

    len_row = len(matrix_B)
    len_col = len(sentences)

    matrix_probability = [[Decimal(0) for col in range(len_col)] for row in range(len_row)]
    matrix_pointer = [["" for col in range(len_col)] for row in range(len_row)]

    # first probability from S (start) to first word
    for i in range(len_row):
        cur_pos_B = list_map_pos_B[(hidden_list[i + 1], sentences[0])]
        cur_pos_A = list_map_pos_A[("S", hidden_list[i + 1])]
        matrix_probability[i][0] = matrix_A[cur_pos_A[0]][cur_pos_A[1]] * matrix_B[cur_pos_B[0]][cur_pos_B[1]]
        matrix_pointer[i][0] = "S"

    for k in range(1, len(sentences)):
        for i in range(len_row):
            max_probability = 0
            for j in range(len_row):
                cur_pos_B = list_map_pos_B[(hidden_list[i + 1], sentences[k])]
                cur_pos_A = list_map_pos_A[(hidden_list[j + 1], hidden_list[i + 1])]
                cur_prob = matrix_probability[j][k - 1] * matrix_A[cur_pos_A[0]][cur_pos_A[1]] * matrix_B[cur_pos_B[0]][
                    cur_pos_B[1]]
                if cur_prob > max_probability:
                    max_probability = cur_prob
                    matrix_probability[i][k] = max_probability
                    matrix_pointer[i][k] = hidden_list[j + 1]

    # for item in matrix_probability:
    #     print(item)
    #
    # for item in matrix_pointer:
    #     print(item)
    # get result
    list_map_final_result = {}
    for i in range(1, len(hidden_list)):
        list_map_final_result.update({hidden_list[i]: i - 1})

    max_final = 0
    final_pos = 1
    for i in range(len_row):
        cur_val = matrix_probability[i][len_col - 1]
        if cur_val > max_final:
            final_pos = i + 1
            max_final = cur_val

    final_result = [hidden_list[final_pos]]

    for i in range(0, len_col):
        final_result.append(matrix_pointer[list_map_final_result[final_result[i]]][len_col - i - 1])

    final_result.pop()
    final_result.reverse()
    # for item in matrix_probability:
    #     print(item)

    for i in range(0, len(sentences)):
        final_result[i] = [copy_sentences[i]] + [final_result[i]]
    return final_result


data = open("TrainDataTachTay.txt", mode="r", encoding="utf-8").read().splitlines()
