"""
 longest substring from t_w (target word) that is present in the keys of the mp_word dictionary.
"""


# LSSRA
def longest_substring_search(target_word, word_map):
    max_length = 0
    matched_word = target_word

    for i in range(len(target_word)):
        current_word = target_word[i:]

        for j in range(len(current_word), 1, -1):
            sub_word = current_word[:j]
            if sub_word in word_map:
                if j > max_length:
                    max_length = j
                    matched_word = sub_word

    return matched_word


"""Levenshtein distance (or edit distance) algorithm. 
This algorithm calculates the minimum number of single-character edits 
(insertions, deletions, or substitutions) needed to transform one string into another.
"""


def calculate_minimum_distance(str1, str2):
    len_str1 = len(str1)
    len_str2 = len(str2)

    # Initialize the dynamic programming matrix
    dp = [[0 for _ in range(len_str2 + 1)] for _ in range(len_str1 + 1)]

    # Fill the matrix based on the Levenshtein distance algorithm
    for i in range(len_str1 + 1):
        for j in range(len_str2 + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i][j - 1], dp[i - 1][j], dp[i - 1][j - 1])

    # The bottom-right cell of the matrix contains the minimum distance
    return dp[len_str1][len_str2]
