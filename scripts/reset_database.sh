# archie and rm chat
cp db/chat.db db/archive/chat_$(date +%s).db
rm db/chat.db

# log whats been done into a log file and console
echo "Database reset at $(date)" >> logs/reset_database.log
echo "Database reset at $(date)"