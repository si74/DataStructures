import sys
import collections

#Implement a Trie with a WildCard to Store all Available Words
class TrieNode:
	def __init__(self, value):
		self.value = value
		self.endNode = False
		self.children = {}

	def addChild(self,TrieNode):
		self.children[TrieNode.value] = TrieNode

class Trie:
	def __init__(self):
		self.rootNode = TrieNode(None)

	#value is array of values
	def insertNode(self,value):
		currentNode = self.rootNode
		for index,v in enumerate(value):
			if v not in currentNode.children:
				newNode = TrieNode(v)
				if (index == len(value) - 1):
					newNode.endNode = True
				currentNode.children[v] = newNode
				currentNode = newNode
			else:
				currentNode = currentNode.children[v]

	#
	def searchString(self,string):
		nodesToSearch = self.rootNode
		self.tempResults = []
		self.searchUtil(self.rootNode,string,'',-1,len(string)-1)
		return self.bestPath(self.tempResults,len(string))

	def searchUtil(self,TrieNode,string,currentPath,index,end):
		#if we've reached end of string
		if index == end:
			if TrieNode.endNode:
				self.tempResults.append(currentPath)
			return
		toVisit = []
		index += 1
		for key,value in TrieNode.children.iteritems():
			if key in [string[index],'*']:
				toVisit.append(value)
		for node in toVisit:
			newPath = currentPath + node.value + ","
			self.searchUtil(node,string,newPath,index,end)
		return

	#function to obtain edit distance 
	def bestPath(self,results,length):
		if not results:
			return 'NO MATCH'
		if len(results) == 1:
			return results[0].rstrip(",")

		#first compare Wildcard counts
		patterns = {}
		for r in results:
			count = r.count('*')
			if count in patterns.keys():
				patterns[count].append(r)
			else:
				patterns[count] = [r] 

		#grab the results with fewest wildcards
		bestPatterns = patterns[min(patterns)]
		if (len(bestPatterns)) == 1:
			return bestPatterns[0].rstrip(",")

		#if more than one of lowest wildcard count compare the wildcard score
		bestPatternArray = [x.rstrip(",").split(",") for x in bestPatterns]
		finalCount = 0
		finalPattern = ''
		for p in bestPatternArray:
			tempCount = 0
			for index,value in enumerate(p):
				if value is '*':
					tempCount += index
			if tempCount > finalCount:
				finalCount = tempCount
				finalPattern = p
	
		return ",".join(finalPattern)

	#functions to check that this is correct
	def printTrie(self):
		self.printUtil(self.rootNode)

	def printUtil(self,TrieNode):
		for key,value in TrieNode.children.iteritems():
			print key
			self.printUtil(value)


if __name__ == "__main__":

	patternTrie = Trie()
	paths = []

	numcount = 0

	#read in the input file
	for line in sys.stdin:
		l = line.rstrip('\n')
		if l.isdigit(): 
			numcount += 1	
		else:
			if numcount == 1:
				patternTrie.insertNode(l.split(','))
			else:
				paths.append(l.strip('/').split('/'))

	for i in paths:
		print patternTrie.searchString(i).rstrip(',')
