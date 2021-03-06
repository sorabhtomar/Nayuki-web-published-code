# 
# Disjoint-set data structure - Library (Python)
# 
# Copyright (c) 2015 Project Nayuki
# https://www.nayuki.io/page/disjoint-set-data-structure
# 
# (MIT License)
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# - The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
# - The Software is provided "as is", without warranty of any kind, express or
#   implied, including but not limited to the warranties of merchantability,
#   fitness for a particular purpose and noninfringement. In no event shall the
#   authors or copyright holders be liable for any claim, damages or other
#   liability, whether in an action of contract, tort or otherwise, arising from,
#   out of or in connection with the Software or the use or other dealings in the
#   Software.
# 


# Represents a set of disjoint sets. Also known as the union-find data structure.
# Main operations are querying if two elements are in the same set, and merging two sets together.
# Useful for testing graph connectivity, and is used in Kruskal's algorithm.
class DisjointSet(object):
	
	# Constructs a new set containing the given number of singleton sets.
	# For example, DisjointSet(3) --> {{0}, {1}, {2}}.
	def __init__(self, numElems):
		if numElems <= 0:
			raise ValueError("Number of elements must be positive")
		
		# A global property
		self.numSets = numElems
		
		# Per-node properties (three):
		# The index of the parent element. An element is a representative iff its parent is itself.
		self.parents = list(range(numElems))
		# Always in the range [0, floor(log2(numElems))].
		self.ranks = [0] * numElems
		# Positive number if the element is a representative, otherwise zero.
		self.sizes = [1] * numElems
	
	
	# Returns the number of elements among the set of disjoint sets; this was the number passed
	# into the constructor and is constant for the lifetime of the object. All the other methods
	# require the argument elemIndex to satisfy 0 <= elemIndex < get_num_elements().
	def get_num_elements(self):
		return len(self.parents)
	
	
	# Returns the number of disjoint sets overall. This number decreases monotonically as time progresses;
	# each call to merge_sets() either decrements the number by one or leaves it unchanged.
	def get_num_sets(self):
		return self.numSets
	
	
	# (Private) Returns the representative element for the set containing the given element. This method is also
	# known as "find" in the literature. Also performs path compression, which alters the internal state to
	# improve the speed of future queries, but has no externally visible effect on the values returned.
	def _get_repr(self, elemIndex):
		if elemIndex < 0 or elemIndex >= len(self.parents):
			raise IndexError()
		# Follow parent pointers until we reach a representative
		parent = self.parents[elemIndex]
		if parent == elemIndex:
			return elemIndex
		while True:
			grandparent = self.parents[parent]
			if grandparent == parent:
				return parent
			self.parents[elemIndex] = grandparent  # Partial path compression
			elemIndex = parent
			parent = grandparent
	
	
	# Returns the size of the set that the given element is a member of. 1 <= result <= get_num_elements().
	def get_size_of_set(self, elemIndex):
		return self.sizes[self._get_repr(elemIndex)]
	
	
	# Tests whether the given two elements are members of the same set. Note that the arguments are orderless.
	def are_in_same_set(self, elemIndex0, elemIndex1):
		return self._get_repr(elemIndex0) == self._get_repr(elemIndex1)
	
	
	# Merges together the sets that the given two elements belong to. This method is also known as "union" in the literature.
	# If the two elements belong to different sets, then the two sets are merged and the method returns True.
	# Otherwise they belong in the same set, nothing is changed and the method returns False. Note that the arguments are orderless.
	def merge_sets(self, elemIndex0, elemIndex1):
		# Get representatives
		repr0 = self._get_repr(elemIndex0)
		repr1 = self._get_repr(elemIndex1)
		if repr0 == repr1:
			return False
		
		# Compare ranks
		cmp = self.ranks[repr0] - self.ranks[repr1]
		if cmp == 0:  # Increment repr0's rank if both nodes have same rank
			self.ranks[repr0] += 1
		elif cmp < 0:  # Swap to ensure that repr0's rank >= repr1's rank
			repr0, repr1 = repr1, repr0
		
		# Graft repr1's subtree onto node repr0
		self.parents[repr1] = repr0
		self.sizes[repr0] += self.sizes[repr1]
		self.sizes[repr1] = 0
		self.numSets -= 1
		return True
	
	
	# For unit tests. This detects many but not all invalid data structures, raising an AssertionError
	# if a structural invariant is known to be violated. This always returns silently on a valid object.
	def check_structure(self):
		numRepr = 0
		for i in range(len(self.parents)):
			parent = self.parents[i]
			rank = self.ranks[i]
			size = self.sizes[i]
			isRepr = parent == i
			if isRepr:
				numRepr += 1
			
			ok = True
			ok &= 0 <= parent < len(self.parents)
			ok &= 0 <= rank and (isRepr or rank < self.ranks[parent])
			ok &= ((not isRepr) and size == 0) or (isRepr and size >= (1 << rank))
			if not ok:
				raise AssertionError()
		if not (1 <= self.numSets == numRepr <= len(self.parents)):
			raise AssertionError()
