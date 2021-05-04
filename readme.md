# Primeiro Projeto de Programacao - MS

## Alunos
- Gustavo Candido
- Gustavo Nunes

## Dependencias
- pacote **tabulate**: `pip3 install tabulate`
- pacote **bisect**: `pip3 install bisect`

## Setup config

`tec_type/ts_type`: deterministic | uniform | mmc | exp

`tec/ts`:
- deterministic: array of possible values
- uniform: 
```
{
  min_value: number, 
  max_value: number
}
```
- mmc: 
```
[
  {
    "class": {
      min_value: number, 
      max_value: number
    },
    "frequency": float in [0, 1)
  }
]
```
- exp: lambda i.e. arrival rate

`max_queue_size`: integer

`clients`: integer

## Executar

- `python3 main.py`

TODO:
- [ ] arrumar Readme
- [ ] printar estatisticas (num medio de entidades na fila, clientes dropados)