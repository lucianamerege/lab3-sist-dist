import rpyc
import select
import sys
import threading

#servidor que dispara um processo filho a cada conexao
from rpyc.utils.server import ThreadedServer

PORT = 10020 # porta de acesso


class Dictionary(rpyc.Service):
	dicionario = {}
	num_linhas = 0

	def iniciaDicionario(self, nada):
		with open('dicionario.txt', 'r') as arq:
			linhas = arq.readlines()
			for i, linha in enumerate(linhas):
				if linha != '\n':
					#strip tira os espaços no começo e fim da linha
					chave, *valores = [entrada.strip() for entrada in linha.split(',')]
					valores.insert(0, i)
					self.dicionario[chave] = valores
				self.num_linhas = self.num_linhas + 1

		print("Dicionario preparado:")
		print(self.dicionario)

	def on_connect(self, conn):
		self.iniciaDicionario(self)
		print("Cliente conectado.")

	def on_disconnect(self, conn):
		print("Cliente desconectou.")

	def exposed_atendeRequisicoes(self, msg):
		#recebe dados do cliente, volta a ser infinito pois está atendendo apenas a cada thread
		while True:
			
			if msg.startswith('Add'):
				resposta = self.checaAdicao(msg)
				return resposta
			elif msg.startswith('List'):
				resposta = self.retornaLista(msg.split())
				return resposta
			elif msg.startswith("Del"):
				resposta = self.deleta(msg.split())
				return resposta				
			else:
				return 'Comando inexistente.'

	def deleta(self, msg):
		if len(msg) != 2:
			return 'Sintaxe incorreta.'
		elif msg[1] not in self.dicionario:
			return 'Sintaxe incorreta.'
		else:
			values = self.dicionario[msg[1]]
			lines = open('dicionario.txt', 'r').readlines()
			lines[values[0]] = '\n'
			arq = open('dicionario.txt', 'w')
			arq.writelines(lines)
			arq.close()
			del self.dicionario[msg[1]]
			resposta = msg[1] + ' removido do dicionário'
			return resposta

	def retornaLista(self, chave):
		if len(chave) != 2:
			return 'Sintaxe incorreta.'
		else:	
			if chave[1] in self.dicionario:
				sorted = self.dicionario[chave[1]]
				num = sorted[0]
				del sorted[0]
				sorted.sort()
				self.dicionario[chave[1]].insert(0, num)
				return sorted
			else:
				return '[]'
			
	def checaAdicao(self, cmd):
		add = cmd.split()
		if len(add) != 3:
			return "Sintaxe incorreta."
		elif add[1] in self.dicionario:
			definicoes = self.dicionario[add[1]]
			definicoes.append(add[2])
			self.dicionario.update({add[1]:definicoes})

			with open('dicionario.txt', 'r+') as arq:
				linhas = arq.readlines()
				#o primeiro valor da lista é o número da linha onde está aquela palavra
				linhas[int(definicoes[0])] = linhas[int(definicoes[0])].strip() + ', ' + add[2] + '\n'
				arq.seek(0)
				for linha in linhas:
					arq.write(linha)

			resp = "Definição adicionada: " + add[2]
			return resp
		else:
			with open('dicionario.txt', 'a', encoding='utf-8') as arq:
				arq.write(add[1] + ', ' + add[2] + '\n')

			definicoes = [self.num_linhas]
			definicoes.append(add[2])
			self.dicionario.update({add[1]:definicoes})

			self.num_linhas = self.num_linhas + 1

			print(self.dicionario)

			resp = "Palavra adicionada ao dicionario: " + add[1]
			return resp


def main():
	print("Pronto para receber conexoes...")
	srv = ThreadedServer(Dict, port = PORT)
	srv.start()


main()
