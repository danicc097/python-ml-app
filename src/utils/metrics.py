import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def cosine_similarity_n_space(m1, m2, batch_size=100):
    assert m1.shape[1] == m2.shape[1]
    ret = np.ndarray((m1.shape[0], m2.shape[0]))
    for row_i in range(int(m1.shape[0] / batch_size) + 1):
        start = row_i * batch_size
        end = min([(row_i + 1) * batch_size, m1.shape[0]])
        if end <= start:
            # ignoring edge cases
            break
        rows = m1[start:end]
        sim = cosine_similarity(rows, m2)  # rows is O(1) size
        ret[start:end] = sim
    return ret
