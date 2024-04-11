import math
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
