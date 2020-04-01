

class CommonUtils():

    @staticmethod
    def remove_duplicates_from_list(duplicates):
        final_list = []
        for item in duplicates:
            if item not in final_list:
                final_list.append(item)
        return final_list
