#This algoritm was copied at 16/Nov/2018 from https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python and applied to activity sequences
delimter = "@"

def length(s):
    return s.count(delimter) + 1

def enumerateSequence(s):
    list = s.split(delimter)
    return enumerate(list,0)

def levenshtein(s1, s2):
    if length(s1) < length(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if length(s2) == 0:
        return length(s1)

    previous_row = range(length(s2) + 1)
    for i, c1 in enumerateSequence(s1):
        current_row = [i + 1]
        for j, c2 in enumerateSequence(s2):
            insertions = previous_row[j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]