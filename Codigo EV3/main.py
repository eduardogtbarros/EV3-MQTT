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
TOPIC_SERVO = b"Mqtt/Servo" # Tópico para receber os valores do servo
TOPIC_ESQ = b"Mqtt/MotorEsq" # Tópico para receber os valores do motor esquerdo
TOPIC_DIR = b"Mqtt/MotorDir" # Tópico para receber os valores do motor direito
TOPIC_SEND = b"Mqtt/Status" # Tópico para troca de informações
CLIENT_ID = b"Seu_Brick_EV3" # Substituir pelo nome do Brick

ev3 = EV3Brick() # Cria um objeto EV3Brick
servo = Motor(Port.A) # Cria um objeto Motor na porta A
motorEsq = Motor(Port.B) # Cria um objeto Motor na porta B
motorDir = Motor(Port.C) # Cria um objeto Motor na porta C

def leMensagem(topic, msg):
    '''
    Função chamada quando uma mensagem é recebida.
    
    Args:
        topic (string): O tópico ao qual a mensagem foi enviada.
        msg (string): O payload da mensagem recebida.
    '''
    valor = int(msg.decode()) # Recebe a mensagem e converte para inteiro
    if topic == TOPIC_SERVO:
        print("Recebido comando para mover o servo para posição: {}".format(valor))
        ev3.screen.clear()
        ev3.screen.draw_text(0, 50, "Posição: {}".format(valor)) # Exibe a posição na tela do Brick
        servo.run_target(500, valor) # Define a velocidade e a posição-alvo de um Servomotor Lego
    else:
        print("Recebido comando para mover o motor para velocidade: {}".format(valor))
        ev3.screen.clear()
        ev3.screen.draw_text(0, 50, "Velocidade: {}".format(valor))
    if topic == TOPIC_ESQ:
        motorEsq.dc(valor) # Define a velocidade do motor esquerdo
        motor = motorEsq
    if topic == TOPIC_DIR:
        motorDir.dc(valor) # Define a velocidade do motor direito
        motor = motorDir
    
    enviaValorDoMotor(topic, motor)

client = MQTTClient(CLIENT_ID, BROKER, port=PORT) # Cria um cliente MQTT com o ID do brick, endereço e porta do Broker
client.set_callback(leMensagem)  # Define a função de callback para mensagens recebidas
try:
    client.connect()
    print("Conectado ao broker MQTT.")
except OSError as e:
    print("Erro ao conectar ao broker MQTT: {}".format(e))
client.subscribe(TOPIC_SERVO)
client.subscribe(TOPIC_ESQ)
client.subscribe(TOPIC_DIR)

def enviaValorDoMotor(topic, motor=None):
    '''
    Função para enviar a posição atual ou a velocidade do motor.
    '''
    if topic == "Mqtt/Servo":
        valor = servo.angle() # Recebe o ângulo atual do motor
        print("Enviado posição atual do servo: {}".format(valor))
        ev3.screen.clear()
        ev3.screen.draw_text(0, 0, "Servo: {}".format(valor))
    else:
        valor = motor.speed()
        print("Enviado velocidade atual do motor: {}".format(valor))
        ev3.screen.clear()
        ev3.screen.draw_text(0, 0, "Motor: {}".format(valor))
    client.publish(TOPIC_SEND, str(valor))

enviaValorDoMotor(TOPIC_SERVO) # Envia a posição do motor na inicialização
enviaValorDoMotor(TOPIC_ESQ,motorEsq) # Envia a velocidade do motor esquerdo na inicialização
enviaValorDoMotor(TOPIC_DIR,motorDir) # Envia a velocidade do motor direito na inicialização

while True:
    client.check_msg()  # Verifica se há novas mensagens