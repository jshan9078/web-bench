#!/bin/bash
# Fleet control for the final-set matrix. Usage:
#   fleet.sh bundle                 tar the repo (no raw/, no media) and upload to s3://$BUCKET/bundle/
#   fleet.sh prereqs                IAM role + instance profile (S3 access to the bucket), key pair, security group (SSH from your IP)
#   fleet.sh seed                   launch ONE Ubuntu seed instance with the seed bootstrap; prints its IP for the operator's sign-ins
#   fleet.sh ami <instance-id>      stop the signed-in seed and create the AMI; prints the AMI id
#   fleet.sh launch <ami-id> <N> [lane] [family] [type]   launch N workers for one lane and config family (family: spark13|sonnet|opus|gemini-3.8-flash|luna|all); self-terminate when their queue slice is empty
#   fleet.sh launch-all <ami-id> <N-per-family> [lane]     one launch per family, N workers each (spreads provider rate limits)
#   fleet.sh status                 queue status + active leases + instances
#   fleet.sh terminate              terminate every instance tagged webbench=worker
# Env: BUCKET (default webbench-matrix-966239516827), REGION (us-east-1), KEY_NAME (webbench), SSH_CIDR (default your IP/32)
set -u; cd "$(dirname "$0")/.."; BUCKET=${BUCKET:-webbench-matrix-966239516827}; REGION=${REGION:-us-east-1}; KEY_NAME=${KEY_NAME:-webbench}
export AWS_DEFAULT_REGION=$REGION; export MATRIX_STORE=s3://$BUCKET/final63
case "${1:-status}" in
bundle)
  tar --exclude=./raw --exclude=./results/attempt1 --exclude=./results/voided --exclude=./results/matrix_store --exclude='*.mp4' --exclude='*.jpg' --exclude='*.png' --exclude=__pycache__ --exclude=./.git --exclude=./scratch --exclude=./archive --exclude='*.cpu.jsonl' -czf /tmp/web-bench.tar.gz .
  aws s3 cp /tmp/web-bench.tar.gz s3://$BUCKET/bundle/web-bench.tar.gz && ls -la /tmp/web-bench.tar.gz ;;
