#!/bin/bash
set -euo pipefail

KIBANA_URL=http://kibana:5601

# wait until Kibana is up and running
while [[ "$(curl -sS -o /dev/null -w '%{http_code}' kibana:5601/api/status)" != "200" ]]; do
    sleep 5
done
# launch metricbeat
metricbeat -e -system.hostfs=/hostfs -strict.perms=false