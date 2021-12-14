# Phương pháp Maximum Matching
import re

f = open("dictionary.txt", mode="r", encoding="utf-8").read().splitlines()

dictionary = set(f)

train = open("TrainDataTachTay.txt", mode="r", encoding="utf-8").read().splitlines()
for item in train:
    item = item.strip().split()
    if "" in item:
        item.remove("")
    for word in item:
        word = word.replace("_", " ")
        dictionary.add(word)

# Dấu gạch ngang – khác dấu gạch nối -
special_character = [",", "–", ";", ":", '''"''', "(", ")", "?", "!", "..."]
special_character = set(special_character)


# oa, oe, uy được ký âm bằng ký hiệu ngữ âm quốc tế là /wa/, /wɛ/, /wi/ nên phải bỏ dấu vào chữ a, e và y
# nguồn: https://vi.wikipedia.org/wiki/Quy_t%E1%BA%AFc_%C4%91%E1%BA%B7t_d%E1%BA%A5u_thanh_trong_ch%E1%BB%AF_qu%E1%BB%91c_ng%E1%BB%AF

# Phân tách câu bằng khoảng trắng và các kí tự đặc biệt
def split_sentences(sentences):
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

                if left[0] != "":

                    for item in left:
                        final_array.append(item)
                final_array.append(sentences[i])
                cur = i + 1
        i = i + 1
    # nếu không có dấu câu từ vị trí split trước đó về cuối
    if cur < len(sentences):
        left = sentences[cur:i].strip().split(" ")
        for item in left:
            final_array.append(item)
    return final_array


# Nối từ bằng phương pháp Maximum Matching
def split_string(string):
    array = split_sentences(string)
    i = 0
    pos = 4
    final_arr = []
    while i < len(array):
        while True:
            cur_string = " ".join(array[i:i + pos])
            # khi chỉ còn 1 từ
            if pos == 1:
                break
            # Nếu chứa kí tự đặc biệt thì bỏ qua
            if not re.search("[,()–:;.?!\"]", cur_string):
                # Check Danh từ riêng, tất cả các từ bắt đầu bằng chữ cái viết hoa và không chứa số
                if cur_string.istitle() and not re.search("\d", cur_string):
                    # check xem có nằm đầu dòng không. Hoặc nằm sau dấu  ? or !
                    if i == 0:
                        # nếu từ nằm đầu dòng có trong từ điển thì tách ra. tuy nhiên cách này cũng k bao phủ tất cả trường hợp, ví dụ trong tên riêng từ đầu có trong từ điển
                        if array[i].lower() in dictionary:
                            final_arr.append(array[i])
                            cur_string = " ".join(array[i + 1:i + pos])

                    i = i + pos - 1
                    break
                # check xem tiếng có nằm trong từ điển
                if cur_string.lower() in dictionary:
                    i = i + pos - 1
                    break
            pos = pos - 1
        final_arr.append(cur_string.replace(" ", "_"))
        pos = 4
        i = i + 1
    return final_arr


# Lấy data từ file TongHopCau làm bộ thử
All_sentences = open("TestDataTachTay.txt", mode="r", encoding="utf-8").read().splitlines()
for item in All_sentences:
    # Tách từ tự động cho câu bằng hàm split_string
    arr = split_string(item)
    print(*arr)
