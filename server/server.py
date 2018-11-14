from flask import Flask, render_template, jsonify, request, g
from random import choice
from flask_cors import CORS
import json
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
import stringdist
import scipy
import numpy

app = Flask(__name__,
            static_folder="../dist/static",
            template_folder="../dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

glove_input_file = './assets/glove_twitter_200d.txt'
word2vec_output_file = './assets/tmp_word2vec.txt'
glove2word2vec(glove_input_file, word2vec_output_file)

stanford_model = KeyedVectors.load_word2vec_format(word2vec_output_file)
google_model = KeyedVectors.load_word2vec_format('./assets/google_pretrained_model.bin', binary=True)


@app.route('/api/name', methods=['POST', 'GET'])
def get_stupid_name():
    plus_one = request.get_json()["plusOne"].strip().lower()
    plus_two = request.get_json()["plusTwo"].strip().lower()
    minus_one = request.get_json()["minusOne"].strip().lower()
    rum_or_whiskey = request.get_json()["rumOrWhiskey"].strip().lower()
    cocktail_object = check_existing_combos(rum_or_whiskey, plus_one, plus_two)
    if cocktail_object == "":
        new_name = True
        adjective_out = get_most_similar_word([plus_one, plus_two], [minus_one], 'adjectives')
        noun_out = get_most_similar_word([plus_two, plus_one], [minus_one], 'nouns')
        cocktail_object = {"adjective": adjective_out, "noun": noun_out}
    if new_name == True:
        print("new word")
    return jsonify(cocktail_object)

@app.route('/api/random')
def random_name():
    with open('./assets/classified_terms.json', 'r') as f:
        names = json.load(f)
        random_adjective = choice(names.get('adjectives'))
        random_noun = choice(names.get('nouns'))
        return jsonify({"noun": random_noun, "adjective": random_adjective})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

def closest_string(base_word, word_list):
    lowest_distance = 100
    closest_word = ''
    for word in word_list:
        distance = stringdist.levenshtein(base_word,word)
        if distance <= lowest_distance:
            closest_word = word
            lowest_distance = distance
    return closest_word

def get_common_w_similarity(base_word, word_list):
    closest_meaning = 0
    closest_word = ''
    if base_word in stanford_model.vocab:
        for word in word_list:
            if word in stanford_model.vocab:
                distance = stanford_model.similarity(base_word, word)
                if distance >= closest_meaning and distance < 1:
                    closest_word = word
                    closest_meaning = distance
    else:
        closest_word = choice(word_list)
    return closest_word

def word_combinator(words_plus, words_minus):
    output_word = stanford_model.most_similar(words_plus, words_minus, n=1)
    print(output_word)
    return output_word

def check_existing_combos(rum_or_whiskey, mixer, garnish):
    existing_combo = ""
    with open('./assets/saved_names.json', 'r') as f:
        combos = json.load(f)
        if rum_or_whiskey in combos:
            if mixer in combos[rum_or_whiskey]:
                if garnish in combos[rum_or_whiskey][mixer]:
                    existing_combo = combos[rum_or_whiskey][mixer][garnish]
    return existing_combo

def update_combos(rum_or_whiskey, mixer, garnish, cocktail_object):
    with open('./assets/saved_names.json', 'r') as f:
        combos = json.load(f)
        if mixer not in combos[rum_or_whiskey]:
            combos[rum_or_whiskey] = mixer
        if garnish not in combos[rum_or_whiskey][mixer]:
            combos[rum_or_whiskey][mixer] = garnish
        combos[rum_or_whiskey][mixer][garnish] = cocktail_object
    with open("replayScript.json", "w") as f:
        json.dump(combos, f)

def vector_length(vector):
    return numpy.sqrt((numpy.sum(vector ** 2)))

def normalize_vector(vector):
    # TODO: check for divide by zero errors
    return vector / vector_length(vector)

def average_word_vectors(vectors):
    return normalize_vector(sum(vectors))

def get_most_similar_word(positive_words, negative_words, noun_or_adjective ='nouns'):
    # This is prone to fail if any of the seed_words aren't already in the model
    average_positive_vector = average_word_vectors(list(map(stanford_model.get_vector, positive_words)))
    if negative_words:
        average_negative_vector = average_word_vectors(list(map(stanford_model.get_vector, negative_words)))
        average_vector = average_positive_vector - average_negative_vector
    else:
        average_vector = average_positive_vector
    with open('./assets/classified_terms.json', 'r') as myFile:
        names = json.load(myFile)
        funny_word_list = names.get(noun_or_adjective)

        max_similarity = 0
        most_similar_word = ''
        for funny_word in funny_word_list:
            # It's boring to end up with the same word we started with...
            if funny_word.strip().lower() in positive_words:
                continue

            try:
                funny_word_vector = stanford_model.get_vector(funny_word.strip().lower())
                similarity = 1 - scipy.spatial.distance.cosine(average_vector, funny_word_vector)
                if similarity > max_similarity:
                    most_similar_word = funny_word
                    max_similarity = similarity
            except KeyError:
                print(funny_word)
                # Note, some of our adjectives aren't already in the model...
                pass

    return most_similar_word