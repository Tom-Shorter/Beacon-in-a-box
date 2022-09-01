"""
Filtering terms Endpoint.

Querying the filtering terms endpoint reveals information about existing ontology filters in this beacon.
These are stored in the DB inside the table named 'ontology_terms'.

"""

from beacon import conf
from beacon.db.filtering_terms import get_filtering_terms, get_resources
from beacon.db.schemas import DefaultSchemas
from beacon.request import RequestParams
from beacon.utils.stream import json_stream


async def handler(request, qparams: RequestParams, entity_schema: DefaultSchemas):
    docs = get_filtering_terms()
    ontology_terms = [
        {
            'id': record['ontology'] + ':' + record['term'],
            'label': record['label']
        }
        async for record in docs
    ]
    response = {
        'meta': conf.beacon_id,
        'apiVersion': conf.api_version,
        'resources': get_resources(),
        'filteringTerms': ontology_terms,
    }
    return await json_stream(request, response)
