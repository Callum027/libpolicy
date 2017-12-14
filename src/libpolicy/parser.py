bindings = {}
policies = []
class Service:
	protocols = []
	def add_protocol(self,prot):
		self.protocols.append(prot)
	def set_name(self,name):
		self.name = name
		
class Protocol:
	def set_data(self,data):
		self.data = data
	
class Group:
	members = []
	def add_member(self,member):
		self.members.append(member)
	def set_name(self,name):
		self.name = name
		
class Entity:
	attribs = []
	def set_name(self,name):
		self.name = name
	def add_attrib(self,attrib):
		self.attribs.append(attrib)
	#todo service group vs group service?  issue 3
		
class PacketAttrib:
	def set_name(self,name):
		self.name = name
	def set_attrib(self,attrib):
		self.attrib = attrib

class Policy:
	def set_name(self,name):
		self.name = name
	def set_action(self,action):
		self.action = action
	def set_sub(self,sub):
		self.sub = sub
	def set_obj(self,obj):
		self.obj = obj
	def set_app(self,app):
		self.app = app
		
def start(file):
	src_file = open(file,"r")
	line  = src_file.readline()
	while line:
		line = line.strip()
		print line
		if line == '' or line[0] == '#':
			# print "commnet"
			pass
		else :
			tokens = line.split()
			if tokens[0] == "service":
				parseService(tokens)
			elif tokens[0] == "group":
				parseGroup(tokens)
			elif tokens[0] == "entity":
				parseEntity(tokens)
			elif tokens[0] == "policy":
				parsePolicy(tokens)
		line = src_file.readline()
	
def parseService(line):
	if line[0] != "service":
		print line
		raise Exception("parseService called but line not a service")
	else:
		service_obj = Service()
		service_obj.set_name(line[1])
		protocol_obj = Protocol()
		protocol_obj.set_data(line[2]+line[3]) #TODO refer to issue 1 for number of protocol tokens
		service_obj.add_protocol(protocol_obj)
		bindings[line[1]] = service_obj
	
def parseGroup(line):
	if line[0] != "group":
		print line
		raise Exception("parseGroup called but line not a service")
	else:
		group_obj = Group()
		group_obj.set_name(line[1])
		#group_type = line[2] #TODO thrown away? refer to issue 2
		if line[2] != "{":
			print line
			raise Exception("Group members not found")
		cur_index = 3
		while cur_index < len(line):
			if line[cur_index]=="}":
				break
			else:
				group_obj.add_member(bindings[line[cur_index]])
			cur_index = cur_index+1
		if line[cur_index] != "}":
			print line
			raise Exception("Unclosed brackets")
		bindings[line[1]] = group_obj
		#print bindings["www"]
		
def parseEntity(line):
	if line[0] != "entity":
		print line
		raise Exception("parseEntity called but line not a entity")
	else:
		entity_name = line[1]
		if entity_name in bindings:
			entity_obj = bindings[line[1]]
		else:
			entity_obj = Entity()
			entity_obj.set_name(line[1])
			bindings[line[1]] = entity_obj
		
		if line[2] == "group":
			entity_obj.add_attrib(bindings[line[3]])
		else:
			entity_attrib = parseEntityAttrib(line[2:])
			entity_obj.add_attrib(entity_attrib)
		
def parseEntityAttrib(subline):
	print subline
	if subline[0] == "service" or subline[0] == "group": #todo fix this 
		service_name = subline[2]
		service_obj = bindings[service_name]
		return service_obj
	else:
		packet_attrib = PacketAttrib()
		packet_attrib.set_name(subline[0])
		packet_attrib.set_attrib(subline[1])
		return packet_attrib
		
def parsePolicy(line):
	if line[0] != "policy":
		print line
		raise Exception("parsePolicy called but line not a policy")
	else:
		policy_obj = Policy()
		policy_obj.set_name(line[1])
		policy_obj.set_action(line[2])
		policy_obj.set_sub(bindings[line[3]])
		policy_obj.set_obj(bindings[line[4]])
		policy_obj.set_app(line[5])
		print policy_obj.name
		bindings[line[1]]=policy_obj
		policies.append(policy_obj)
		
	
start("test")
print bindings
print policies
print bindings["www"]