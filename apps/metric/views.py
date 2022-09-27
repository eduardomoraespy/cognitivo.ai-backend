from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from .models import Metric, LogMetric
from datetime import date, datetime
import time
from .serializers import LogMetricSerializer
import tweepy as tw


def search_csv():
    """

    """
    path_file = 'AppleStore.csv'
    df = pd.read_csv(path_file)

    # Application of the News category, which has the highest number of reviews.
    df_categ_news = df.loc[df['rating_count_tot'] == df['rating_count_tot'][df['prime_genre'] == "News"].max()]
    
    # Top 10 Applications of the Music and Book genre that have the most ratings.
    df_book_music = pd.concat([df[df['prime_genre'] == 'Book'], df[df['prime_genre'] == 'Music']])
    df_book_music_top_10 = df_book_music.sort_values('rating_count_tot', ascending=False)[:10]

    df_result = pd.concat([df_categ_news, df_book_music_top_10], ignore_index=True)

    return df_result

def generate_report():

    dates = search_csv()
    dates['n_citacoes'] = 0
    list_coluns = ['track_name', 'n_citacoes', 'size_bytes', 'price', 'prime_genre']
    date_now = datetime.now()
    date_now = date_now.strftime('%d-%m-%Y_%H-%M')
    date_today = date.today().strftime('%Y-%m-%d')

    bearer_token = 'AAAAAAAAAAAAAAAAAAAAAMDwhQEAAAAAqP3l5yhmWJKfWr6fMw4n1Qn083s%3DM4bGd3yDa5DaFaS3VvBp4ex2eMecLyA31bvnJAJZszCW0xiPVn'
    consumer_key = 'K11freHIjuSlNinqNaMFaCyXH'
    consumer_secret = 'YxdjBkXVqYFogAz8oq60gDMqFRPQrEdzPgTlUOdXOyF6yHZpMb'
    access_token = '1573762553070714884-lDR6P69AS3zQTiAxYRbwgwo2VIHrQS'
    access_token_secret = 'qNzA4X9rMs9oMVtwBDtrNTRlpbwuYWg3XN5m3SeAuTYjQ'

    start = f"{str(date_today)}T00:00:01Z"
    end = f"{str(date_today)}T23:59:01Z"

    cliente = tw.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)

    response_music = cliente.search_recent_tweets(query='music', max_results=100)
    response_book = cliente.search_recent_tweets(query='book', max_results=100)
    date_music= response_music.data
    date_book= response_book.data

    cont_music = 0
    cont_book = 0
    dict_citation = {}
    list_citation = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # response music and book
    for c in range(1, 11):
        if dates.loc[c, ['prime_genre']][0] == 'Music':
            for c_music in date_music:
                text_music = c_music.text

                if str(dates.loc[c, ['track_name']][0]).lower() in text_music.lower():
                    cont_music+=1
                    dict_citation[f'{c}'] = [str(dates.loc[c, ['track_name']][0]), int(dates.loc[c, ['id']][0]), cont_music]
                    list_citation[c-1] = cont_music
                    
                cont_music = 0

        if dates.loc[c, ['prime_genre']][0] == 'Book':
            for c_book in date_book:
                text_book = c_book.text

                if str(dates.loc[c, ['track_name']][0]).lower() in text_book.lower():
                    cont_book+=1
                    dict_citation[f'{c}'] = [str(dates.loc[c, ['track_name']][0]), int(dates.loc[c, ['id']][0]), cont_book]
                    list_citation[c-1] = cont_book

                cont_book = 0
    
    try:
        # Save Table
        for c in range(1, 11):
            # last_id = Metric.objects.last().id
            insert_metric = Metric.objects.create(
                # id = last_id+1,
                track_name = str(dates.loc[c,['track_name']][0]),
                n_citacoes = int(list_citation[c-1]),
                size_bytes = int(dates.loc[c,['size_bytes']][0]),
                price = dates.loc[c,['price']][0],
                prime_genre = dates.loc[c,['prime_genre']][0]
            )

            LogMetric.objects.create(
                metric_id = Metric.objects.get(id = int(insert_metric.id))
            )
        # Create csv
        dates[1:][list_coluns].to_csv(f'files/report_csv/report_{str(date_now)}.csv')

        # Create Json
        dates[1:][list_coluns].to_json(f'files/report_json/report{str(date_now)}.json')

    except Exception as error:
        print(error)

@api_view(['GET'])
def metric_api(request):

    generate_report()

    reports = LogMetric.objects.all().order_by('id')
    serializer = LogMetricSerializer(reports, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

