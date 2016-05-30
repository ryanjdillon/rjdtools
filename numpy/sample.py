'''
You can alternatively use a math trick and iteratively go through myList from
left to right, picking numbers with dynamically-changing probability
(N-numbersPicked)/(total-numbersVisited). The advantage of this approach is
that it's an O(N) algorithm since it doesn't involve sorting!

http://stackoverflow.com/a/6482925/943773
'''

def orderedSampleWithoutReplacement(seq, k):
    if not 0<=k<=len(seq):
        raise ValueError('Required that 0 <= sample_size <= population_size')

    numbersPicked = 0
    for i,number in enumerate(seq):
        prob = (k-numbersPicked)/(len(seq)-i)
        if random.random() < prob:
            yield number
            numbersPicked += 1
