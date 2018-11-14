import gensim
import json
import scipy

# GoogleNews-vectors-negative300.bin comes from https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit
print('Loading...')
model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
print('Loaded.')


def average_word_vectors(vectors):
	if len(vectors) == 0:
		print('ERROR: Did not pass in any vectors')
		return None

	return sum(vectors) / len(vectors)


def get_most_common_word(seed_words):
	# This is prone to fail if any of the seed_words aren't already in the model
	average_vector = average_word_vectors(map(model.get_vector, seed_words))

	with open('classified_terms.json', 'r') as myFile:
		names = json.load(myFile)
		adjectives = names.get('adjectives')

		max_similarity = 0
		most_similar_word = ''
		for word in adjectives:
			# It's boring to end up with the same word we started with...
			if word in seed_words:
				continue

			try:
				adjective_vector = model.get_vector(word)
				similarity = 1 - scipy.spatial.distance.cosine(average_vector, adjective_vector)
				if similarity > max_similarity:
					most_similar_word = word
					max_similarity = similarity
			except KeyError:
				# Note, some of our adjectives aren't already in the model...
				pass

	return most_similar_word


print('Most common word: ', get_most_common_word(['banana', 'sleep']))