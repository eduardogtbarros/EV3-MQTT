#!/usr/bin/env pybricks-micropython

'''
File: main.py
Author: Eduardo Barros
Brief: Código para controlar um motor em um EV3Brick via MQTT.
'''

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from umqtt.simple import MQTTClient

# Configurações do MQTT
BROKER = "exemplo-mqtt.org"  # Substituir pelo endereço web ou IP do Broker
PORT = 1883  # Porta padrão para comunicação com o Broker
TOPIC_RECEIVE = b"Mqtt/Motor" # Tópico para receber os valores
TOPIC_SEND = b"Mqtt/Status" # Tópico para troca de informações
CLIENT_ID = b"Seu_Brick_EV3" # Substituir pelo nome do Brick

ev3 = EV3Brick() # Cria um objeto EV3Brick
motor = Motor(Port.A) # Cria um objeto Motor na porta A

def leMensagem(topic, msg):
    '''
    Função chamada quando uma mensagem é recebida.
    
    Args:
        topic (string): O tópico ao qual a mensagem foi enviada.
        msg (string): O payload da mensagem recebida.
    '''
    posicao = int(msg.decode()) # Recebe a mensagem e converte para inteiro
    print("Recebido comando para mover o motor para posição: {}".format(posicao))
    ev3.screen.clear()
    ev3.screen.draw_text(0, 50, "Posição: {}".format(posicao)) # Exibe a posição na tela do Brick
    motor.run_target(500, posicao) # Define a velocidade e a posição-alvo de um Servomotor Lego
    enviaPosicaoDoMotor()

client = MQTTClient(CLIENT_ID, BROKER, port=PORT) # Cria um cliente MQTT com o ID do brick, endereço e porta do Broker
client.set_callback(leMensagem)  # Define a função de callback para mensagens recebidas
try:
    client.connect()
    print("Conectado ao broker MQTT.")
except OSError as e:
    print("Erro ao conectar ao broker MQTT: {}".format(e))
client.subscribe(TOPIC_RECEIVE)

def enviaPosicaoDoMotor():
    '''
    Função para enviar a posição atual do motor.
    '''
    posicao = motor.angle() # Recebe o ângulo atual do motor
    client.publish(TOPIC_SEND, str(posicao))
    print("Enviado posição atual do motor: {}".format(posicao))
    ev3.screen.clear()
    ev3.screen.draw_text(0, 0, "Motor: {}".format(posicao))

enviaPosicaoDoMotor() # Envia a posição do motor na inicialização

while True:
    client.check_msg()  # Verifica se há novas mensagens