from sahyun_bot.utils import read_config, NON_EXISTENT, nuke_from_orbit, parse_bool, parse_list

DEFAULT_HOST = 'localhost'
DEFAULT_CUSTOMSFORGE_INDEX = 'cdlcs'

DEFAULT_REQUEST_FIELDS = (
    'artist^4',
    'title^4',
    'album^2',
    'author',
)
DEFAULT_REQUEST_MATCH_CEILING = 3

TEST_CUSTOMSFORGE_INDEX = DEFAULT_CUSTOMSFORGE_INDEX + '_test'
TEST_ONLY_VALUES = frozenset([
    TEST_CUSTOMSFORGE_INDEX,
])

e_host = NON_EXISTENT
e_cf_index = NON_EXISTENT
e_req_fields = NON_EXISTENT
e_req_max = NON_EXISTENT
e_explain = NON_EXISTENT


def ready_or_die():
    """
    Immediately shuts down the application if the module is not properly configured.
    Make the call immediately after imports in every module that depends on this configuration to be loaded.
    """
    if NON_EXISTENT in [e_host, e_cf_index, e_req_fields, e_req_max, e_explain]:
        nuke_from_orbit('programming error - elastic module imported before elastic_settings is ready!')


def init():
    global e_host
    global e_cf_index
    global e_req_fields
    global e_req_max
    global e_explain

    e_host = read_config('elastic', 'Host', fallback=DEFAULT_HOST)
    e_cf_index = read_config('elastic', 'CustomsforgeIndex', fallback=DEFAULT_CUSTOMSFORGE_INDEX)
    # noinspection PyTypeChecker
    e_req_fields = read_config('elastic', 'RequestFields', convert=parse_list, fallback=DEFAULT_REQUEST_FIELDS)
    e_req_max = read_config('elastic', 'RequestMatchCeiling', convert=int, fallback=DEFAULT_REQUEST_MATCH_CEILING)
    e_explain = read_config('elastic', 'Explain', convert=parse_bool, fallback=False)

    e_req_max = e_req_max if Verify.timeout(e_req_max) else DEFAULT_REQUEST_MATCH_CEILING

    for config in [e_host, e_cf_index, e_req_fields, e_req_max, e_explain]:
        if config in TEST_ONLY_VALUES:
            nuke_from_orbit('configuration error - cannot use TEST values for REAL initialization')


def init_test():
    global e_host
    global e_cf_index
    global e_req_fields
    global e_req_max
    global e_explain

    e_host = DEFAULT_HOST
    e_cf_index = TEST_CUSTOMSFORGE_INDEX
    e_req_fields = DEFAULT_REQUEST_FIELDS
    e_req_max = DEFAULT_REQUEST_MATCH_CEILING
    e_explain = True


class Verify:
    @staticmethod
    def timeout(timeout: int) -> bool:
        return timeout > 0
