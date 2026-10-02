# Data Quality Checks

Biblioteca Python leve para validação de qualidade de dados — completude,
unicidade, formato (regex) e faixa de valores — com geração automática de
um **score de 0 a 100** por coluna e um score geral. Sem dependências de
frameworks de teste ou de validação pesados: apenas `pandas` para
manipulação de dados e `Faker` para gerar dados sintéticos de teste.

> Portfólio de análise de dados / governança de dados — foco em qualidade e
> confiabilidade de dados com Python.

## O que este projeto demonstra

Em qualquer pipeline de dados, antes de confiar em um relatório ou em um
modelo, é preciso responder: **os dados estão bons o suficiente?** Este
projeto implementa, de forma simples e reutilizável, os quatro checks de
qualidade mais comuns no dia a dia de um analista/engenheiro de dados:

- **Completude** — quantos valores não estão nulos?
- **Unicidade** — quantos valores são realmente únicos (ex.: chaves
  primárias que não deveriam se repetir)?
- **Faixa de valores** — os valores numéricos estão dentro do esperado
  (ex.: um valor de pedido não pode ser negativo nem absurdamente alto)?
- **Formato (regex)** — o campo segue o padrão esperado (ex.: um e-mail
  válido)?

Os resultados são agregados em um score de 0 a 100 por coluna e em um score
geral do dataset, através da classe `DataQualityReport`.

## Estrutura do repositório

```
src/
  data_quality/
    __init__.py
    checks.py          # funções de check + DataQualityReport
  generate_sample_data.py  # gera um CSV sintético (Faker) com problemas propositais
  run_report.py             # carrega o CSV e imprime o relatório de qualidade
tests/
  test_checks.py        # testes de sanidade (assert-based, sem pytest)
requirements.txt
```

## Como executar

```bash
# 1. Instale as dependências
pip install -r requirements.txt

# 2. Gere um dataset sintético (~500 linhas, com problemas injetados de propósito)
python src/generate_sample_data.py

# 3. Rode o relatório de qualidade de dados
python src/run_report.py

# 4. (opcional) Rode os testes
python -m tests.test_checks
```

O dataset gerado (`data/customers_orders.csv`) é 100% sintético — nomes,
e-mails e datas fake via `Faker`, com nulos, duplicidades e e-mails
malformados injetados deliberadamente (~8% das linhas) para que os checks
tenham algo real para detectar. O arquivo não é versionado (veja
`.gitignore`) por ser reproduzível a partir do script.

## Exemplo de saída do `run_report.py`

```
Linhas avaliadas: 500

=== Data Quality Report ===

country              score: 100.00 / 100
customer_id          score:  95.60 / 100
customer_name        score: 100.00 / 100
email                score:  90.30 / 100
order_amount         score:  96.40 / 100
order_date           score: 100.00 / 100
order_id             score: 100.00 / 100

OVERALL              score:  97.47 / 100
```

(valores ilustrativos — a saída real depende da geração aleatória, ainda
que com seed fixa para reprodutibilidade)

## API da biblioteca

```python
from data_quality import DataQualityReport, check_completeness

# uso direto de uma função de check
scores = check_completeness(df, ["email", "order_amount"])

# uso agregando várias checks em um relatório
report = DataQualityReport()
report.add_completeness(df, ["email", "order_amount"])
report.add_uniqueness(df, ["customer_id"])
report.add_value_range(df, "order_amount", 0, 5000)
report.add_regex_format(df, "email", r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

print(report.render())
print(report.overall_score())
```

## Habilidades demonstradas

- Design de uma pequena biblioteca Python reutilizável (funções puras +
  uma classe de agregação), sem dependências desnecessárias
- Manipulação de dados tabulares com `pandas`
- Geração de dados sintéticos realistas com `Faker`, incluindo injeção
  deliberada de defeitos para validar a própria lógica de checagem
- Expressões regulares aplicadas a validação de formato
- Testes de sanidade simples e diretos (sem depender de um framework de
  testes), cobrindo o caminho feliz e casos de borda (dataframe vazio,
  múltiplos checks por coluna)

## Licença

Distribuído sob a licença MIT — veja [LICENSE](LICENSE).
