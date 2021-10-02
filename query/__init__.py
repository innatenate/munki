queries = {
    'recentQuery': None,
    'pastQueries': [],
    'maxQueryLength': 10
}

def make(name, keywords, function, data=False):
    global queries

    query = {
        'name': name,
        'keywords': keywords,
        'func': function,
        'data': data
    }

    if queries['recentQuery']:
        queries['pastQueries'].append(queries['recentQuery'])
        if len(queries['pastQueries']) >= queries['maxQueryLength']:
            queries['pastQueries'].pop(len(queries['pastQueries'])-1)
    queries['recentQuery'] = query


def check(name):
    for query in queries['pastQueries']:
        if queries['pastQueries'][query]['name'] == name:
            return True, queries['pastQueries'][query]
        elif queries['recentQuery']['name'] == name:
            return True, queries['recentQuery']


def remove(name):
    for query in queries['pastQueries']:
        if queries['pastQueries'][query]['name'] == name:
            return True, queries['pastQueries'][query]
        elif queries['recentQuery']['name'] == name:
            return True, queries['recentQuery']
