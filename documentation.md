# Documentação

Além das informações neste arquivo, recomenda-se a leitura do arquivo `readme.md`

## config.json

Esse arquivo tem a função de especificar os atributos para a execução da simulação, como o tipo das variáveis aleatórias, número de clientes na simulação e tamanho máximo da fila.

Mais informações podem ser encontradas no arquivo `readme.md`

## main.py

Ponto de entrada do programa. Inicia a simulação e instancia os geradores das variáveis aleatórias.

## generators.py

Definição dos geradores de números aleatórios utilizáveis na simulação. São eles:

- Gerador de inteiros aleatórios no intervalo distribuídos de maneira uniforme (`Uniform`)
- Gerador de números aleatórios dentre um conjunto pré-especificado de valores possíveis (`Deterministic`)
- Gerador de números aleatórios seguindo distribuição exponencial (`Exponential`)
- Gerador de números aleatórios seguindo o método de Monte Carlo, atribuindo classes de valores possíveis e suas respectivas `frequências` ou `probabilidades`

## server.py

Classe para encapsular o servidor na simulação.

## simulation.py

Classe que controla a simulação, executando a chegada dos clientes e gerando as estatísticas que serão printadas ao final do processo.

