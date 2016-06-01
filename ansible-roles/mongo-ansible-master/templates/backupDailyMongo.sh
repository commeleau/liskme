#!/bin/sh
sudo -u {{mongodb_backup_user}} mkdir -p /home/{{mongodb_backup_user}}/mongoDB

# Purge pruge directory from backup older thant {{mongodb_backup_max_days}} 
find /home/{{mongodb_backup_user}}/mongoDB/[0-9]* -maxdepth 0  -type d  -ctime {{mongodb_backup_max_days}} | xargs rm -rf 

# What's the day today.
day=$(date +"%Y%m%d")

#Create folders if necessary
sudo -u {{mongodb_backup_user}} mkdir -p  /home/{{mongodb_backup_user}}/mongoDB/$day

sudo -u {{mongodb_backup_user}} mongodump   -o /home/{{mongodb_backup_user}}/mongoDB/$day
