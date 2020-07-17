gradient jobs create --name SSHD-JOB --command 'bash ./data/run_sshd.sh'  --apiKey a89b1d82aa901f10194447412e9b83 --projectId prr6d2y9i --machineType 'C3' --container isischameleon/mltraining-sshd:latest --ports 8888:22 --workspace "https://github.com/IsisChameleon/ml-training.git"


#(ml-training) isischameleon@~/Dropbox/Coding/gitrepos/ml-training/data (master)$ ▶ gradient jobs stop --id j9dqsgf8kph5f
#Gradient reponse content: b'',             status_code:204, data: None
#Job j9dqsgf8kph5f stopped