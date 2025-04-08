class R_WMemory:
	memory = {}
	def __init__(self):
		self.memory = R_WMemory.memory
	#~you wont be able to use "pop" tonight~
	#damn, that top comment is cringe.
	def WMemory(self, index, write):
		if not write == "pop":
			self.memory[index] = write
		else:
			try:
				del self.memory[index]
			except KeyError:
				print("unable to delete key because it does not exist.")
	def RMemory(self,index):
		try:
			for _,item in self.memory.items():
				if item == self.memory[index]:
					return item
		except KeyError:
			print("index not found")
			return None
	def MemoryReturn(self):
		return self.memory
def class_finder(item):
	if type(item) == list:
	    return "list"
	elif type(item) == dict:
		return "dict"
	elif type(item) == str:
		return "str"
	elif type(item) == int:
		return "int"
	elif type(item) == float:
		return "float"
	else:
		return "unknown"

def list_unfold(list):
	unfolded_list = []
	for item in list:
		if class_finder(item) == "list":
			unfolded_list.extend(list_unfold(item))
		elif class_finder(item) == "dict":
			for _,item2 in item.items():
				unfolded_list.extend(list_unfold(item2))
		elif class_finder(item) == "str" or "int" or "float":
			unfolded_list.append(item)
	return unfolded_list
def list_compacter(list):
	compacted = []
	for item in list:
		if not item in compacted:
			compacted.append(item)