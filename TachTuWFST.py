import math
import sys
import re
from decimal import Decimal

special_character = [",", "–", ";", ":", '''"''', "(", ")", "?", "!", "..."]
special_character = set(special_character)


def split_sentences(_sentences):
    _sentences = _sentences.strip().split()
    if "" in _sentences:
        _sentences.remove("")
    return _sentences


def split_special_character(sentences):
    final_array = []
    cur = 0
    i = 0

    while i < len(sentences):
        # nếu phát hiện ra dấu câu thì tách
        if sentences[i] in special_character:
            # xử lí trường hợp tường thuật
            if sentences[i] == ":":
                if sentences[i + 1] == " ":
                    sentences = sentences[:i + 1] + sentences[i + 2:]
            # check xem dấu chấm than có nằm cuối câu không
            if not (sentences[i] == "!" and i != len(sentences) - 1):
                left = sentences[cur:i].strip().split(" ")
                # trường hợp dấu câu dạng :"
                if left[0] != "":
                    final_array.append(left)
                final_array.append(sentences[i])
                cur = i + 1
        i = i + 1
    # nếu không có dấu câu ở cuối
    if cur < len(sentences):
        left = sentences[cur:i].strip().split(" ")
        final_array.append(left)
    return final_array


def train_data(train_folder):
    f = open("dictionary.txt", mode="r", encoding="utf-8").read().splitlines()
    dictionary = {}
    for item in f:
        item = item.replace(" ", "_")
        dictionary.update({item: 1})

    # print(dictionary)
    train = open(train_folder, mode="r", encoding="utf-8").read().splitlines()
    for item in train:
        item = split_sentences(item)
        for word in item:

            if word in dictionary:
                dictionary.update({word: dictionary[word] + 1})
            else:

                dictionary.update({word: 1})

    len_dictionary = len(dictionary)
    for item in dictionary:
        dictionary.update({item: -Decimal(math.log2(Decimal(dictionary[item]) / len_dictionary))})
    return dictionary


def split_sen(_sen):
    len_dictionary = len(dictionary)

    def split_single_sentences(test_case):
        def all_possible_sentences(i, array, length_case, S):

            if i + 4 > len(test_case):
                end = len(test_case)
            else:
                end = i + 4
            for j in range(i, end):
                cur_words = "_".join(test_case[i:j + 1])

                if cur_words in dictionary or j - i == 0:
                    # check trường hợp viết hoa, tương tự như phương pháp mxm matching check xem từ đầu có nằm trong từ điển và không chứa số
                    if not (cur_words.istitle() and test_case[i].lower() in dictionary and re.search("\d",
                                                                                                     cur_words)):
                        S.append(cur_words)

                        length_case += j - i + 1
                        if length_case < len(test_case):
                            all_possible_sentences(j + 1, array, length_case, S)
                        else:
                            array.append(S.copy())

                        S.pop()
                        length_case -= j - i + 1
            return array

        final_arr = all_possible_sentences(0, [], 0, [])
        # for item in final_arr:
        #     print(item)
        min_value = sys.maxsize
        final_sentences = []
        for item in final_arr:
            value = 0
            for word in item:
                if word in dictionary:
                    value += dictionary[word]
                else:
                    value += -Decimal(math.log2(1 / len_dictionary))

            if value < min_value:
                min_value = value
                final_sentences = item

        return final_sentences

    input_test_case = _sen

    input_test_case = split_special_character(input_test_case)

    # Xử lí in hoa sau :" hay ở đầu câu
    if len(input_test_case[0]) > 1:
        if not input_test_case[0][1].istitle():
            input_test_case[0][0] = input_test_case[0][0][0].lower() + input_test_case[0][0][1:]
    for i in range(1, len(input_test_case) - 1):
        if input_test_case[i] == '''"''' and input_test_case[i - 1] == ":":
            if not input_test_case[i + 1][1].istitle():
                input_test_case[i + 1][0] = input_test_case[i + 1][0][0].lower() + input_test_case[i + 1][0][1:]

    result = []
    for item in input_test_case:
        if isinstance(item, list):
            cur_arr = split_single_sentences(item)
            for i in cur_arr:
                result.append(i)
        else:
            result.append(item)

    # Trả lại in hoa chữ cái đầu
    result[0] = result[0][0].upper() + result[0][1:]
    for i in range(1, len(result) - 1):
        if result[i] == '''"''' and result[i - 1] == ":":
            result[i + 1] = result[i + 1][0].upper() + result[i + 1][1:]
    return result


All_sentences = open("TestDataTachTay.txt", mode="r", encoding="utf-8").read().splitlines()
dictionary = train_data("TrainDataTachTay.txt")
for item in All_sentences:
    # Tách từ tự động cho câu bằng hàm split_string
    arr = split_sen(item)
    print(*arr)
