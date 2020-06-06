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
        irule(args.operation, args.collection, value=args.value, verbose=args.verbose)


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


if __name__ == '__main__':
    main()
