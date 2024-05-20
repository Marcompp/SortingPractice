sorting_algorithms = ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort", "Heap Sort","Counting Sort","Radix Sort","Bucket Sort","Tim Sort", "Shell Sort"]

def get_sorting_generator(algorithm_name, data):
    if algorithm_name == "Bubble Sort":
        return bubble_sort(data)
    elif algorithm_name == "Selection Sort":
        return selection_sort(data)
    elif algorithm_name == "Insertion Sort":
        return insertion_sort(data)
    elif algorithm_name == "Merge Sort":
        return merge_sort(data)
    elif algorithm_name == "Quick Sort":
        return quick_sort(data)
    elif algorithm_name == "Heap Sort":
        return heap_sort(data)
    elif algorithm_name == "Counting Sort":
        return counting_sort(data)
    elif algorithm_name == "Bucket Sort":
        return bucket_sort(data)
    elif algorithm_name == "Radix Sort":
        return radix_sort(data)
    elif algorithm_name == "Tim Sort":
        return tim_sort(data)
    elif algorithm_name == "Shell Sort":
        return shell_sort(data)
    else:
        raise ValueError("Unknown sorting algorithm")


def bubble_sort(data):
    """A generator to perform bubble sort, yielding the array at each step."""
    n = len(data)
    for i in range(n):
        for j in range(0, n-i-1):
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
            yield data

def selection_sort(data):
    """A generator to perform selection sort, yielding the array at each step."""
    n = len(data)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if data[min_idx] > data[j]:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
        yield data

def insertion_sort(data):
    """A generator to perform insertion sort, yielding the array at each step."""
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and key < data[j]:
            data[j + 1] = data[j]
            j -= 1
            yield data
        data[j + 1] = key
        yield data

def merge_sort(data):
    """A generator to perform merge sort, yielding the array at each step."""
    if len(data) > 1:
        mid = len(data) // 2
        left_half = data[:mid]
        right_half = data[mid:]

        # Recursively sort both halves
        yield from merge_sort(left_half)
        yield from merge_sort(right_half)

        i = j = k = 0

        # Merge the sorted halves
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                data[k] = left_half[i]
                i += 1
            else:
                data[k] = right_half[j]
                j += 1
            k += 1
            yield data

        # Check if any element was left
        while i < len(left_half):
            data[k] = left_half[i]
            i += 1
            k += 1
            yield data

        while j < len(right_half):
            data[k] = right_half[j]
            j += 1
            k += 1
            yield data


def quick_sort(data, low=0, high=None):
    """A generator to perform quick sort, yielding the array at each step."""
    if high is None:
        high = len(data) - 1

    if low < high:
        # Partition the array
        pi = yield from partition(data, low, high)
        
        # Recursively sort elements before partition and after partition
        yield from quick_sort(data, low, pi - 1)
        yield from quick_sort(data, pi + 1, high)


def partition(data, low, high):
    """Helper function to perform the partitioning for quick sort."""
    pivot = data[high]  # Pivot element is at the end
    i = low - 1  # Index of smaller element

    for j in range(low, high):
        if data[j] <= pivot:
            i += 1
            data[i], data[j] = data[j], data[i]
            yield data  # Yield after each swap

    data[i + 1], data[high] = data[high], data[i + 1]
    yield data  # Yield after final swap
    return i + 1

def heapify(data, n, i):
    """Heapify subtree rooted at index i."""
    largest = i  # Initialize largest as root
    l = 2 * i + 1  # Left child
    r = 2 * i + 2  # Right child

    # Check if left child exists and is greater than root
    if l < n and data[l] > data[largest]:
        largest = l

    # Check if right child exists and is greater than largest so far
    if r < n and data[r] > data[largest]:
        largest = r

    # Change root, if needed
    if largest != i:
        data[i], data[largest] = data[largest], data[i]
        yield data
        # Recursively heapify the affected sub-tree
        yield from heapify(data, n, largest)

def heap_sort(data):
    """A generator to perform heap sort, yielding the array at each step."""
    n = len(data)

    # Build a maxheap
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(data, n, i)

    # One by one extract elements
    for i in range(n - 1, 0, -1):
        data[i], data[0] = data[0], data[i]  # Swap
        yield data
        yield from heapify(data, i, 0)

