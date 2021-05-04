# Primeiro Projeto de Programacao - MS

## Alunos
- Gustavo Candido
- Gustavo Nunes

## Dependências
- pacote **tabulate**: `pip3 install tabulate`
- pacote **bisect**: `pip3 install bisect`

## Setup arquivo de config

Para cada executar a simulação, é necessário adicionar os parâmetros desejados no arquivo `config.json`.


Os parâmetros que adicionam aleatoriedade à simulação são os parâmetros TEC (tempo entre chegadas) e TS (tempo de serviço). É possível controlar o tipo da variável desejada pelos atributos `tec_type` e `ts_type`, que podem receber um dos possíveis valores abaixo:

<table>
<tr>
  <th>Tipo de TEC-TS</th>
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
  <th>Tipo de TEC-TS</th>
  <th style="width: 55%">Descrição do atributo</th>
  <th>Exemplo</th>
</tr>

<tr>

<td><code>uniform</code></td>
<td style="width: 55%">Intervalo de valores possíveis</td>
<td><code>
<pre>
"ts": {
  min_value: 1.5, 
  max_value: 5
}
</pre></code>
</td></tr>

<td><code>deterministic</code></td>
<td style="width: 55%">Array com os possíveis valores</td>
<td><code>
<pre>
"ts": [3, 2, 5]
</pre></code>
</td></tr>

<td><code>exp</code></td>
<td style="width: 55%">Taxa de chegada (em unidades de tempo). Por exemplo: lambda = 0.5 significa que os clientes chegam em média a cada meia hora (se a unidade de tempo for em horas), portanto chegam 1/0.5 = 2 clientes por hora. </td>
<td><code>
<pre>
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
"ts": [
  {
    "class": {
      min_value: 0, 
      max_value: 5
    },
    "frequency": 3
  },
  {
    "class": {
      min_value: 5, 
      max_value: 10
    },
    "frequency": 1
  }
]
</pre></code>
</td></tr>



</table>


`max_queue_size`: integer

`clients`: integer

## Executar

- `python3 main.py`