# archie and rm messages
cp db/messages.db db/archive/messages_$(date +%s).db
rm db/messages.db

# log whats been done into a log file and console
echo "Database reset at $(date)" >> logs/reset_database.log
echo "Database reset at $(date)"