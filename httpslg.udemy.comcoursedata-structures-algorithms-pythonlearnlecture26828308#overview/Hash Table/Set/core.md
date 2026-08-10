
---

# Introduction to Sets

## 1. What are Sets?
Sets are similar to dictionaries, except that instead of having key/value pairs, they only have the **keys** but not the values.

### Key Characteristics:
* **Implementation:** Like dictionaries, they are implemented using a **hash table**.
* **Uniqueness:** Sets can only contain unique elements (meaning that duplicates are not allowed).
* **Use Cases:** They are useful for various operations such as:
    * Finding the distinct elements in a collection.
    * Performing set operations such as union and intersection.

---

## 2. Defining a Set
Sets can be defined by either using curly braces `{}` or the built-in `set()` function.

```python
# Create a set using {}
my_set = {1, 2, 3, 4, 5} 

# Create a set using set()
my_set = set([1, 2, 3, 4, 5])
```

---

## 3. Common Set Operations
Once a set is defined, you can perform various operations on it, such as adding or removing elements, finding the union, intersection, or difference of two sets, and checking membership.

### Adding and Updating
```python
# Add an element to a set
# If the number 6 is already in the set, it will not be added again.
my_set.add(6) 

# Update is used to add multiple elements to the set at once. 
# It takes an iterable object (e.g., list, tuple, set) as an argument.
my_set.update([3, 4, 5, 6]) 
```

### Removing Elements
```python
# Removing an element from a set
my_set.remove(3) 
```

### Set Mathematics
Given two sets, `my_set` and `other_set`:

```python
other_set = {3, 4, 5, 6}

# Union: All elements from both sets
union_set = my_set.union(other_set) 

# Intersection: Elements present in both sets
intersection_set = my_set.intersection(other_set) 

# Difference: Elements in my_set that are NOT in other_set
difference_set = my_set.difference(other_set) 
```

### Membership Testing
Checking if a given element is a member of a set using the `in` keyword.

```python
if "hello" in my_set:
    print("Found hello in my_set")
```

---

**Next Step:** Now let's look at some common coding interview questions that use sets!
