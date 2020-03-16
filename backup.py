#!/opt/bin/python3

from hb import backup_media_file, backup_media, backup_plex_db, get_media_backup_logs, get_plex_db_backup_logs, get_media_backup_stats, get_plex_db_backup_stats, selftest_media_backup, selftest_plex_db_backup
from destination_helpers import turn_on_destinations, turn_off_destinations
import argparse
from pushover import Client

# Set up and get arguments
parser = argparse.ArgumentParser(description='Coordinate file backups.')
parser.add_argument('file', nargs='?', help='Backup only the specified file')
parser.add_argument('--upload', '-u', help='Upload to destinations', action='store_true')
parser.add_argument('--selftest', '-t', help='Run the selftest after completing the backup', action='store_true')
parser.add_argument('--logs', '-l', help='Get the logs after completing the backup', action='store_true')

args = parser.parse_args()

if args.upload:
    turn_on_destinations()
else:
    turn_off_destinations()

if args.file is None:
    backup_media()
    backup_plex_db()
else:
    backup_media_file(args.file)

if args.selftest:
    selftest_media_backup()
    selftest_plex_db_backup()

if args.logs:
    client = Client('u8rfcaghrikib2i4qtkkazoqc4m9dd', api_token='agixw6imtgs59zigj2mmzfspajstun')

    media_stats = get_media_backup_stats()
    media_logs = get_media_backup_logs()
    plex_db_stats = get_plex_db_backup_stats()
    plex_db_logs = get_plex_db_backup_logs()

    media_alert = media_logs + "\n--------------------------------\n\n" + media_stats
    plex_db_alert = plex_db_logs + "\n--------------------------------\n\n" + plex_db_stats
    
    client.send_message(media_alert, title="Plex media")
    client.send_message(plex_db_alert, title="Plex database")
