# Simulação de Filas M/M/1 - MS

## Alunos
- Gustavo Candido
- Gustavo Nunes

## Descrição

Este projeto tem como objetivo simular um sistema onde clientes podem chegar e ser atendidos por um único servidor. Por exemplo, o sistema pode ser um lava-jato onde os carros chegam no sistema, esperam por um tempo na fila até serem atendidos pelo atendente.

A simulação é útil para que possamos coletar dados como por exemplo:

- número médio de clientes na fila durante o tempo da simulação
- tempo médio de um cliente no sistema
- tempo médio de um cliente na fila
- tempo médio no qual o servidor demora para atender o cliente

Os tempos com os quais os clientes chegam no sistema e o tempo que o servidor leva para atender um cliente são definidos de forma aleatória através do arquivo de config (ver detalhes nos itens abaixo).

## Dependências
- `python3` instalado na máquina
- `pip3` instalado na máquina
- pacote **tabulate**
  - `pip3 install tabulate`
- pacote **bisect**
  - `pip3 install bisect`

## Setup arquivo de config

Para executar a simulação, é necessário adicionar os parâmetros desejados no arquivo `config.json`. Os parâmetros possíveis são:

<table>
<tr>
  <th>Nome</th>
  <th style="width: 55%">Descrição</th>
  <th style="width: 55%">Valores Possíveis</th>
</tr>

<tr>

<td><code>tec_type</code></td>
<td>Tipo de aleatoriedade usada para gerar o tempo entre as chegadas</td>
<td>
  <code>uniform</code>, <code>deterministic</code>, <code>exp</code>, <code>mmc</code>
</td>
</tr>

<td><code>tec</code></td>
<td>Parâmetro necessário para gerar o tempo entre as chegadas dependendo do <code>tec_type</code> desejado</td>
<td>
  (Ver explicação abaixo)
</td>
</tr>

<td><code>ts_type</code></td>
<td>Tipo de aleatoriedade usada para gerar o tempo de serviço</td>
<td>
  <code>uniform</code>, <code>deterministic</code>, <code>exp</code>, <code>mmc</code>
</td>
</tr>

<td><code>ts</code></td>
<td>Parâmetro necessário para gerar o tempo de serviço dependendo do <code>ts_type</code> desejado</td>
<td>
  (Ver explicação abaixo)
</td>
</tr>

<td><code>clients</code></td>
<td>Número de clientes na simulação</td>
<td>
  <code>int</code> > 0
</td>
</tr>

<td><code>max_queue_size</code> (opcional, default = inf)</td>
<td>Tamanho máximo da fila</td>
<td>
  <code>int</code> >= 0
</td>
</tr>
</table><br>

### Parâmetros de aleatoriedade e seus atributos

Os parâmetros que adicionam aleatoriedade à simulação são os parâmetros TEC (tempo entre chegadas) e TS (tempo de serviço). É possível controlar o tipo da variável aleatória desejada pelos atributos `tec_type` e `ts_type`, que podem receber um dos possíveis valores abaixo:

<table>
<tr>
  <th>Tipo</th>
  <th style="width: 55%">Descrição</th>
</tr>

<tr>

<td><code>uniform</code></td>
<td>Distribuição uniforme em um intervalo</td>
</tr>

<td><code>deterministic</code></td>
<td>Valores determinísticos</td>
</tr>

<td><code>exp</code></td>
<td>Distribuição exponencial</td>
</tr>

<td><code>mmc</code></td>
<td>Método de Monte Carlo</td>
</tr>

</table><br>



Os campos `tec` e `ts` armazenam os parâmetros necessários dependendo do tipo (dentre os mencionados acima). Cada tipo exige um formato especial para os parâmetros conforme os exemplos abaixo:

<table>
<tr>
  <th>Tipo</th>
  <th style="width: 55%">Descrição do atributo</th>
  <th>Exemplo</th>
</tr>

<tr>

<td><code>uniform</code></td>
<td style="width: 55%">Intervalo de valores possíveis</td>
<td><code>
<pre>
"ts_type": "uniform",
"ts": {
  "min_value": 1.5, 
  "max_value": 5
}
</pre></code>
</td></tr>

<td><code>deterministic</code></td>
<td style="width: 55%">Array com os possíveis valores</td>
<td><code>
<pre>
"ts_type": "deterministic",
"ts": [3, 2, 5]
</pre></code>
</td></tr>

<td><code>exp</code></td>
<td style="width: 55%">Taxa de chegada (em unidades de tempo). Por exemplo: lambda = 0.5 significa que os clientes chegam em média a cada meia hora (se a unidade de tempo for em horas), portanto chegam 1/0.5 = 2 clientes por hora. </td>
<td><code>
<pre>
"ts_type": "exp",
"ts": {
  "lambda": 0.5 
}
</pre></code>
</td></tr>

<td><code>mmc</code></td>
<td style="width: 55%">Array de objetos. Cada objeto vai ter um campo "class" indicando a sua classe com o intervalo representado, e a sua frequência desejada em relação aos outros objetos (ou seja, a sua probabilidade). No exemplo ao lado, o primeiro objeto irá aparecer 3x mais que o segundo.

As frequências também podem assumir valores de probabilidade. por exemplo, ao invés de frequências 3 e 1, poderiam assumir suas probabilidades direto: 0.75 e 0.25 respectivamente.

</td>
<td><code>
<pre>
"tec_type": "mmc",
"tec": [
  {
    "class": {
      "min_value": 0, 
      "max_value": 5
    },
    "frequency": 3
  },
  {
    "class": {
      "min_value": 5, 
      "max_value": 10
    },
    "frequency": 1
  }
]
</pre></code>
</td></tr>

</table>

## Execução

### Ambiente Linux

- No terminal, executar: `python3 main.py`