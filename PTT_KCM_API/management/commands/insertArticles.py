from django.core.management.base import BaseCommand, CommandError
from project.settings_database import uri
from pymongo import MongoClient
from PTT_KCM_API.view.dictionary.postokenizer import  CutAndrmStopWords
import json, pyprind, pymongo

class Command(BaseCommand):
    help = 'use this for activating build_IpTable'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.client = MongoClient(uri)
        self.db = self.client['ptt']
        self.articlesCollect = self.db['articles']
        self.IndexCollect = self.db['invertedIndex']
        

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('json', type=str)
        parser.add_argument(
            '--append',
            default=False,
            help='An optional argument, if Append==True, then it wont empty mongoDB and append new articles in it. Otherwise, empty MongoDB before inserting articles.',
        )


    def handle(self, *args, **options):
        if options['append']==False:
            self.articlesCollect.remove({})
            self.IndexCollect.remove({})
            self.db['ip'].remove({})
            self.db['locations'].remove({})


        f = json.load(open(options['json'], 'r', encoding='utf-8-sig'))
        # cut sentence of all articles before inserting into MongoDB.
        self.cut_articles(f)

        self.invertedIndex()

        self.stdout.write(self.style.SUCCESS('insert Articles success!!!'))

    def cut_articles(self, file):
        for i in pyprind.prog_percent(file['articles']):
            i['content'] = contentSet = list(
                set(
                    CutAndrmStopWords('' if i.get('content', '')==None else i.get('content', ''))
                )
            )
            for j in i.get('messages', []):
                j['push_content'] = list(
                    set(
                        CutAndrmStopWords('' if j.get('push_content', '')==None else j.get('push_content', ''))
                    )
                )
        self.articlesCollect.insert(file['articles'])

    def invertedIndex(self):
        key = dict()
        for i in self.articlesCollect.find().batch_size(500):
            # pymongo Cursor with timeout if time of query data exceed 10 minutes.
            # so setting batch_size will fetch amount of document from mongo 
            # in per query.
            # But there is no universal "right" batch_size
            # You should test with different values and see what is the appropriate value for your use case i.e. how many documents can you process in a 10 minute window.
            # http://stackoverflow.com/questions/24199729/pymongo-errors-cursornotfound-cursor-id-not-valid-at-server
            objectID = i['_id']
            
            titleSet = set(CutAndrmStopWords('' if i.get('article_title', '')==None else i.get('article_title', '')))
            uniqueTerm = titleSet.union(set(i['content']))
            for k in uniqueTerm:
                key.setdefault(k, []).append(objectID)

        IndexList = tuple({'ObjectID':v, 'issue':k} for k, v in key.items())
        self.IndexCollect.insert(IndexList)
        self.IndexCollect.create_index([("issue", pymongo.HASHED)])