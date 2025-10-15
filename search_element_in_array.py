ex_data = [1, 2, 3, 45, 356, 569, 600, 705, 923]


def find_element(element, sorted_numbers=ex_data):
    """Находит индекс element в отсортированном списке sorted_numbers."""
    left = 0
    right = len(sorted_numbers)
    while left < right:
        mid = (left + right) // 2
        if sorted_numbers[mid] == element:
            return element
        if sorted_numbers[mid] < element:
            left = mid + 1
        else:
            right = mid
    return None


def search(number: id) -> bool:
    return True if find_element(number) else False


print(search(378))
