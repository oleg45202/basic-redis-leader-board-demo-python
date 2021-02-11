import json

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from redis import Redis

from configuration.settings import REDIS_LEADERBOARD

if settings.REDIS_URL:
    redis_default = Redis.from_url(url=settings.REDIS_URL)
else:
    redis_default = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        db=settings.REDIS_DB
    )


def get_result(data):
    res = []
    for i in range(0, data.__len__()):
        symbol = data[i][0].decode('utf-8')
        company = redis_default.hgetall(symbol)
        res.append(
            {
                'company': get_str_from_bytes(company[b'company']),
                'country': get_str_from_bytes(company[b'country']),
                'marketCap': data[i][1],
                'rank': i+1,
                'symbol': symbol
            }
        )
    return res


def get_str_from_bytes(data):
    return data.decode('utf-8')


class GetTo10(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(json.dumps(get_result(redis_default.zrevrange(name=REDIS_LEADERBOARD, start=0, end=9,
                                                                          withscores=True, score_cast_func=int))),
                            status=200)


def index(request):
    context = {}
    return render(request, 'index.html', context)
