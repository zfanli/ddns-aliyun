echo python3 $(dirname $0)/dns_challenge_aliyun.py ${CERTBOT_VALIDATION}
python3 dns_challenge_aliyun.py ${CERTBOT_VALIDATION}
# sleep to make sure the challenge is applied
sleep 25
