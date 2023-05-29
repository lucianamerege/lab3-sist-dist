#servidor de echo: lado cliente
import rpyc

HOST = 'localhost' # maquina onde esta o servidor
PORT = 10020       # porta que o servidor esta escutando

def iniciaCliente():
	'''Conecta-se ao servidor.
	Saida: retorna a conexao criada.'''
	conn = rpyc.connect(HOST, PORT) 
	
	print(type(conn.root)) # mostra que conn.root eh um stub de cliente
	print(conn.root.get_service_name()) # exibe o nome da classe (servico) oferecido

	return conn

def fazRequisicoes(conn):
	# le as mensagens do usuario ate ele digitar 'fim'
	while True: 
		msg = input("\nO que deseja fazer?\nOpções:\n > Adicionar palavra/significado: Digite 'Add <palavra> <significado>'\n > Listar significados: Digite 'List <palavra>'\n > Deletar palavra: Digite 'Del <palavra>'\n > Fechar conexão: Digite 'Fim'\n\n")
		if msg == 'Fim': break 

		# envia a mensagem do usuario para o servidor
		ret = conn.root.exposed_atendeRequisicoes(msg)

		print(ret)

	# encerra a conexao
	conn.close()

def main():
	#inicia o cliente
	conn = iniciaCliente()
	#interage com o servidor ate encerrar
	fazRequisicoes(conn)

main()