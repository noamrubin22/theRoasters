def calculate_score(word, count):

    score = 0;

    for i in range(len(word)):
        if word[i] == 'a':
            score+=1

    return score



words = ['The', 'amount', 'and', 'complexity', 'of', 'information', 'produced', 'in', 'science,', 'engineering,', 'business,', 'and', 'everyday', 'human', 'activity', 'is', 'increasing', 'at', 'staggering',
'rates.', 'The', 'goal', 'of', 'this', 'course', 'is', 'to', 'expose', 'you', 'to', 'visual', 'representation', 'methods', 'and', 'techniques', 'that', 'increase', 'the', 'understanding',
 'of', 'complex', 'data.', 'Good', 'visualizations', 'not', 'only', 'present', 'a',
 'visual', 'interpretation', 'of', 'data,', 'but', 'do', 'so', 'by', 'improving',
 'comprehension,', 'communication,', 'and', 'decision', 'making.']

words = sorted(words, key=calculate_score, reverse=True)
