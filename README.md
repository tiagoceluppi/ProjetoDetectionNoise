Detector de Defeitos com Filtro Casado
Um projeto simples para detectar defeitos em sinais de áudio usando a técnica de filtro casado.

O que este projeto faz?
Imagine que você tem uma "assinatura sonora" de um defeito (como o barulho que uma máquina faz quando algo está errado) e quer encontrar quando esse mesmo defeito aparece em uma gravação longa de operação. Este programa faz exatamente isso!

Como funciona?
Carrega dois arquivos de áudio:

assinatura_defeito.wav - O "molde" do defeito que queremos encontrar
operacao_completa.wav - A gravação completa onde vamos procurar o defeito

Usa matemática para encontrar similaridades:

Aplica uma técnica chamada "correlação cruzada"
É como comparar o molde do defeito com cada pedacinho da gravação completa
Encontra onde a similaridade é máxima

Mostra os resultados:

Gráficos dos sinais originais
Gráfico da correlação (onde o pico indica quando o defeito foi detectado)
Tempo exato em que o defeito foi encontrado

O que você vai ver
O programa gera três gráficos:

Sinal de entrada: A gravação completa da operação
Molde do defeito: A assinatura sonora que estamos procurando
Resultado da detecção: Onde o pico mostra quando o defeito foi encontrado

Como usar

Coloque os arquivos de áudio na pasta do projeto:

assinatura_defeito.wav
operacao_completa.wav


Execute o programa:

bash   python signal_detector.py

Veja os gráficos e o resultado no console!

Requisitos
bashpip install numpy matplotlib scipy
Contexto técnico
Este projeto implementa um filtro casado, uma técnica clássica de processamento digital de sinais que:

Maximiza a relação sinal-ruído (SNR)
É ótima para detectar sinais conhecidos em meio ao ruído
É amplamente usada em radar, sonar e detecção de padrões

Estrutura do projeto
projeto/
├── matched_filter_detection.py    # Código principal
├── assinatura_defeito.wav         # Molde do defeito
├── operacao_completa.wav          # Gravação a ser analisada
└── README.md                      # Este arquivo

Sobre os arquivos de áudio
Os arquivos WAV podem ser gravações reais de:

Máquinas industriais
Equipamentos em operação
Qualquer fonte sonora onde você queira detectar padrões específicos

