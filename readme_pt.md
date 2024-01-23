© Danilo Florentino Maia, 2024

# Processador de Texto PI

## Visão Geral

O Processador de Texto PI é uma ferramenta experimental baseada em Python projetada para converter textos em inglês para o formato PI. O formato PI, também conhecido como Ortografia Didática PI, é uma adaptação da ortografia inglesa projetada para facilitar o aprendizado da pronúncia e compreensão oral do inglês.

## Propósito

Este instrumento desempenha um papel central no projeto de pesquisa entitulado "Didática com Estratégias de Andaime", que pretende investigar e comparar a eficiência de diferentes metodologias para o ensino de pronúncia e compreensão oral. Um das metodologias investigadas é o Método PI, uma nova abordagem didática que propõe integrar estratégias educacionais individualizáveis com ferramentas audiovisuais inteligentes, em busca de tornar o aprendizado fonético mais eficiente e engajador.

## Componentes

- **Arquivos Python**:

  - `main.py`: O script principal para execução de comandos.
  - `config.py`: Definições de configuração.
  - `transcriber.py`: Lida com a transcrição do inglês padrão (SE) para PI.
  - `dictionary.py`: Gerencia o dicionário SE para PI.
  - `corpora_manager.py`: Gerencia arquivos de corpus para atualizações de dicionário.

- **Arquivos de Corpus**:

  - `corpus_misc.txt` e `corpus_1000.txt`: Contêm mapeamentos para a transcrição do SE para PI.

- **Arquivos de Dicionário**:

  - `pi_dictionary.json`: Dicionário de conversão.
  - `dictionary_schema.json`: Schema do dicionário.

- **Documentação**:
  - `corpus_info.md`: Informações sobre a estrutura dos arquivos de corpus.
  - `transcriber_steps.md`: Informações sobre as etapas de transcrição implementadas pelo programa.
  - `Manifesto do PI.pdf`: Pitch abrangente que defende a existência da metodologia PI.
  - `Resumo da ODPI v2.1.pdf`: Resumo da Ortografia Didática PI.

## Instalação

1. Instale o Python 3.x.
2. Clone/baixe o código-fonte.
3. Instale as dependências: `pip install -r requirements.txt`.

## Uso

A ferramenta oferece uma CLI para converter textos em inglês padrão para PI, suportando uma variedade de opções.

### Comando Transcribe

Converte texto em inglês padrão para PI usando várias opções.

```
python main.py transcribe [--text TEXT] [--file FILE] [--output OUTPUT] [--variation VARIATION]
```

- `--text TEXT`: Especifique o texto.
- `--file FILE`: Local do arquivo de texto em inglês.
- `--output OUTPUT`: Local de saída para o texto convertido.
- `--variation VARIATION`: Variação do formato PI (L1, L2, L3, ou FM).

### Modo Interativo

Para transcrição em tempo real, use a opção `--interactive`:

```
python main.py transcribe --interactive
```

## Contexto e Metodologia da Pesquisa

- **Desenvolvimento de Algoritmos de PLN**: Analisando padrões de pronúncia para aprimorar abordagens de aprendizagem com andaime.
- **Abordagem Centrada no Usuário**: Ciclo de feedback para melhoria do sistema, focando em adaptabilidade e individualização.

## Impacto e Visão

- **Melhorias nas Habilidades Linguísticas**: Avanços nas habilidades de pronúncia e compreensão oral.
- **Sistema de Aprendizagem Adaptativo**: Um sistema de IA que adapta estratégias de ensino às necessidades dos alunos.
- **Colaboração Interdisciplinar**: Colaboração em linguística, pedagogia e ciência da computação.

## Desafios e Direções Futuras

- **Aceitação Acadêmica e Implementação Prática**: Abordando desafios na aceitação acadêmica e implementação prática.
- **Escalabilidade e Recursos**: Discutindo escalabilidade e necessidades de recursos para expansão para diferentes idiomas e contextos educacionais.

## Considerações Éticas e Medição de Impacto

- **Adesão às Diretrizes Éticas**: Seguindo diretrizes éticas na coleta e análise de dados.

- **Medição de Impacto**: Avaliações de desempenho, análise estatística e pesquisas de satisfação.

## Conclusão

O Processador de Texto PI é um componente fundamental em um projeto de pesquisa ambicioso, buscando revolucionar o ensino de idiomas com métodos aprimorados pela IA, especialmente em pronúncia e compreensão oral.

## Contribuição

Contribuições são bem-vindas. Consulte `CONTRIBUTING.md` para orientações.

## Licença

Este trabalho está licenciado sob a Licença Internacional Creative Commons Attribution 4.0. Para visualizar uma cópia desta licença, visite [http://creativecommons.org/licenses/by/4.0/](http://creativecommons.org/licenses/by/4.0/) ou envie uma carta para Creative Commons, PO Box 1866, Mountain View, CA 94042, EUA.

## Contato

Para consultas ou assistência, entre em contato com [contact@thepimethod.org](mailto:contact@thepimethod.org).

---

© Danilo Florentino Maia, 2024
