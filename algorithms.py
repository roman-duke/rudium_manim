import math
import random
# File for first implementing the algorithms before animating with manim
# BINARY SEARCH ALGORITHM

def binary_search(array, target):
  # two initial extremeties
  min = 0
  max = len(array) - 1

  def search_helper(min, max):      
    # generate random guess and check if guess is equal to target
    index = math.floor((min + max) / 2)

    if (array[index] == target):
      return f"Target, {target} found at index --> {index}"

    elif (array[index] < target):
      min = index + 1
      return search_helper(min, max)
    
    else:
      max = index - 1
      return search_helper(min, max)

  return search_helper(min, max)

# print(binary_search([1, 2, 3, 5, 9, 15], 3))

# QUICK SORT ALGORITHM
# def qsort(array):
#   if len(array) < 2:
#     return array
  
#   rand_index = random.randint(0, len(array) - 1)
#   pivot = array.pop(rand_index)

#   left_sub_array, right_sub_array = [], []

#   for i in array:
#     if pivot <= i: right_sub_array.append(i)
#     else: left_sub_array.append(i)

#   return qsort(left_sub_array) + [pivot] + qsort(right_sub_array)

# Code refactor using list comprehension
def qsort(array):
  if len(array) < 2:
    return array
  
  rand_index = random.randint(0, len(array) - 1)
  pivot = array.pop(rand_index)

  left_sub_array = [i for i in array if pivot >= i]
  right_sub_array = [i for i in array if pivot < i]

  return qsort(left_sub_array) + [pivot] + qsort(right_sub_array)

# print(qsort([5, 12, 3, 9, 31]))

# BREADTH-FIRST SEARCH
graph = {
  "you": ["bob", "claire", "alice"],
  "bob": ["anuj", "peggy"],
  "alice": ["peggy"],
  "claire": ["thom", "jonny"],
  "anuj": [],
  "peggy": [],
  "thom": [],
  "jonny": []
}

# iterative approach
def bfs(name):
  queue = [*graph[name]]
  while len(queue) > 0:
    if mango_seller(queue[0]):
      return f"Mango seller found --> {queue[0]}"
    else:
      queue.extend(graph[queue[0]])
      queue.pop(0)


def mango_seller(name):
  return True if "m" in name else False

print(bfs("you"))
