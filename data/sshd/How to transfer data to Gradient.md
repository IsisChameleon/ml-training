https://medium.com/@jacobjonhansen/getting-your-data-onto-paperspace-gradient-176c97fb176e

Run sshd server on gradient :
''' paperspace jobs create \ 
      --apiKey a89b1d82aa901f10194447412e9b83 \
      --projectId prr6d2y9i \
      --machineType C3 \ 
      --container Test-Container \ 
      --ports 8888:22 \ 
      --command 'bash ./data/run_sshd.sh' \ 
      --workspace "https://github.com/IsisChameleon/ml-training.git" '''