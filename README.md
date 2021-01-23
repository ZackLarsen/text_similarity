# text_similarity
Example application for comparing similarity of different texts

## Considerations:
1. Do you count punctuation or only words?
1. Which words should matter in the similarity comparison?
1. Do you care about the ordering of words?
1. What metric do you use to assign a numerical value to the similarity?
    * A useful metric here may be cosine similarity, as it unitizes the length of the text to allow for a more fair comparison between sentences, paragraphs, and entire documents.
1. What type of data structures should be used? (Hint: Dictionaries and lists are particularly helpful data structures that can be leveraged to calculate the similarity of two pieces of text.)
