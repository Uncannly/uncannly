def array_to_string(word):
	return ' '.join(word)

def string_to_array(word):
	return word.split(' ')

def kebab_to_snake(string):
	return string.replace('-', '_')