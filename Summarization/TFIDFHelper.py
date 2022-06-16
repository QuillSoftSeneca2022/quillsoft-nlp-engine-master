import sys
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


class TFIDFHelper:

    # Calculates tf-idf and performs a cosine similarity on all the provided sentences to each other, returns filtered sentences based on threshold
    @classmethod
    def tfidf(cls, corpus, arr, threshold):
        """
        :param corpus: string - The "corpus" this will usually be the whole text of an article
        :param arr: array of string - The "document", containing the text we are calculating similarity for. This will usually be sentences from a paragraph.
        :param threshold: float - The limit of similarity sentences being compared can be, before being filtered out
        :returns: array of strings
        """
        tfidf_vectorizer = TfidfVectorizer(stop_words="english")

        # Fit using paper or document as the corpus
        tfidf_data = tfidf_vectorizer.fit(corpus)

        # Transform the document
        X = tfidf_vectorizer.transform(arr)

        similarity_arr = []
        for x in range(len(arr) - 1):
            similarity = cosine_similarity(X[x : x + 1], X)
            l = similarity
            similarity_arr.append(l)

        # Filter out likely sentences in the array, this will create a dictionary using the sentence 
        # # as key and similar sentences (array/list) as value
        filter_dict = {}
        for outer_count, ndarr in enumerate(similarity_arr):
            temp_arr = list(ndarr.flatten())
            filter_arr = []
            for count, value in enumerate(temp_arr):
                if not (count == 0 or value >= 1) and value >= threshold:
                    filter_arr.append(count)
            filter_dict[outer_count] = filter_arr

        # Using the dictionary created from above, iterate and add the sentence number to be filtered, this will
        # avoid scenarios such as if sentence 2 is removed and sentence 3 is being removed because of sentence 2, keep sentence 3
        final_filter_arr = []
        for sent_num in filter_dict:
            if sent_num not in final_filter_arr:
                # Concat the values into a single array
                final_filter_arr = final_filter_arr + filter_dict[sent_num]

        # Append sentences not in filtered sentences array to new array
        filtered_sentences = []
        for count, sent in enumerate(arr):
            if not count in final_filter_arr:
                filtered_sentences.append(sent)

        return filtered_sentences
