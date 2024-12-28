#!/usr/bin/env pybricks-micropython

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

def on_message(topic, msg):
    '''
    Função chamada quando uma mensagem é recebida
    
    :param topic: O tópico ao qual a mensagem foi enviada.
    :param msg: O payload da mensagem recebida.
    '''
    position = int(msg.decode()) # Recebe a mensagem e converte para inteiro
    print("Recebido comando para mover o motor para posição: {}".format(position))
    ev3.screen.clear()
    ev3.screen.draw_text(0, 50, "Posição: {}".format(position)) # Exibe a posição na tela do Brick
    motor.run_target(500, position) # Define a velocidade e a posição-alvo de um Servomotor Lego
    send_motor_position()

client = MQTTClient(CLIENT_ID, BROKER, port=PORT) # Cria um cliente MQTT com o ID do brick, endereço e porta do Broker
client.set_callback(on_message)  # Define a função de callback para mensagens recebidas
client.connect()
print("Conectado ao broker MQTT.")
client.subscribe(TOPIC_RECEIVE)

def send_motor_position():
    '''
    Função para enviar a posição atual do motor
    '''
    position = motor.angle() # Recebe o ângulo atual do motor
    client.publish(TOPIC_SEND, str(position))
    print("Enviado posição atual do motor: {}".format(position))
    ev3.screen.clear()
    ev3.screen.draw_text(0, 0, "Motor: {}".format(position))

send_motor_position() # Envia a posição atual do motor na inicialização

try:
    while True:
        client.check_msg()  # Verifica se há novas mensagens
except KeyboardInterrupt:
    print("Desconectando...")
    client.disconnect()
