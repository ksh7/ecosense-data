import environ
import requests
from requests_aws4auth import AWS4Auth
import json

env = environ.Env()
environ.Env.read_env()

rearc_headers = {
    'Content-Type': 'application/json',
    'x-amzn-dataexchange-asset-id': env('REARC-DATAEXCHANGE-ASSET-ID'),
    'x-amzn-dataexchange-data-set-id': env('REARC-DATAEXCHANGE-DATA-SET-ID'),
    'x-amzn-dataexchange-revision-id': env('REARC-DATAEXCHANGE-REVISION-ID')
}

predicthq_headers = {
    'Content-Type': 'application/json',
    'x-amzn-dataexchange-asset-id': env('PREDICTHQ-DATAEXCHANGE-ASSET-ID'),
    'x-amzn-dataexchange-data-set-id': env('PREDICTHQ-DATAEXCHANGE-DATA-SET-ID'),
    'x-amzn-dataexchange-revision-id': env('PREDICTHQ-DATAEXCHANGE-REVISION-ID')
}

rearc_aws_auth = AWS4Auth(env('AWSID'), env('AWSKEY'), 'us-east-1', 'dataexchange')
predicthq_aws_auth = AWS4Auth(env('AWSID'), env('AWSKEY'), 'us-west-2', 'dataexchange')

def get_aws_dataset(sources, provider_type):
    _data = {}

    for source in sources:
        if provider_type = 'REARC':
            r = requests.request('GET', 'https://api-fulfill.dataexchange.us-east-1.amazonaws.com/v1/series/' + source.aws_api_url + '?limit=100&offset=0', auth=rearc_aws_auth, headers=rearc_headers)
            if r.status_code == 200:
                _data[source.aws_api_url] = {
                    'name': source.name,
                    'description': source.description,
                    'dataset': r.json()["dataset"],
                    'series': r.json()["series"],
                    'provider': r.json()["provider"]
                }
        if provider_type = 'PREDICTHQ':
            r = requests.request('GET', 'https://api-fulfill.dataexchange.us-east-1.amazonaws.com/v1/series/' + source.aws_api_url + '?limit=100&offset=0', auth=predicthq_aws_auth, headers=predicthq_headers)
            if r.status_code == 200:
                _data[source.aws_api_url] = {
                    'name': source.name,
                    'description': source.description,
                    'dataset': r.json()["results"]
                }
    
    return _data