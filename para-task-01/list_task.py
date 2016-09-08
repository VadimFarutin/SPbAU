# Remove equal adjacent elements
#
# Example input: [1, 2, 2, 3]
# Example output: [1, 2, 3]
def remove_adjacent(lst):
    new_lst = [lst[0]]
    for i in range(1, len(lst)):
        if lst[i] != lst[i - 1]:
            new_lst.append(lst[i])
    return new_lst


# Merge two sorted lists in one sorted list in linear time
#
# Example input: [2, 4, 6], [1, 3, 5]
# Example output: [1, 2, 3, 4, 5, 6]
def linear_merge(lst1, lst2):
    new_lst = []
    i = 0
    j = 0
    max_elem = max(lst1[-1], lst2[-1]) + 1
    lst1.append(max_elem)
    lst2.append(max_elem)
    len1 = len(lst1)
    len2 = len(lst2)
    for k in range(len1 + len2 - 2):
        if lst1[i] < lst2[j]:
            new_lst.append(lst1[i])
            i += 1
        else:
            new_lst.append(lst2[j])
            j += 1
    return new_lst
