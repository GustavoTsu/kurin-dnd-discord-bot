# kurin-dnd-discord-bot
Um bot para discord com funcionalidades para sessoẽs de rpg
 
## Pré requisitos:
- python 3.9 ou superior
- Um editor de código qualquer
- um token de um bot que você tenha criado (caso não saiba como fazer siga o tutorial abaixo)

## Criar o bot
- Para criar o bot acesse [discord.com/developers](https://discord.com/developers)

https://github.com/user-attachments/assets/120eae49-5938-44ab-a3a9-a9f43235e6d1

## Pegar o TOKEN
https://github.com/user-attachments/assets/3478de89-3fcc-416e-820e-8000f6882f10

## Rodar o bot
- baixe o zip do projeto ou use `git clone https://github.com/GustavoTsu/kurin-d-d-discord-bot.git` 
- descompacte o projeto e abra a pasta no terminal, `cd Kurin-dnd-discord-bot` em sistemas linux
- use `pip install -r requirements.txt para instalar as dependências
- abra um editor de código e coloque o token do seu bot na ultima linha do código
![Image](https://github.com/user-attachments/assets/3a477592-c91f-40a8-9c38-825d562996bd)

E por fim finalmente rode o código via terminal ou pelo editor de código usado,
no caso do terminal abra a pasta do projeto e use o comando `python main.py` ou `python3 main.py`


## Comandos disponíveis

### Como rolar um dado

Para rolar um dado, basta enviar a mensagem no formato:
- `1d20` ou `3d12+4` para rolagens normais.
- `#3d8+2` caso queira que os dados sejam rolados individualmente.

### XP e Ficha
- `;xp [valor]` - Adiciona XP à sua ficha. Caso não informe um valor, o bot exibirá seu XP atual.
- `;foto_ficha` - Adiciona uma imagem à sua ficha. Após o comando, envie a imagem em resposta ao bot.
- `;ficha [@usuário]` - Exibe sua ficha ou a ficha da pessoa mencionada.

### Personalização e Interação
- `;oi` - Envia uma saudação personalizada.
- `;nick [apelido]` - Define um apelido para ser usado pelo bot ao se referir a você.
- `;xingar @usuário` - Envia um xingamento aleatório para o usuário mencionado.
- `;beijar @usuário` - Marque uma pessoa para beijar e veja o que acontece.
- `;falar [frase]` - O bot repetirá a frase fornecida.

### Atributos e Cálculos
- `;calc [expressão]` - Calculadora simples, ex: `;calc 5 * 6`.
- `;upd_atributos [atributo1] [atributo2]` - Adiciona pontos aos atributos da ficha. Exemplo:
  - `;upd_atributos destreza` adiciona +2 na base do atributo.
  - `;upd_atributos destreza inteligencia` adiciona +1 em cada um.

### Armas
- `;?arma [nome ou parte do nome]` - Pesquisa armas pelo nome ou parte do nome. Exemplo: `;?arma bes` retorna todas as armas que começam com "bes".
- `;adicionar_arma [nome da arma]` - Adiciona uma arma à sua ficha.
- `;armas [@usuário]` - Exibe as armas vinculadas à sua ficha ou à de outra pessoa mencionada.

### Criação de Fichas e Armas
- `/criar_ficha` - Abre um formulário para criar uma nova ficha de personagem.
- `/criar_arma` - Abre um formulário para criar uma nova arma de D&D.

---

Este bot foi desenvolvido para facilitar a jogabilidade de RPG no Discord, garantindo mais praticidade para os jogadores!

