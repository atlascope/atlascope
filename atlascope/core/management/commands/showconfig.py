from pprint import pprint

import django.conf
import djclick as click


def remove_hidden_keys(d: dict) -> dict:
    """
    Recursively remove hidden keys from a dict.

    For django settings, "hidden" keys would be ones that either (a) begin with
    an underscore or (b) are not all-uppercase.
    """
    # You can't remove keys from a dict during iteration, so instead we collect
    # the keys to be removed in a list and do them in a batch after the
    # iteration pass.
    remove = []
    for k in d:
        if k.startswith('_') or k.upper() != k:
            remove.append(k)
        elif type(d[k]) is dict:
            remove_hidden_keys(d[k])

    for k in remove:
        del d[k]

    return d


@click.command()
def command():
    settings = django.conf.settings
    config_dict = {}

    for key in dir(settings):
        config_dict[key] = getattr(settings, key)

    pprint(remove_hidden_keys(config_dict))
