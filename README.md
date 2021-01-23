# text_similarity
Example application for comparing similarity of different texts

## Considerations:
1. Do you count punctuation or only words?
    * I will leave this as an optional keywork argument for the user. This also facilitates comparison to see how much the score may change under different conditions.
1. Which words should matter in the similarity comparison?
    * Words that don't occur frequently should be given priority. One way to do this would be term frequency - inverse document frequency, but since the sample texts are fairly short, I am choosing to allow stopword removal using an optional keyword argument, which removes stopwords in a sample list of such words.
1. Do you care about the ordering of words?
    * Yes, in general there should be at least some penalty to the score if the order is not the same. One way to do this is to blend two scores, both between 0 and 1, so that even if the overlap is perfect but the order is different, the score will not be a perfect one. The way I am implementing this is with ngrams to check the overlap not just of single words (tokens), but in sequences of words (token ngrams). If the same words overlap but not in the correct sequence or order, the ngram similarity score will be less than 1, penalizing the overall score.
1. What metric do you use to assign a numerical value to the similarity?
    * A useful metric here may be Jaccard similarity (a.k.a. intersection-over-union) which compares the overlap in texts.
1. What type of data structures should be used? (Hint: Dictionaries and lists are particularly helpful data structures that can be leveraged to calculate the similarity of two pieces of text.)
    * Lists, dictionaries, Counters, and zipped lists may be of use here.

## Instructions:
* This program can be run as a command line application. It is built with python 3.8, so if the user has python 3.X+ installed, they can run the program at the command line and supply the input texts and the necessary arguments, and the similarity score will be printed to the terminal:
```bash
python compare_texts.py
```
