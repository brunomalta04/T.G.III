class Usuario:
    def __init__(self, id, nome):  
        self.id = id
        self.nome = nome
        self.filhos = []
        self.interacoes = {}

    def adicionar_interacao(self, id_filho, mensagem):
        self.interacoes[id_filho] = mensagem


class ArvoreRedeSocial:
    def __init__(self):  
        self.usuarios = {}

    def inserir_usuario(self, id, nome, id_pai=None):
        novo_usuario = Usuario(id, nome)
        self.usuarios[id] = novo_usuario
        if id_pai:
            pai = self.usuarios.get(id_pai)
            if pai:
                pai.filhos.append(novo_usuario)

    def remover_usuario(self, id):
        usuario = self.usuarios.pop(id, None)
        if usuario:
            for pai in self.usuarios.values():
                if usuario in pai.filhos:
                    pai.filhos.remove(usuario)
            for filho in usuario.filhos:
                self.usuarios.pop(filho.id, None)

    def buscar_usuario(self, id):
        return self.usuarios.get(id)

    def exibir_arvore(self):
        def exibir(no, nivel=0):
            print(" " * (nivel * 2) + no.nome)
            for filho in no.filhos:
                exibir(filho, nivel + 1)

        raizes = [u for u in self.usuarios.values() if all(u not in pai.filhos for pai in self.usuarios.values())]
        for raiz in raizes:
            exibir(raiz)

    def encontrar_comunidades(self):
        comunidades = []
        visitados = set()

        def dfs(no, comunidade):
            comunidade.append(no.nome)
            visitados.add(no.id)
            for filho in no.filhos:
                if filho.id not in visitados:
                    dfs(filho, comunidade)

        for usuario in self.usuarios.values():
            if usuario.id not in visitados:
                comunidade = []
                dfs(usuario, comunidade)
                if comunidade:
                    comunidades.append(comunidade)
        return comunidades

    def centralidade_grau(self):
        return {usuario.id: len(usuario.filhos) for usuario in self.usuarios.values()}

    def analisar_sentimentos(self):
        sentimentos = {}
        for usuario in self.usuarios.values():
            for id_filho, mensagem in usuario.interacoes.items():
                polaridade = self.analisar_polaridade(mensagem)
                subjetividade = self.analisar_subjetividade(mensagem)
                sentimentos[(usuario.id, id_filho)] = (polaridade, subjetividade)
        return sentimentos

    def analisar_polaridade(self, mensagem):
        positivas = ['bom', 'ótimo', 'excelente', 'otimo']
        negativas = ['ruim', 'terrível', 'péssimo', 'pessimo', 'terrivel']
        polaridade = 0
        palavras = mensagem.lower().split()
        for palavra in palavras:
            if palavra in positivas:
                polaridade += 1
            elif palavra in negativas:
                polaridade -= 1
        return polaridade

    def analisar_subjetividade(self, mensagem):
        palavras_subjetivas = ['eu', 'meu', 'acho', 'sentir']
        subjetividade = 0
        palavras = mensagem.lower().split()
        for palavra in palavras:
            if palavra in palavras_subjetivas:
                subjetividade += 1
        return subjetividade / len(palavras) if palavras else 0

    def exibir_sentimentos(self):
        sentimentos = self.analisar_sentimentos()
        for (id_usuario, id_filho), (polaridade, subjetividade) in sentimentos.items():
            print(f"Interação de {self.usuarios[id_usuario].nome} para {self.usuarios[id_filho].nome}:")
            print(f"  Polaridade: {polaridade:.2f}, Subjetividade: {subjetividade:.2f}")


# Criando a rede social e inserindo usuários
rede_social = ArvoreRedeSocial()
rede_social.inserir_usuario(1, "Alice")
rede_social.inserir_usuario(2, "Bob", 1)
rede_social.inserir_usuario(3, "Carol", 1)
rede_social.inserir_usuario(4, "David", 2)
rede_social.inserir_usuario(5, "Gabriel", 3)

# Adicionando interações entre os usuários
rede_social.usuarios[1].adicionar_interacao(2, "Você é um ótimo amigo!")
rede_social.usuarios[2].adicionar_interacao(3, "Vamos sair para jantar.")

# Exibindo a árvore da rede social
print("\nÁrvore da Rede Social:")
rede_social.exibir_arvore()

# Exibindo comunidades
print("\nComunidades:", rede_social.encontrar_comunidades())

# Exibindo centralidade de grau
print("\nCentralidade de Grau:", rede_social.centralidade_grau())

# Exibindo sentimentos das interações
print("\nSentimentos das Interações:")
rede_social.exibir_sentimentos()