def counting_sort(data):
    """A generator to perform counting sort, yielding the array at each step."""
    # Find the maximum element in the array
    max_element = max(data)
    # Initialize count array with zeros
    count = [0] * (max_element + 1)
    
    # Count the occurrences of each element in the input array
    for num in data:
        count[num] += 1
        # yield count

    # Reconstruct the sorted array using the count array
    sorted_data = []
    for i in range(len(count)):
        while count[i] > 0:
            sorted_data.append(i)
            count[i] -= 1
            yield sorted_data

def bucket_sort(data, num_buckets=10):
    """A generator to perform bucket sort, yielding the array at each step."""
    # Find the minimum and maximum elements in the array
    min_element = min(data)
    max_element = max(data)
    
    # Calculate the range of each bucket
    bucket_range = (max_element - min_element + 1) / num_buckets

    # Initialize empty buckets
    buckets = [[] for _ in range(num_buckets)]

    # Distribute elements into buckets
    for num in data:
        index = int((num - min_element) / bucket_range)
        if index == num_buckets:
            index -= 1
        buckets[index].append(num)
        yield concatenate_buckets(buckets)

    # Sort each bucket individually (using another sorting algorithm)
    for i in range(num_buckets):
        buckets[i].sort()
        yield concatenate_buckets(buckets)

    # Concatenate sorted buckets to produce the sorted array
    sorted_data = []
    for bucket in buckets:
        sorted_data.extend(bucket)
        yield sorted_data

def concatenate_buckets(buckets):
    allbuckets = []
    for bucket in buckets:
        allbuckets.extend(bucket)
    return allbuckets

def radix_sort(data, base=10):
    """A generator to perform radix sort, yielding the array at each step."""
    # Find the maximum number of digits in the input array
    max_digits = len(str(max(data)))
    
    # Iterate over each digit position, starting from the least significant digit
    for digit_index in range(max_digits):
        # Initialize empty buckets for each digit (0 to base-1)
        buckets = [[] for _ in range(base)]
        
        # Distribute elements into buckets based on the current digit
        for num in data:
            digit = (num // (base ** digit_index)) % base
            buckets[digit].append(num)
            yield concatenate_buckets(buckets)

        # Concatenate the buckets to update the data array
        data = [num for bucket in buckets for num in bucket]
        yield data

def tim_sort(data):
    """A generator to perform Tim Sort, yielding the array at each step."""
    # Define the minimum run size for insertion sort
    min_run = 32
    
    # Split the input array into runs using insertion sort
    for start in range(0, len(data), min_run):
        end = min(start + min_run, len(data))
        insertion_sort_aux(data, start, end)
        yield data

    # Merge adjacent runs to produce sorted subarrays of size 2*min_run
    size = min_run
    while size < len(data):
        for start in range(0, len(data), 2*size):
            mid = min(len(data), start + size)
            end = min(len(data), start + 2*size)
            merge(data, start, mid, end)
            yield data
        size *= 2

def insertion_sort_aux(data, start, end):
    """Insertion sort algorithm."""
    for i in range(start + 1, end):
        key = data[i]
        j = i - 1
        while j >= start and data[j] > key:
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key

def merge(data, start, mid, end):
    """Merge function for merging two sorted subarrays."""
    left = data[start:mid]
    right = data[mid:end]
    i = j = 0
    k = start
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            data[k] = left[i]
            i += 1
        else:
            data[k] = right[j]
            j += 1
        k += 1
    while i < len(left):
        data[k] = left[i]
        i += 1
        k += 1
    while j < len(right):
        data[k] = right[j]
        j += 1
        k += 1

def shell_sort(data):
    """A generator to perform Shell Sort, yielding the array at each step."""
    # Start with a large gap, then reduce the gap
    n = len(data)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = data[i]
            j = i
            # Move elements that are gap apart until correct position is found
            while j >= gap and data[j - gap] > temp:
                data[j] = data[j - gap]
                j -= gap
                yield data
            data[j] = temp
        gap //= 2  # Reduce the gap
    yield data  # Yield the sorted array at the end