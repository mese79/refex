REF_TITLE = 'References\n'

CITATIONS = {
    'Style1': {
        'name': 'Style1',
        'patterns': [
            r'''(?P<authors>.+?)\.\s+(?P<title>.+?)\.\s+(?P<pub>.+?),\s+(?P<page>.+?),\s+(?P<year>19|20\d{2})\.''',
        ]
    },
    'MLA': {
        'name': 'Modern Language Association',
        'patterns': [
            r'''(?P<authors>.+?\.)\s+"(?P<title>.+?)\."\s+(?P<pub>.+?)\s+\((?P<year>19|20\d{2})\)\.''',
        ]
    },
    'Chicago': {
        'name': 'Chicago',
        'patterns': [
            r'''(?P<authors>.+?\.)\s+"(?P<title>.+?)\."\s+(?P<pub>.+?)\s+\((?P<year>19|20\d{2})\)\.''',
        ]
    },
    'APA': {
        'name': 'American Psychological Association',
        'patterns': [
            r'''(?P<authors>.+?\.)\s+\((?P<year>19|20\d{2})\)\.\s+(?P<title>.+?)\.\s+(?P<pub>.+?)\.''',
        ]
    },
    'Harvard': {
        'name': 'Harvard',
        'patterns': [
            r'''(?P<authors>.+?\.),\s+(?P<year>19|20\d{2})\.\s+(?P<title>.+?)\.\s+(?P<pub>.+?)\.''',
        ]
    },
    'Vancouver': {
        'name': 'Vancouver',
        'patterns': [
            r'''(?P<authors>.+?\.)\s+(?P<title>.+?)\.\s+(?P<pub>.+?)\.\s+(?P<year>19|20\d{2})''',
        ]
    },
    'IEEE': {
        'name': 'IEEE',
        'patterns': [
            r'''(?P<authors>.+?),\s+"(?P<title>.+?),"\s+(?P<pub>.+?)\.\s+(?P<year>19|20\d{2})''',
        ]
    }
}
