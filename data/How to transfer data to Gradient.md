https://medium.com/@jacobjonhansen/getting-your-data-onto-paperspace-gradient-176c97fb176e

Run sshd server on gradient :
''' paperspace jobs create --machineType C3 --container Test-Container --ports 8888:22 --command 'bash ./data/run_sshd.sh' --workspace "https://github.com/IsisChameleon/ml-training" '''