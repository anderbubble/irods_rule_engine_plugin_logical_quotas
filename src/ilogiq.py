#!/usr/bin/env python


import argparse
import json
import subprocess


OPERATIONS_MAP = {
    'ls': 'ls',
    'count-objects': 'logical_quotas_count_total_number_of_data_objects',
    'count-size': 'logical_quotas_count_total_size_in_bytes',
    'recalculate': 'logical_quotas_recalculate_totals',
    'set-max-objects': 'logical_quotas_set_maximum_number_of_data_objects',
    'set-max-size': 'logical_quotas_set_maximum_size_in_bytes',
    'start-monitoring': 'logical_quotas_start_monitoring_collection',
    'stop-monitoring': 'logical_quotas_stop_monitoring_collection',
    'unset-max-objects': 'logical_quotas_unset_maximum_number_of_data_objects',
    'unset-max-size': 'logical_quotas_unset_maximum_size_in_bytes',
    'unset-total-objects': 'logical_quotas_unset_total_number_of_data_objects',
    'unset-total-size': 'logical_quotas_unset_total_size_in_bytes',
}


def main ():
    help_epilog = "Operations: {}".format(' '.join(OPERATIONS_MAP.keys()))
    parser = argparse.ArgumentParser(epilog=help_epilog)
    parser.add_argument('operation', type=lambda x: OPERATIONS_MAP[x])
    parser.add_argument('collection')
    parser.add_argument('value', nargs='?', default=None)
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()
    if args.operation == 'ls':
        imeta_lsw(args.collection)
    else:
        value = args.value
        if args.operation == 'logical_quotas_set_maximum_size_in_bytes':
            value = parse_bytes(value)
        irule(args.operation, args.collection, value=value, verbose=args.verbose)


def irule (operation, collection, value=None, verbose=False):
    cmd = ['irule']
    if verbose:
        cmd.append('--verbose')
    rule = {
        'operation': operation,
        'collection': collection,
    }
    if value is not None:
        rule['value'] = str(value)
    cmd.append(json.dumps(rule))
    cmd.extend(('null', 'null'))
    subprocess.call(cmd)


def imeta_lsw(collection):
    cmd = ['imeta', 'lsw', '-C', collection, 'irods::logical_quotas::%']
    subprocess.call(cmd)


def parse_bytes(bytes_str):
    bytes_str = bytes_str.lower()
    if bytes_str.endswith('pb'):
        return int(bytes_str[:-2]) * (1000 ** 5)
    elif bytes_str.endswith('tb'):
        return int(bytes_str[:-2]) * (1000 ** 4)
    elif bytes_str.endswith('gb'):
        return int(bytes_str[:-2]) * (1000 ** 3)
    elif bytes_str.endswith('mb'):
        return int(bytes_str[:-2]) * (1000 ** 2)
    elif bytes_str.endswith('kb'):
        return int(bytes_str[:-2]) * (1000 ** 1)
    elif bytes_str.endswith('pib'):
        return int(bytes_str[:-3]) * (1024 ** 5)
    elif bytes_str.endswith('tib'):
        return int(bytes_str[:-3]) * (1024 ** 4)
    elif bytes_str.endswith('gib'):
        return int(bytes_str[:-3]) * (1024 ** 3)
    elif bytes_str.endswith('mib'):
        return int(bytes_str[:-3]) * (1024 ** 2)
    elif bytes_str.endswith('kib'):
        return int(bytes_str[:-3]) * (1024 ** 1)
    else:
        return int(bytes_str)


if __name__ == '__main__':
    main()
