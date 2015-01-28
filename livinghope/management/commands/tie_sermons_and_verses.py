from django.core.management.base import BaseCommand, CommandError
from livinghope.models import Sermon, Verse
from livinghope.functions import parse_string_to_verses

class Command(BaseCommand):
    help = 'Ties all sermons to verse objects corresponding to their \
            passage input. Also cleans up passage designations with abbreviations'
    def handle(self, *args, **options):
        all_sermons = Sermon.objects.all()
        for sermon in all_sermons:
            passage = sermon.passage
            sermon_id = sermon.id
            if 'Gen.' in passage:
                passage = passage.replace('Gen.', 'Genesis')
            if 'Thess.' in passage:
                passage = passage.replace('Thess.', 'Thessalonians')
            if 'Is.' in passage:
                passage = passage.replace('Is.', 'Isaiah')
            if 'Matt.' in passage:
                passage = passage.replace('Matt.', 'Matthew')
            if 'Gal.' in passage:
                passage = passage.replace('Gal.', 'Galatians')
            if 'Sam.' in passage:
                passage = passage.replace('Sam.', 'Samuel')
            if 'Col.' in passage:
                passage = passage.replace('Col.', 'Colossians')
            if 'Ps.' in passage:
                passage = passage.replace('Ps.', 'Psalm')
            if 'Tim.' in passage:
                passage = passage.replace('Tim.', 'Timothy')
            if 'Pet.' in passage:
                passage = passage.replace('Pet.', 'Peter')
            if 'Neh.' in passage:
                passage = passage.replace('Neh.', 'Nehemiah')
            if 'Rev.' in passage:
                passage = passage.replace('Rev.', 'Revelation')
            if 'Phil.' in passage:
                passage = passage.replace('Phil.', 'Philippians')
            if ';' in passage:
                passage = passage.replace(';', ',')
            sermon.passage = passage
            verse_list = parse_string_to_verses(passage)
            verses = Verse.objects.filter(id__in=verse_list)
            sermon.verses.add(*verses)
            sermon.save()
            # print passage
            print "%s tied with %d verses" % (passage, len(verse_list))
            # print "%s successfully tied with %s" % (sermon, passage)
