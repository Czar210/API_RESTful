Este projeto foi desenvolvido como parte do seminário da disciplina Comunicação em Sistemas Distribuídos. Ele demonstra a aplicação de uma API RESTful, com integração à API oficial da Riot Games, e um sistema distribuído que consulta, salva e exibe dados de partidas de jogadores de League of Legends.
Objetivo
Demonstrar na prática a comunicação entre componentes distribuídos através de uma API RESTful, utilizando:
- API externa (Riot Games)
- Backend com Flask
- Banco de dados local (SQLite)
- Frontend em HTML/JS acessando o backend
Estrutura do Projeto
.
├── app.py                      # Servidor Flask principal
├── call_champions.py          # Comunicação com API da Riot
├── database.py                # Operações de banco SQLite
├── index_um_jogador_botoes_api20.html  # Frontend principal
├── requirements.txt           # Dependências do projeto
├── .env.example               # Exemplo de arquivo com variável de ambiente
└── README.md                  # Você está aqui
Atenção: O banco mydatabase.db e o arquivo .env com sua chave não devem ser enviados ao GitHub.
Como Executar o Projeto
1. Clone o repositório:
git clone https://github.com/Czar210/API_RESTful.git
cd API_RESTful
2. Instale as dependências:
pip install -r requirements.txt
3. Configure sua chave da Riot:
Coloque no arquivo .env sua chave da riot api:
RIOT_API_KEY=sua-chave-aqui
Você pode obter sua chave gratuita em: https://developer.riotgames.com/
