from enum import StrEnum

from elasticsearch import Elasticsearch


class AggOps(StrEnum):
    AVG = 'avg'
    MIN = 'min'
    MAX = 'max'


class SearchService:

    def __init__(self, es: Elasticsearch, index: str):
        self._index = index
        self._es = es

    def get_agg_by_gender(self, agg_op: AggOps):
        es_body = {
            'aggs': {
                'group_by_gender': {
                    'terms': {'field': 'gender'},
                    'aggs': {
                        f'{agg_op}_age': {str(agg_op): {'field': 'age'}},
                    }
                }
            }
        }
        ret = self._es.search(index=self._index, body=es_body)
        return [{'gender': bucket['key'], f'{agg_op}_age': bucket[f'{agg_op}_age']['value']} for bucket in
                ret.body['aggregations']['group_by_gender']['buckets']]
