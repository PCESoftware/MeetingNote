

def wer(reference, hypothesis):
    """
    Calculate the Word Error Rate (WER) between a reference sentence and a hypothesis sentence.

    Parameters:
    reference (str): The reference sentence.
    hypothesis (str): The hypothesis sentence.

    Returns:
    float: The Word Error Rate (WER).
    """
    ref_words = reference.split()
    hyp_words = hypothesis.split()
    d = [[0] * (len(hyp_words) + 1) for _ in range(len(ref_words) + 1)]

    for i in range(len(ref_words) + 1):
        d[i][0] = i
    for j in range(len(hyp_words) + 1):
        d[0][j] = j

    for i in range(1, len(ref_words) + 1):
        for j in range(1, len(hyp_words) + 1):
            if ref_words[i - 1] == hyp_words[j - 1]:
                cost = 0
            else:
                cost = 1
            d[i][j] = min(d[i - 1][j] + 1,
                          d[i][j - 1] + 1,
                          d[i - 1][j - 1] + cost)

    edit_distance = d[len(ref_words)][len(hyp_words)]
    wer_value = edit_distance / len(ref_words)
    return wer_value
