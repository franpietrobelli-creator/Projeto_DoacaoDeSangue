# Projeto Sangue — API

API REST em Flask feita no 1º semestre de Engenharia de Software (PUCPR) para gerenciar hospitais, pacientes e bolsas de sangue. Os dados ficam em arquivos JSON.

## Rotas

- `GET /hospitais/<int:id>`
- `POST /hospitais`
- `GET /hospitais`
- `PUT /hospitais/<int:id>`
- `DELETE /hospitais/<int:id>`
- `GET /pacientes/<int:id>`
- `POST /pacientes`
- `GET /pacientes`
- `PUT /pacientes/<int:id>`
- `DELETE /pacientes/<int:id>`
- `GET /bolsas/<int:id>`
- `GET /bolsas`
- `POST /bolsas`
- `PUT /bolsas/<int:id>`
- `DELETE /bolsas/<int:id>`

## Como rodar

```bash
pip install flask flask-cors
python api.py
```
