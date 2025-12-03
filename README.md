# QualityIa

Sistema de inspeção visual inteligente para bancos automotivos com IA.
- Detecção de Defeitos**: 10 tipos de defeitos detectados automaticamente
- Validação de Processos**: Verifica se etapas estão sendo seguidas corretamente
- Dashboard: Monitoramento em tempo real com métricas
- IA Explicável: XAI (Explainable AI) mostra por que detectou defeitos
- Relatórios: Geração automática de relatórios de conformidade

Instalação Rápida

```bash
# 1. Clonar repositório
git clone <seu-repo>
cd visual_inspector_ai

# 2. Criar ambiente virtual
python -m venv venv

# 3. Ativar ambiente
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Configurar ambiente
cp .env.example .env
# Editar .env com suas configurações

# 6. Executar
python run.py
```

Estrutura do Projeto

```
visual_inspector_ai/
├── config/           # Configurações
├── src/             # Código fonte
│   ├── core/        # Componentes principais
│   ├── ia/          # Inteligência Artificial
│   ├── deteccao/    # Detecção de defeitos
│   ├── validacao/   # Validação de processos
│   └── ...
├── web/             # Interface Web
├── data/            # Dados e modelos
└── tests/           # Testes
```

Iniciar Sistema
```bash
python run.py
```

Acesse: http://localhost:5050

Treinar IA
1. Cole amostras em `data/treinamento/defeitos/`
2. Acesse interface web
3. Clique em "Treinar IA"

Validar Processo
1. Clique em "Iniciar Novo Banco"
2. Sistema valida automaticamente cada etapa
3. Ao finalizar, gera relatório completo

Documentação

- [Instalação Detalhada](docs/INSTALACAO.md)
- [Guia de Uso](docs/USO.md)
- [API Reference](docs/API.md)
- [Desenvolvimento](docs/DESENVOLVIMENTO.md)

Configuração

Edite `config/config.yaml` para customizar:
- Parâmetros da câmera
- Thresholds de confiança
- Processos de validação
- Categorias de defeitos

Testes

```bash
# Executar todos os testes
pytest tests/

# Teste específico
pytest tests/test_detector.py
```

Status

- Detecção de defeitos funcionando(DONE)
- Interface web operacional(DONE)
- Dashboard de métricas (DONE)
- Validação de processos (em desenvolvimento)
- IA de etapas (em desenvolvimento)

Licença

Proprietary - Todos os direitos reservados

Suporte

Para dúvidas ou problemas, entre em contato.
