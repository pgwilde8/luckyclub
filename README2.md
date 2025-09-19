
Username:	support@luckyclubwins.com
Password:	Securepass1
POP/IMAP Server:	heracles.mxrouting.net
SMTP Server:	heracles.mxrouting.net

LUCKYCLUB /luckyclubwins.com

http://24.144.67.150:9177/

su - luckyadmin
cd /opt/webwise/luckyclub
source .venv/bin/activate

git add .
git commit -m "pgw3"
git push

uvicorn app.main:app --host 0.0.0.0 --port 9177 --reload

sudo cp luckyclub.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable luckyclub.service
sudo systemctl start luckyclub.service
sudo systemctl stop luckyclub.service
sudo systemctl restart luckyclub.service
sudo systemctl status luckyclub.service
sudo journalctl -u luckyclub.service -f
sudo systemctl start luckyclub.service
---------------------------------------------------
psql -U luckyclub -d luckyclub -h localhost

              List of relations
 Schema |      Name       | Type  |   Owner   
--------+-----------------+-------+-----------
 public | alembic_version | table | luckyclub
 public | entry_ledger    | table | luckyclub
 public | proof_uploads   | table | luckyclub
 public | raffles         | table | luckyclub
 public | users           | table | luckyclub
(5 rows)

sudo -u postgres psql -d luckyclub -c "
SELECT id, user_id, kind, file_path, status, created_at
FROM proof_uploads 
ORDER BY created_at DESC 
LIMIT 10;
"

sudo -u postgres psql -d luckyclub -c "
SELECT id, user_id, kind, file_path, status, created_at, reviewed_at
FROM proof_uploads 
WHERE file_path LIKE '%96a58fbc-ef96-42a7-a100-7bf90db41fb7.webp%'
ORDER BY created_at DESC;
"
-------------------------------------------------


3. Entry System
Why this? Core functionality - users need to earn entries
What to build: Entry earning mechanisms (voting, sharing, uploading proofs)
Files to work on: Entry forms, entry tracking
🎯 Phase 2: Raffle Management
4. Admin Panel
Why? You need to manage raffles, review proofs, draw winners
What to build: Admin dashboard, raffle creation, proof review
Files to work on: app/templates/admin/ directory
5. Proof Upload System
Why? Users need to upload screenshots for entry verification
What to build: File upload forms, proof review interface