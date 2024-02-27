## TESTES PARA MQTT
Utilizando o simulador de dispositivos IoT desenvolvido na atividade passada e utilizando os conceitos de TDD vistos no decorrer da semana, implemente testes automatizados para validar o simulador. Seus testes obrigatoriamente devem abordar os seguintes aspectos:

- Recebimento - garante que os dados enviados pelo simulador são recebidos pelo broker.
- Validação dos dados - garante que os dados enviados pelo simulador chegam sem alterações.
- Confirmação da taxa de disparo - garante que o simulador atende às especificações de taxa de disparo de mensagens dentro de uma margem de erro razoável.

- ## Como rodar:
- Clone o repositório
- pip install paho-mqtt pytest
- python3 publisher.py
- pytest subscriber.py

![Screenshot 2024-02-27 102542](https://github.com/riqueschilder/Ponderada-1-2-3/assets/99187952/24d52027-9a43-423f-bd25-02fd11b2ffb3)

  
https://github.com/riqueschilder/Ponderada-1-2/assets/99187952/be36b793-acba-4a25-80be-0bfa418473fe

