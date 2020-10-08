cd "$(dirname $0)"
python3 dns_challenge_aliyun.py ${CERTBOT_VALIDATION}
# sleep to make sure the challenge is applied
sleep 25
