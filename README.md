# Projeto Doação de Sangue: API

API REST em **Python + Flask** feita no 1º semestre de Engenharia de Software (PUCPR) para gerenciar um sistema de doação de sangue com **hospitais**, **pacientes** e **bolsas de sangue**. Não usa banco de dados: as informações ficam salvas em arquivos JSON.

## Arquivos

| Arquivo | O que é |
|---|---|
| `api.py` | A API, com todas as rotas e validações |
| `hospitais.json` | Hospitais cadastrados (nome, capacidade de leitos, ocupação) |
| `pacientes.json` | Pacientes, com dados de cadastro e informações médicas (tipo sanguíneo, fator RH, data do internamento) |
| `bolsas.json` | Estoque de bolsas de sangue (tipo, fator RH, quantidade) |

Os dados dos JSONs são fictícios, só para testar.

## Como o código funciona

- **`carregar(arquivo)` e `salvar(arquivo, dados)`:** leem e gravam os arquivos JSON. Toda rota carrega o arquivo, faz a alteração e salva de novo.
- **`buscar_por_id(lista, id)`:** percorre a lista e devolve o item com aquele `id`, ou `None` se não encontrar.
- **IDs automáticos:** ao cadastrar, o novo `id` é o maior `id` que já existe mais 1.
- **Validações:** antes de salvar, a API confere se os campos obrigatórios foram enviados e se estão no tipo certo. Quando algo está errado, ela devolve uma mensagem explicando o problema.
- **CORS** liberado com `flask_cors`, para que um front-end (como o Angular) consiga acessar a API.

### Códigos de resposta

| Código | Quando acontece |
|---|---|
| `200` | Busca, atualização ou exclusão feita com sucesso |
| `201` | Cadastro criado |
| `400` | Faltou um campo obrigatório |
| `404` | O item com aquele `id` não existe |
| `422` | O campo foi enviado, mas com um valor inválido (por exemplo, texto onde devia ser número) |

## Rotas

### Hospitais
| Método | Rota | O que faz |
|---|---|---|
| GET | `/hospitais` | Lista todos os hospitais |
| GET | `/hospitais/<id>` | Busca um hospital pelo id |
| POST | `/hospitais` | Cadastra um hospital. Obrigatórios: `nome`, `capacidade` (inteiro), `ocupacao` (inteiro) e `estoque_bolsas` (cada bolsa com `tipo` e `fator_RH` booleano) |
| PUT | `/hospitais/<id>` | Atualiza os dados de um hospital |
| DELETE | `/hospitais/<id>` | Remove um hospital |

### Pacientes
| Método | Rota | O que faz |
|---|---|---|
| GET | `/pacientes` | Lista todos os pacientes |
| GET | `/pacientes/<id>` | Busca um paciente pelo id |
| POST | `/pacientes` | Cadastra um paciente. Dentro de `cadastro`, são obrigatórios: `nome`, `CPF`, `telefone`, `sexo` (`masculino`, `feminino` ou `outro`), `idade` (inteiro) e `endereco` |
| PUT | `/pacientes/<id>` | Atualiza os dados de um paciente |
| DELETE | `/pacientes/<id>` | Remove um paciente |

### Bolsas de sangue
| Método | Rota | O que faz |
|---|---|---|
| GET | `/bolsas` | Lista as bolsas, com filtros opcionais na URL: `/bolsas?tipo=A` ou `/bolsas?tipo=A&urgencia=alta` |
| GET | `/bolsas/<id>` | Busca uma bolsa pelo id |
| POST | `/bolsas` | Cadastra uma bolsa. Dentro de `cadastro`, são obrigatórios: `tipo_sanguineo`, `fator_rh` (booleano) e `quantidade` (inteiro) |
| PUT | `/bolsas/<id>` | Atualiza uma bolsa |
| DELETE | `/bolsas/<id>` | Remove uma bolsa |

### Exemplo de cadastro de paciente (POST `/pacientes`)

```json
{
  "cadastro": [
    {
      "nome": "Maria",
      "CPF": "000.000.000-00",
      "telefone": "45 90000-0000",
      "sexo": "feminino",
      "idade": 30,
      "endereco": "Rua Exemplo, 123"
    }
  ],
  "informacoes_medicas": [
    {
      "altura": 1.65,
      "peso": 60,
      "tipo_sanguineo": "A",
      "fator_RH": true,
      "data_do_internamento": "10/04/2026"
    }
  ]
}
```

## Como rodar

```bash
pip install flask flask-cors
python api.py
```

A API sobe em `http://127.0.0.1:5000`. Para testar as rotas, use o **Postman** (ou o navegador, no caso das rotas GET).
