class TrieNode(object):
		
	def __init__(self, val):
		self.val = val
		self.kids = {}
		self.val_has_call = hasattr(val, '__call__')
		self.terminal = False
	
	def __call__(self, x):
		if self.val is None:
			return None
		if self.val_has_caller:
			return self.val.__call__(x)
		if type(self.val) in (str, unicode):
			return self.val.__eq__(x)
		if type(self.val) is _pattern_type:
			return self.val.search(x)
		raise(Exception('Nodes must be strings, compiled regular expressions, or callables.'))
	
	def __in__(self, val):
		return val in self.kids
			
	def __getitem__(self, val):
		return self.kids.get(val, None)

class PhraseTrie(object):
	def __init__(self, phrases):
		"""
		phrases : a list of lists or tuples where each element is a token, like this:
				[('phrase', 'one'), ('phrase', 'two'), ('phrase', 'three')]
		"""
		self.n = 0
		self.root = TrieNode(None)
		for phrase in phrases:
			self.add_phrase(phrase)
		self.phrases = copy(phrases)
	
	def __len__(self):
		return self.n
		
	def add_phrase(self, phrase, data=None):
		
		cur = self.root
		for token in phrase:
			next = cur[token]
			if next is None:
				next = TrieNode(token)
				cur.kids[token] = next
			cur = next
			
		if next.terminal == False:
			#This phrase was not previously here. We inserted anyway in case the the
			#data changed.
			self.n += 1
		next.terminal = True
		if data is not None:
			next.data = data
		return next

	def exact_match(self, phrase):
		cur = self.root
		for token in phrase:
			next = cur[token]
			if next is None:
				return False
			cur = next
		if next.terminal is True:
			return next
		return False
	
	def __contains__(self, phrase):
		cur = self.root
		for token in phrase:
			next = cur[token]
			if next is None:
				return False
			cur = next
		return True

def preserve_phrases(tokens, phrase_trie, phrase_funct):
	if len(phrase_trie) == 0:
		return tokens
	i = 0
	new_tokens = []
	while i < len(tokens): #The last word can't be a phrase
		#Token i starts a phrase! Let's see how far we can take it.
		end_matches = []
		#Find all the matches and keep the biggest one
		j = i
		while j < len(tokens):
			guess = tokens[i:j+1] #= because we want token j
			if guess not in phrase_trie:
				break
			if phrase_trie.exact_match(guess):
				end_matches.append(j)
			j += 1
		if not end_matches:
			new_tokens.append(tokens[i])
			i += 1
			continue
		
		j = end_matches[-1]
		phrase = phrase_funct(tokens[i:j+1])
		new_tokens.append(phrase)
		i = j+1
	return new_tokens
