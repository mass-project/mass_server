class ListFunctions:
    @staticmethod
    def merge_lists_without_duplicates(list1, list2):
        return list(set(list1)|set(list2))