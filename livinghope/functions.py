from difflib import get_close_matches
import urllib2, string, re, pickle
import hashlib
from livinghope.models import Verse, Book, Chapter
def force_int(entry):
    """
    accepts string entry with numbers and/or characters. If entry only contains
    numbers, will convert it to int then return value.
    If entry contains characters, will force remove characters then convert remains to int
    """
    try:
        result = int(entry)
    except:
        temp = re.sub(r'\D', '', entry)
        result = int(temp)
    return result

def parse_string_to_verses(query):
    """
    receives as input, a string query in the form (book chapter:verses)
    or (book chapter:verse-verse).
    returns a list of verse ids
    """
    query = query.strip().lower()
    #makes sure query is not empty string (no scripture reference)
    if query == '':
        return []
    # break up the string into groupings
    query_groups = query.split(',')
    results = []
    previous_book = None
    for query_group in query_groups:
        previous_book, verse_list = parse_string_group_to_verses(
                                        query_group.strip(), previous_book)
        results += verse_list
    return set(results)


def parse_string_group_to_verses(query, previous_book=None):
    """
    receives as input, a string query in the form (book chapter:verses)
    or (book chapter:verse-verse).
    returns a list of verse ids
    """
    book_list = ['genesis', 'exodus', 'leviticus', 'numbers', 'deuteronomy', 
        'joshua', 'judges', 'ruth', '1 samuel', '2 samuel', '1 kings', '2 kings', 
        '1 chronicles', '2 chronicles', 'ezra', 'nehemiah', 'esther', 'job', 
        'psalm', 'proverbs', 'ecclesiastes', 'song of solomon', 'isaiah', 
        'jeremiah', 'lamentations', 'ezekiel', 'daniel', 'hosea', 'joel', 'amos', 
        'obadiah', 'jonah', 'micah', 'nahum', 'habakkuk', 'zephaniah', 'haggai', 
        'zechariah', 'malachi', 'matthew', 'mark', 'luke', 'john', 'acts', 'romans', 
        '1 corinthians', '2 corinthians', 'galatians', 'ephesians', 'philippians', 
        'colossians', '1 thessalonians', '2 thessalonians', '1 timothy', '2 timothy',
        'titus', 'philemon', 'hebrews', 'james', '1 peter', '2 peter', '1 john', 
        '2 john', '3 john', 'jude', 'revelation']
        

    query_parts = query.split(' ')
    # query_parts will help to distinguish between 2 john and 2:2 for example
    #check if book name has ordinal, find location of first number
    if query[0] in '123' and len(query_parts) > 1:
        match = re.search("\d", query[2:])
        loc_ord = 2
    else:
        match = re.search("\d", query)
        loc_ord = 0
        
    #if there is no number(just book)
    #get_close matches takes input query, a list of possible options, number of
    #results to return and a difference factor and returns a list of close matches.
    #.42 needed for rev. match
    if not match:
        book = get_close_matches(query, book_list, 1, 0.6)[0]
        chapver = []
    else:
        num_loc = match.start() + loc_ord
        try:
            book = get_close_matches(query[0:num_loc].strip(), book_list, 1, 0.6)[0]
        except:
            book = None
        chapver = query[num_loc:].split(':')

    # if there is no book in query, (2:2-5) then use previous book
    if not book:
        if not previous_book:
            # could not parse book and no book passed in
            return None, []
        book = previous_book

    #if there is nothing after the book name, get the whole book
    if not chapver:
        qs = Verse.objects.filter(book__name__iexact=book)
        verse_list = qs.values_list('id', flat=True)
        return book, list(verse_list)
    else:
        chapter = chapver[0].strip()
    verse_list = []
    #this checks whether  there is verse designation. if not, get queryset of whole chapter
    if len(chapver) == 1:
        #check if this has '-'. if so, get multiple chapters
        if '-' in chapter:
            chapter_list = chapter.split('-')
            start_chapter = int(chapter_list[0])
            end_chapter = int(chapter_list[1])
            middle_chapters = range(start_chapter+1, end_chapter)
        
            begin_chap_verses = Verse.objects.filter(
                book__name__iexact=book, chapter__number=start_chapter,)
                
            end_chap_verses = Verse.objects.filter(
                book__name__iexact=book, chapter__number=end_chapter)
                
            mid_chap_verses = Verse.objects.none()
            for mid_chap in middle_chapters:
                verse_qs = Verse.objects.filter(
                    book__name__iexact=book, chapter__number=mid_chap)
                mid_chap_verses = mid_chap_verses | verse_qs
                
            all_verses_qs = begin_chap_verses | mid_chap_verses | end_chap_verses
            verse_list = all_verses_qs.values_list('id', flat=True)

        else:
            chapter = int(chapter)
            qs = Verse.objects.filter(book__name__iexact=book, chapter__number=chapter)
            verse_list = qs.values_list('id', flat=True)
    #this checks if string spans multiple chapters
    elif len(chapver) == 3:
        #example isaiah 52:13-53:12
        #[52, 13-53, 12]
        start_chapter = int(chapter)
        mid = chapver[1].split('-')
        #deals with a/b designation in verses for example verse 14b, just translate to 14
        #enough to just take off last char?
        #see force_int method
        start_verse = force_int(mid[0])
        end_chapter = int(mid[1])
        end_verse = force_int(chapver[2])

        middle_chapters = range(start_chapter+1, end_chapter)
        
        begin_chap_verses = Verse.objects.filter(
            book__name__iexact=book, chapter__number=start_chapter,
            number__gte=start_verse)
            
        end_chap_verses = Verse.objects.filter(
            book__name__iexact=book, chapter__number=end_chapter,
            number__lte=end_verse)
            
        mid_chap_verses = Verse.objects.none()
        for mid_chap in middle_chapters:
            verse_qs = Verse.objects.filter(
                book__name__iexact=book, chapter__number=mid_chap)
            mid_chap_verses = mid_chap_verses | verse_qs
            
        all_verses_qs = begin_chap_verses | mid_chap_verses | end_chap_verses
        #to get value of specific field in all elements within queryset use
        #qs.value() for dict, or qs.values_list('fieldname', flat=True) for list
        verse_list = all_verses_qs.values_list('id', flat=True)
    else: #if verse designation, then parse the verse string
        verses = chapver[1]
        chapter = int(chapter)
        #if there's a dash in verses, get beginning and end number then get all verses in between
        if '-' in verses:
            startend = verses.split('-')
            start = force_int(startend[0])
            end = force_int(startend[1])
            qs = Verse.objects.filter(book__name__iexact=book,chapter__number=chapter,
                number__gte=start).filter(number__lte=end)
            verse_list = qs.values_list('id', flat=True)
        else:
            verses = force_int(verses)
            verse_object = Verse.objects.get(book__name__iexact=book, chapter__number=chapter, number=verses)
            verse_list.append(verse_object.id)
    verse_list = list(verse_list)
    return book, verse_list
    # return book
    
def test_parsable(query):
    """
    function that receives as in put a query and returns true if parsable and false if not
    """
    try:
        verse_list = parse_string_to_verses(query)
        if len(verse_list) > 0:
            parsable = True
        else:
            parsable = False
    except:
        parsable = False
    return parsable
    