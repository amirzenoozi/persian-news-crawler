import sqlite3
import sys

from tqdm import tqdm
from flair.data import Sentence
from flair.models import SequenceTagger


db_file_path = './volume/fars_news.db'
ner_count = {
    'PER': 0,
    'LOC': 0,
    'ORG': 0,
    'DAT': 0,
    'TIM': 0,
    'PCT': 0,
    'MON': 0,
    'MISC': 0,
    'ERROR': 0,
}

def main():
    db_connection = sqlite3.connect(db_file_path)
    db_cursor = db_connection.cursor()
    query = "SELECT body FROM news ORDER BY published_datetime ASC;"
    db_cursor.execute(query)
    result = db_cursor.fetchall()
    db_connection.commit()
    db_connection.close()

    # load tagger
    tagger = SequenceTagger.load("PooryaPiroozfar/Flair-Persian-NER")

    for record in tqdm(result):
        for item in record[0].split('.'):
            if item != '':
                try:
                    # make example sentence
                    sentence = Sentence(item)

                    # predict NER tags
                    tagger.predict(sentence)

                    # iterate over entities and print
                    for entity in sentence.get_spans('ner'):
                        ner_count[entity.tag] = ner_count.get(entity.tag) + 1
                        # print(entity.text)
                        # print(entity.tag)
                        # print(ner_count[entity.tag])
                except KeyboardInterrupt:
                    print(ner_count)
                    sys.exit(0)
                except:
                    ner_count['ERROR'] = ner_count.get('ERROR') + 1
                    print(ner_count)
    
    print(ner_count)

if __name__ == '__main__':
    main()