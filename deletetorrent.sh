#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

source ${DIR}/auth/conf_move.ini

echo [$(date)] " movetorrent.sh started"

# use transmission-remote to get torrent list from transmission-remote list
# use sed to delete first / last line of output, and remove leading spaces
# use cut to get first field from each line
TORRENTLIST=$(transmission-remote --auth $auth --list | sed -e '1d;$d;s/^ *//' | cut --only-delimited --delimiter=" " --fields=1)
# for each torrent in the list
for TORRENTID in $TORRENTLIST
do
  TORRENTID=$(echo "$TORRENTID" | sed 's:*::')
  echo [$(date)] " Torrent #$TORRENTID: Operations on torrent starting"
  # check if torrent download is completed
  DL_COMPLETED=$(transmission-remote --auth $auth --torrent $TORRENTID --info | grep "Percent Done: 100%")
  # check torrent.s current state is .Stopped., .Finished., or .Idle.
  STATE_STOPPED=$(transmission-remote --auth $auth --torrent $TORRENTID --info | grep "State: Stopped\|Finished\|Idle\|Seeding")
  # if the torrent is .Stopped., .Finished., or .Idle. after downloading 100%.
  if [ "$DL_COMPLETED" != "" ] && [ "$STATE_STOPPED" != "" ]; then
    #echo "Removing torrent from list."
    transmission-remote --auth $auth --torrent $TORRENTID --remove
    echo [$(date)] " Torrent #$TORRENTID: Completed. Removing."
  else
    echo [$(date)] " Torrent #$TORRENTID: not completed. Ignoring."
  fi
  #echo "* * * * * Operations on torrent ID $TORRENTID completed. * * * * *"
done
