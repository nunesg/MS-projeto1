# Primeiro Projeto de Programacao - MS

## Alunos
- Gustavo Candido
- Gustavo Nunes

## Dependencias
- pacote **tabulate**: `pip3 install tabulate`

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
- exp: lambda i.e. float in [0, 1)

`queue_max_size`: integer

`clients`: integer

## Executar

- `python3 main.py`

TODO:
- [ ] criar geradores (MMC, exponencial)
- [ ] criar config (arquivo JSON ou algo do tipo)
- [ ] arrumar Readme
- [ ] printar estatisticas (tempo medio de fila, etc)


