#!/usr/bin/env python
from time import time
from maas_common import status_ok, status_err, metric, get_cinder_client


def main():
    try:
        cinder = get_cinder_client()
        if cinder is None:
            status_err('Unable to obtain valid cinder client, cannot proceed')

        start_time = time()
        volumes = cinder.volumes.list()
        request_time = int((time() - start_time) * 1000)
        available = [v for v in volumes if v.status == 'available']
        errored = [v for v in volumes if 'error' in v.status]

        snaps = cinder.volume_snapshots.list()
        snaps_available = [v for v in snaps if v.status == 'available']
        snaps_errored = [v for v in snaps if 'error' in v.status]
    except Exception as e:
        status_err(str(e))

    status_ok()
    metric('cinder_response_time', 'uint32', request_time)
    metric('cinder_volumes', 'uint32', len(volumes))
    metric('cinder_volumes_available', 'uint32', len(available))
    metric('cinder_volumes_errored', 'uint32', len(errored))
    metric('cinder_volume_snaps', 'uint32', len(snaps))
    metric('cinder_volume_snaps_available', 'uint32', len(snaps_available))
    metric('cinder_volume_snaps_errored', 'uint32', len(snaps_errored))

if __name__ == "__main__":
    main()