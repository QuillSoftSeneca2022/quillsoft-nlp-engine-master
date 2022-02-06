from typing import List


class QSList(List):
    def __init__(self, value):
        self.value = value

    def MergeArrays(self, list1, list2):
        return list1 + sorted(set(list2) - set(list1))

    def JoinHyphenatedBlocks(self):
        num = 0
        while num < len(self.value) - 1:
            if self.value[num].rstrip().endswith("-"):
                self.value[num] = self.value[num].rstrip()[:-1] + self.value[num + 1]
                del self.value[num + 1]
                num -= 1
            num += 1

        return self.value

    def JoinHyphenatedParagraphs(self):
        num = 0
        while num < len(self.value) - 1:
            if self.value[num].endswith("-") or self.value[num].endswith("- "):
                self.value[num] = self.value[num].rstrip()[:-1] + self.value[num + 1]
                del self.value[num + 1]
                num -= 1
            num += 1

        return QSList(self.value)

    def JoinParagraphs(self):
        num = 0
        while num < len(self.value) - 1:
            if (not self.value[num].strip().endswith(".")) and not self.value[num + 1][0].isupper():
                self.value[num] += " " + self.value[num + 1]
                del self.value[num + 1]
                num -= 1
            num += 1

        return self.value

    def MergeSentences(self, list2):
        set_1 = set(self.value)
        set_2 = set(list2)

        list_2_items_not_in_list_1 = list(set_2 - set_1)
        merged_list = self.value + list_2_items_not_in_list_1

        return sorted(merged_list)

    def MergeDocumentSentences(self, list2):
        set_1 = dict(self.value)
        set_2 = dict(list2)

        # Merge dictionaries to filter duplicate keywords
        merged_set = {**set_1, **set_2}
        # Sort dictionary to descending list
        sorted_list = sorted(merged_set.items(), key=lambda kv: kv[1], reverse=True)
        return sorted_list

    def JoinSentences(self, list2):

        set_1 = set(self.value)
        set_2 = set(list2)

        list_2_items_not_in_list_1 = list(set_2 - set_1)
        joined_list = set_2 - set(list_2_items_not_in_list_1)

        return sorted(joined_list)
