special_character = [",", "–", ";", ":", '''"''', "(", ")", "?", "!", "..."]
special_character = set(special_character)


def split_compare_sentences(_sen):
    array = []
    cur_pos = 0
    i = 0
    while i < len(_sen):
        if _sen[i] == " ":
            array.append(_sen[cur_pos: i])
            cur_pos = i
        elif _sen[i] == "_":
            array.append(_sen[cur_pos: i])
            cur_pos = i
        i += 1
    array.append(_sen[cur_pos:])
    return array


def result_compare_sentences(sentences1, sentences2):
    sentences1 = split_compare_sentences(sentences1)
    sentences2 = split_compare_sentences(sentences2)

    i = 0
    result = 0
    while i < len(sentences1):
        if sentences1[i][0] == "_":
            cur_sentences = [sentences1[i - 1], sentences1[i]]
            if i + 1 < len(sentences1):
                if sentences1[i + 1][0] == "_":
                    cur_sentences.append(sentences1[i + 1])
                    if i + 2 < len(sentences1):
                        if sentences1[i + 2][0] == "_":
                            cur_sentences.append(sentences1[i + 2])

            compare_sentences = []
            for j in range(i - 1, i - 1 + len(cur_sentences)):
                compare_sentences.append(sentences2[j])

            if cur_sentences == compare_sentences:
                result += 1
            i += len(cur_sentences) - 1
        i += 1
    return result


GoldResult = open("GoldDataTachTay.txt", mode="r", encoding="utf-8").read().splitlines()
VnCoreNlpResult = open("VnCoreNlpResult.txt", mode="r", encoding="utf-8").read().splitlines()
TachTuWFST = open("TachTuWFSTResult.txt", mode="r", encoding="utf-8").read().splitlines()
TachTuMXM = open("TachTuMXMResult.txt", mode="r", encoding="utf-8").read().splitlines()
sum_score_vncore = 0
sum_score_tachtu_MXM = 0
sum_score_tachtu_WFST = 0
for i in range(0, len(GoldResult)):
    sum_score_vncore += result_compare_sentences(GoldResult[i], VnCoreNlpResult[i])
    sum_score_tachtu_MXM += result_compare_sentences(GoldResult[i], TachTuMXM[i])
    sum_score_tachtu_WFST += result_compare_sentences(GoldResult[i], TachTuWFST[i])

max_score = 0
for item in GoldResult:
    item = item.split(" ")
    for j in item:
        if j.count("_") > 0:
            max_score += 1

print("Xác suất phương pháp maximum Matching: " + str(sum_score_tachtu_MXM / max_score * 100))
print("Xác suất phương pháp tách từ WFST : " + str(sum_score_tachtu_WFST / max_score * 100))
print("Xác suất phương pháp VncoreNLP: " + str(sum_score_vncore / max_score * 100))
