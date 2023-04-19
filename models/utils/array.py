from typing import List, Union


def remove_items(ls: List[str], indexes: List[int]) -> List[str]:
    if len(indexes) == 0:
        return ls
    rt_ls = []
    ignore_idx = indexes.pop(0)
    for i, item in enumerate(ls):
        if i == ignore_idx:
            if len(indexes) > 0:
                ignore_idx = indexes.pop(0)
            else:
                ignore_idx = -1
            continue
        else:
            rt_ls.append(item)

    return rt_ls


def add_items(ls: List[str], indexes: List[int], words: List[str]) -> List[str]:
    if len(indexes) > 0:
        rt_ls = []
        add_idx = indexes.pop(0)
        add_word = words.pop(0)
        for i, item in enumerate(ls):
            if i == add_idx:
                rt_ls.append(add_word)
                if len(indexes) > 0:
                    add_idx = indexes.pop(0)
                    add_word = words.pop(0)
                else:
                    add_idx = -1
            rt_ls.append(item)

        return rt_ls
    else:
        return ls


def flatten(ls: List[Union[List[str], str]]) -> List[str]:
    rt_ls = []
    for token in ls:
        if type(token) == str:
            rt_ls.append(token)
        else:
            for t in token:
                rt_ls.append(t)
    return rt_ls


if __name__ == "__main__":
    items = [1, 2, 3, 4, 5]
    rm = [1, 3]
    print(remove_items(items, rm))
    add = [1]
    w = [6]
    print(add_items(items, add, w))