prereqs)
  aws iam get-role --role-name webbench-worker >/dev/null 2>&1 || {
    aws iam create-role --role-name webbench-worker --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"ec2.amazonaws.com"},"Action":"sts:AssumeRole"}]}' >/dev/null
    aws iam put-role-policy --role-name webbench-worker --policy-name s3-matrix --policy-document "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Action\":[\"s3:GetObject\",\"s3:PutObject\",\"s3:DeleteObject\",\"s3:ListBucket\"],\"Resource\":[\"arn:aws:s3:::$BUCKET\",\"arn:aws:s3:::$BUCKET/*\"]}]}"
    aws iam create-instance-profile --instance-profile-name webbench-worker >/dev/null; aws iam add-role-to-instance-profile --instance-profile-name webbench-worker --role-name webbench-worker; sleep 10; }
  aws ec2 describe-key-pairs --key-names $KEY_NAME >/dev/null 2>&1 || { aws ec2 create-key-pair --key-name $KEY_NAME --query KeyMaterial --output text > ~/.ssh/$KEY_NAME.pem; chmod 600 ~/.ssh/$KEY_NAME.pem; echo "key saved to ~/.ssh/$KEY_NAME.pem"; }
  VPC=$(aws ec2 describe-vpcs --filters Name=isDefault,Values=true --query 'Vpcs[0].VpcId' --output text)
  SG=$(aws ec2 describe-security-groups --filters Name=group-name,Values=webbench-worker --query 'SecurityGroups[0].GroupId' --output text 2>/dev/null)
  if [ "$SG" = None ] || [ -z "$SG" ]; then SG=$(aws ec2 create-security-group --group-name webbench-worker --description "web-bench matrix workers" --vpc-id $VPC --query GroupId --output text); aws ec2 authorize-security-group-ingress --group-id $SG --protocol tcp --port 22 --cidr ${SSH_CIDR:-$(curl -s https://checkip.amazonaws.com)/32} >/dev/null; fi
  echo "role webbench-worker, key $KEY_NAME, sg $SG" ;;
seed)
  AMI=$(aws ec2 describe-images --owners amazon --filters "Name=name,Values=ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*" --query 'sort_by(Images,&CreationDate)[-1].ImageId' --output text)
  SG=$(aws ec2 describe-security-groups --filters Name=group-name,Values=webbench-worker --query 'SecurityGroups[0].GroupId' --output text)
  sed "s/__BUCKET__/$BUCKET/g" aws/user_data_seed.sh > /tmp/ud_seed.sh
  ID=$(aws ec2 run-instances --image-id $AMI --instance-type c7i.xlarge --key-name $KEY_NAME --security-group-ids $SG --iam-instance-profile Name=webbench-worker --user-data file:///tmp/ud_seed.sh --block-device-mappings '[{"DeviceName":"/dev/sda1","Ebs":{"VolumeSize":40,"VolumeType":"gp3"}}]' --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=webbench-seed},{Key=webbench,Value=seed}]' --query 'Instances[0].InstanceId' --output text)
  aws ec2 wait instance-running --instance-ids $ID; IP=$(aws ec2 describe-instances --instance-ids $ID --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)
  echo "seed $ID at $IP  ->  ssh -i ~/.ssh/$KEY_NAME.pem ubuntu@$IP   (wait for ~/SEED_DONE, then sign in claude, codex, muse, agy)" ;;
ami)
  ID=$2; aws ec2 stop-instances --instance-ids $ID >/dev/null; aws ec2 wait instance-stopped --instance-ids $ID
  AMI=$(aws ec2 create-image --instance-id $ID --name "webbench-worker-$(date +%Y%m%d-%H%M)" --query ImageId --output text); aws ec2 wait image-available --image-ids $AMI; echo "AMI $AMI" ;;
launch)
  AMI=$2; N=$3; LANE=${4:-local}; FAM=${5:-all}; TYPE=${6:-c7i.xlarge}
  SG=$(aws ec2 describe-security-groups --filters Name=group-name,Values=webbench-worker --query 'SecurityGroups[0].GroupId' --output text)
  sed "s/__BUCKET__/$BUCKET/g; s/__LANE__/$LANE/g; s/__FAMILY__/$FAM/g; s/__SHUTDOWN__/shutdown -h now/" aws/user_data_worker.sh > /tmp/ud_worker.sh
  aws ec2 run-instances --image-id $AMI --count $N --instance-type $TYPE --key-name $KEY_NAME --security-group-ids $SG --iam-instance-profile Name=webbench-worker --user-data file:///tmp/ud_worker.sh --instance-initiated-shutdown-behavior terminate --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=webbench-worker-$LANE-$FAM},{Key=webbench,Value=worker}]" --query 'Instances[].InstanceId' --output text ;;
launch-all)
  AMI=$2; N=$3; LANE=${4:-local}; for FAM in spark13 sonnet opus gemini-3.8-flash luna; do echo "$FAM: $("$0" launch $AMI $N $LANE $FAM | tr '\n' ' ')"; done ;;
status)
  python3 matrix_queue.py status; echo; python3 matrix_queue.py workers; echo
  aws ec2 describe-instances --filters Name=tag:webbench,Values=worker,seed Name=instance-state-name,Values=pending,running,stopping --query 'Reservations[].Instances[].[InstanceId,Tags[?Key==`Name`].Value|[0],State.Name,PublicIpAddress]' --output table ;;
terminate)
  IDS=$(aws ec2 describe-instances --filters Name=tag:webbench,Values=worker Name=instance-state-name,Values=pending,running,stopped --query 'Reservations[].Instances[].InstanceId' --output text); if [ -n "$IDS" ]; then aws ec2 terminate-instances --instance-ids $IDS --query 'TerminatingInstances[].InstanceId' --output text; else echo "no workers"; fi ;;
esac
