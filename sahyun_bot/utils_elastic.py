import webbrowser
from typing import Callable

from elasticsearch import Elasticsearch
from elasticsearch_dsl.connections import get_connection

from sahyun_bot.elastic import CustomDLC
from sahyun_bot.utils import debug_ex
from sahyun_bot.utils_logging import get_logger

LOG = get_logger(__name__)

DOCUMENTS = frozenset([
    CustomDLC,
])


def setup_elastic() -> bool:
    """
    Initializes all indexes if they do not yet exist. See set of documents to initialize above.
    Also verifies if the mappings in the index match.
    """
    return _with_elastic('setup', _setup)


def purge_elastic() -> bool:
    """
    Deletes all indexes that are associated with this application. Intended for use with tests or while developing.
    This will delete all data if used!
    """
    return _with_elastic('purge', _purge)


def links(query: str):
    """
    Searches for matching CDLCs in the index and opens any found links in the browser.
    """
    results = CustomDLC.request(query)
    if results:
        for hit in results:
            webbrowser.open(hit.link, new=2)
    else:
        LOG.warning('No CDLCs matching <%s> were found.')


def _with_elastic(do: str, action: Callable[[Elasticsearch], None]) -> bool:
    try:
        action(get_connection())
        return True
    except Exception as e:
        LOG.warning('Could not %s elastic. Perhaps client is down?', do)
        return debug_ex(e, f'{do} elastic', LOG, silent=True)


def _setup(es):
    for doc in DOCUMENTS:
        index = doc.index_name()
        if es.indices.exists(index):
            mapping_on_server = es.indices.get_mapping(index)[index]['mappings']
            if mapping_on_server != doc.mapping():
                LOG.critical('Mapping mismatch for %s! Using this index may produce unpredictable results!', index)
        else:
            LOG.warning('Initializing index: %s.', index)
            doc.init()


def _purge(es):
    for doc in DOCUMENTS:
        LOG.critical('Deleting index & its contents (if it exists): %s', doc.index_name())
        doc._index.delete(ignore=[404])