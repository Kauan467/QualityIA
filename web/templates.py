from src.core.common_imports import *

HTML_MONITORAMENTO_IA = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>ENSINO E DETECÇÃO DE DEFEITOS - IA</title>
    <style>
        :root {
            --primary: #1890ff;
            --success: #52c41a;
            --danger: #ff4d4f;
            --warning: #faad14;
            --background: #0f1b2d;
        }
        
        body { 
            font-family: 'Segoe UI', Arial, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: var(--background);
            color: white;
        }
        
        .container { 
            max-width: 1800px; 
            margin: 0 auto; 
            background: #1a2b3c; 
            padding: 0;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header { 
            background: linear-gradient(135deg, var(--primary), #096dd9); 
            color: white; 
            padding: 25px 40px; 
            text-align: center; 
            border-bottom: 2px solid #1890ff;
        }
        
        .header h1 {
            margin: 0;
            font-size: 2em;
            font-weight: 300;
        }
        
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
        }
        
        .content {
            display: grid;
            grid-template-columns: 1fr 500px;
            gap: 0;
            min-height: 800px;
        }
        
        .camera-section {
            background: #000;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 600px;
            border-right: 2px solid #2d3b4d;
        }
        
        .camera-feed {
            width: 100%;
            min-height: 600px;
            object-fit: contain;
        }
        
        .controls-section {
            background: #1e2f3e;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            overflow-y: auto;
            max-height: 800px;
        }
        
        .panel {
            background: #2d3b4d;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid var(--primary);
        }
        
        .panel-ia {
            border-left-color: #13c2c2;
        }
        
        .panel-treinamento {
            border-left-color: var(--warning);
        }
        
        .status-item {
            display: flex;
            justify-content: space-between;
            margin: 8px 0;
            padding: 8px 0;
            border-bottom: 1px solid #3a4959;
        }
        
        .status-label {
            font-weight: 500;
            color: #a0b3c8;
        }
        
        .status-value {
            font-weight: 600;
            color: white;
        }
        
        .btn { 
            padding: 12px 20px; 
            margin: 8px 0; 
            border: none; 
            border-radius: 6px; 
            cursor: pointer; 
            font-size: 14px;
            font-weight: 600;
            transition: all 0.3s ease;
            width: 100%;
            text-align: center;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        
        .btn-primary {
            background: var(--primary);
            color: white;
        }
        
        .btn-success {
            background: var(--success);
            color: white;
        }
        
        .btn-danger {
            background: var(--danger);
            color: white;
        }
        
        .btn-warning {
            background: var(--warning);
            color: white;
        }
        
        .btn-ia {
            background: #13c2c2;
            color: white;
        }
        
        .stat-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin: 15px 0;
        }
        
        .stat-card {
            background: #3a4959;
            padding: 10px;
            border-radius: 6px;
            text-align: center;
        }
        
        .stat-number {
            font-size: 20px;
            font-weight: bold;
        }
        
        .stat-aprovado {
            color: var(--success);
        }
        
        .stat-reprovado {
            color: var(--danger);
        }
        
        .stat-label {
            font-size: 12px;
            color: #a0b3c8;
        }
        
        .training-progress {
            background: #3a4959;
            border-radius: 10px;
            height: 8px;
            overflow: hidden;
            margin: 10px 0;
        }
        
        .progress-fill {
            background: var(--success);
            height: 100%;
            transition: width 0.3s ease;
        }
        
        .ia-status {
            position: absolute;
            top: 15px;
            left: 15px;
            background: rgba(0,0,0,0.7);
            color: white;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 12px;
            z-index: 10;
        }
        
        .collection-options {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin: 10px 0;
        }
        
        .feedback-message {
            padding: 10px;
            margin: 10px 0;
            border-radius: 6px;
            text-align: center;
            font-weight: 500;
        }
        
        .success-feedback {
            background: rgba(82, 196, 26, 0.2);
            border: 1px solid var(--success);
            color: var(--success);
        }
        
        .error-feedback {
            background: rgba(255, 77, 79, 0.2);
            border: 1px solid var(--danger);
            color: var(--danger);
        }
        
        /* NOVOS ESTILOS PARA MODO ENSINO */
        .teaching-panel {
            background: linear-gradient(135deg, #1890ff, #096dd9);
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            text-align: center;
        }
        
        .defect-categories {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            margin: 10px 0;
        }
        
        .defect-category {
            background: #2d3b4d;
            padding: 10px;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s ease;
            border-left: 4px solid #1890ff;
        }
        
        .defect-category:hover {
            background: #3a4959;
            transform: translateY(-2px);
        }
        
        .category-name {
            font-weight: bold;
            font-size: 12px;
            margin-bottom: 5px;
        }
        
        .category-desc {
            font-size: 10px;
            color: #a0b3c8;
        }
        
        .teaching-instructions {
            background: #f0f8ff;
            color: #1890ff;
            padding: 10px;
            border-radius: 6px;
            margin: 10px 0;
            border-left: 4px solid #1890ff;
        }
        
        .mode-indicator {
            position: absolute;
            top: 15px;
            right: 15px;
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 8px 12px;
            border-radius: 20px;
            font-size: 12px;
            z-index: 10;
        }
        
        .mode-teaching {
            background: rgba(24, 144, 255, 0.8);
        }
        
        .mode-auto {
            background: rgba(82, 196, 26, 0.8);
        }
        
        .defect-stats {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 5px;
            margin: 10px 0;
        }
        
        .defect-stat {
            background: #3a4959;
            padding: 5px;
            border-radius: 4px;
            font-size: 11px;
            text-align: center;
        }
        
        .visualization-info {
            background: #1a3b5c;
            padding: 10px;
            border-radius: 6px;
            margin: 10px 0;
            border-left: 4px solid #13c2c2;
        }
        
        .color-legend {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 5px;
            margin: 10px 0;
        }
        
        .color-item {
            display: flex;
            align-items: center;
            font-size: 10px;
            margin: 2px 0;
        }
        
        .color-box {
            width: 12px;
            height: 12px;
            margin-right: 5px;
            border-radius: 2px;
        }

        /* NOVOS ESTILOS PARA AS FUNCIONALIDADES AVANÇADAS */
        .advanced-tools {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }
        
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            z-index: 1000;
        }
        
        .modal-content {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 20px;
            border-radius: 10px;
            width: 500px;
            max-width: 90%;
            max-height: 90vh;
            overflow-y: auto;
            color: #333;
        }
        
        .modal-large {
            width: 90%;
            max-width: 1000px;
        }
        
        .modal h3 {
            margin-top: 0;
            color: #2c3e50;
        }
        
        .modal-buttons {
            text-align: right;
            margin-top: 20px;
        }
        
        .modal-buttons button {
            padding: 10px 20px;
            margin-left: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        
        .btn-cancel {
            background: #95a5a6;
            color: white;
        }
        
        .btn-confirm {
            background: #27ae60;
            color: white;
        }
        
        .btn-close {
            background: #e74c3c;
            color: white;
        }
        
        .xai-content {
            text-align: center;
            margin: 20px 0;
        }
        
        .xai-image {
            max-width: 100%;
            border: 2px solid #3498db;
            border-radius: 5px;
        }
        
        .xai-explanation {
            margin-top: 10px;
            color: #7f8c8d;
            font-size: 14px;
        }

        /* ESTILOS PARA A BARRA DE PROGRESSO MELHORADA */
        .training-progress {
            background: #2d3b4d;
            border-radius: 10px;
            height: 12px;
            overflow: hidden;
            margin: 10px 0;
            border: 1px solid #3a4959;
        }

        .progress-fill {
            background: linear-gradient(90deg, #1890ff, #52c41a);
            height: 100%;
            transition: width 0.5s ease;
            position: relative;
            overflow: hidden;
        }

        .progress-fill::after {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            animation: shimmer 2s infinite;
        }

        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }

        /* ESTILOS PARA BOTÕES DE STATUS */
        .btn-treinar {
            background: linear-gradient(135deg, #1890ff, #096dd9);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
            width: 100%;
            margin: 8px 0;
        }

        .btn-treinar:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(24, 144, 255, 0.4);
        }

        .btn-treinar:disabled {
            background: #95a5a6;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Quality IA</h1>
        </div>

        <div class="content">
            <div class="camera-section">
                <img id="cameraFeed" class="camera-feed" src="{{ url_for('video_feed') }}" 
                     alt="Monitoramento em tempo real">
                <div class="ia-status" id="iaStatus">
                     MODO: ENSINO
                </div>
                <div class="mode-indicator mode-teaching" id="modeIndicator">
                     MODO ENSINO
                </div>
            </div>

            <div class="controls-section">
                <!-- Painel de Ferramentas -->
                <div class="advanced-tools">
                    <h3>Ferramentas</h3>
                    
                    <button class="btn" onclick="window.open('/dashboard-performance', '_blank')" 
                            style="background: #e74c3c; margin-bottom: 10px;">
                            Dashboard de Performance
                    </button>
                    
                    <button class="btn" onclick="abrirModalCorrecao()" 
                            style="background: #f39c12; margin-bottom: 10px;">
                           Correção Rápida
                    </button>
                    
                    <button class="btn" onclick="gerarExplicacaoXAI()" 
                            style="background: #9b59b6;">
                           Análise de Causa Raiz (XAI)
                    </button>
                </div>

                <!-- Painel de Ensino -->
                <div class="teaching-panel">
                    <h3> CLASSIFIQUE PARA ENSINAR A IA</h3>
                    <p>Quando ver um defeito, clique no tipo específico abaixo:</p>
                </div>

                <!-- Informações de Visualização -->
                <div class="visualization-info">
                    <h4> VISUALIZAÇÃO DE DEFEITOS</h4>
                    <p><strong>Bound Box:</strong> A IA irá marcar os defeitos com bound box com cores específicas para cada erro</p>
                    <div class="color-legend">
                        <div class="color-item">
                            <div class="color-box" style="background: #ffa500;"></div>
                            <span>Rugas</span>
                        </div>
                        <div class="color-item">
                            <div class="color-box" style="background: #ff0000;"></div>
                            <span>Costura</span>
                        </div>
                        <div class="color-item">
                            <div class="color-box" style="background: #0000ff;"></div>
                            <span>Arranhões</span>
                        </div>
                        <div class="color-item">
                            <div class="color-box" style="background: #800080;"></div>
                            <span>Sujeira</span>
                        </div>
                        <div class="color-item">
                            <div class="color-box" style="background: #00ffff;"></div>
                            <span>Montagem</span>
                        </div>
                        <div class="color-item">
                            <div class="color-box" style="background: #00ff00;"></div>
                            <span>Gotejamento</span>
                        </div>
                    </div>
                </div>

                <!-- Categorias de Defeitos para Ensino -->
                <div class="panel">
                    <h3> DEFEITOS ESPECÍFICOS</h3>
                    
                    <div class="teaching-instructions">
                        <strong>COMO ENSINAR:</strong><br>
                        1. Posicione o banco na câmera<br>
                        2. Clique no defeito específico<br>
                        3. A IA guarda esse exemplo<br>
                        4. Repita 50+ vezes por defeito<br>
                        5. Clique em "Treinar IA"
                    </div>
                    
                    <div class="defect-categories">
                        <!-- Categoria: APROVADO -->
                        <div class="defect-category" onclick="classificarManual('APROVADO')">
                            <div class="category-name">APROVADO✅</div>
                            <div class="category-desc">Banco perfeito - dentro do padrão</div>
                        </div>
                        
                        <!-- Categoria: RUGAS -->
                        <div class="defect-category" onclick="classificarManual('RUGAS_TECIDO')">
                            <div class="category-name">RUGAS NO TECIDO</div>
                            <div class="category-desc">Tecido ondulado, mal esticado</div>
                        </div>
                        
                        <!-- Categoria: FALHA DE COSTURA SIMPLIFICADA -->
                        <div class="defect-category" onclick="classificarManual('FALHA_COSTURA')">
                            <div class="category-name">FALHA NA COSTURA</div>
                            <div class="category-desc">Costura irregular ou defeituosa</div>
                        </div>
                        
                        <!-- Categoria: ERROS DE MANUSEIO -->
                        <div class="defect-category" onclick="classificarManual('ERRO_MANUSEIO_ARRANHOES')">
                            <div class="category-name">ARRANHÕES</div>
                            <div class="category-desc">Arranhões no banco</div>
                        </div>
                        
                        <div class="defect-category" onclick="classificarManual('ERRO_MANUSEIO_SUJEIRA')">
                            <div class="category-name">SUJEIRA</div>
                            <div class="category-desc">Manchas do operador</div>
                        </div>
                        
                        <div class="defect-category" onclick="classificarManual('ERRO_MANUSEIO_MONTAGEM')">
                            <div class="category-name">MONTAGEM ERRADA</div>
                            <div class="category-desc">Peças montadas incorretamente</div>
                        </div>
                        
                        <!-- Categoria: DEFEITOS DE PINTURA -->
                        <div class="defect-category" onclick="classificarManual('DEFEITO_PINTURA_GOTEJAMENTO')">
                            <div class="category-name">MANCHAS NO BANCO</div>
                            <div class="category-desc">respingos no banco </div>
                        </div>
                        
                        <!-- Categoria: ESTRUTURA -->
                        <div class="defect-category" onclick="classificarManual('STRUCTURE_TRINCO_DANIFICADO')">
                            <div class="category-name">BASE DO BANCO COM DEFEITO</div>
                            <div class="category-desc">Trincado, quebrado ou torto</div>
                        </div>
                        
                        <div class="defect-category" onclick="classificarManual('STRUCTURE_PARAFUSO_FALTANDO')">
                            <div class="category-name">PARAFUSO FALTANDO</div>
                            <div class="category-desc">Falta de parafusos</div>
                        </div>
                        
                        <div class="defect-category" onclick="classificarManual('STRUCTURE_SOLDA_DEFEITUOSA')">
                            <div class="category-name">SOLDA DEFEITUOSA</div>
                            <div class="category-desc">Solda mal feita, frágil</div>
                        </div>
                    </div>
                </div>

                <!-- Painel de Status -->
                <div class="panel">
                    <h3>STATUS DO SISTEMA</h3>
                    <div class="stat-grid">
                        <div class="stat-card">
                            <div class="stat-number" id="totalFrames">0</div>
                            <div class="stat-label">Frames</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number" id="classificacoesIa">0</div>
                            <div class="stat-label">Classificações</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number stat-aprovado" id="aprovadosIa">0</div>
                            <div class="stat-label">Aprovados</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number stat-reprovado" id="defeitosDetectados">0</div>
                            <div class="stat-label">Defeitos</div>
                        </div>
                    </div>
                    
                    <div class="status-item">
                        <span class="status-label">Amostras Coletadas:</span>
                        <span class="status-value" id="amostrasColetadas">0</span>
                    </div>
                    
                    <div class="status-item">
                        <span class="status-label">Última Detecção:</span>
                        <span class="status-value" id="ultimaClassificacao">-</span>
                    </div>
                    
                    <!-- Estatísticas de Defeitos por Tipo -->
                    <div class="defect-stats" id="defectStats">
                        <!-- Preenchido via JavaScript -->
                    </div>
                </div>

                <!-- Painel de Treinamento -->
                <div class="panel panel-ia">
                    <h3>TREINAMENTO DA IA</h3>
                    
                    <div class="status-item">
                        <span class="status-label">Status IA:</span>
                        <span class="status-value" id="statusIa">MODO ENSINO</span>
                    </div>
                    
                    <div class="status-item">
                        <span class="status-label">Modelo Treinado:</span>
                        <span class="status-value" id="modeloTreinado">Não</span>
                    </div>

                    <div class="status-item">
                        <span class="status-label">Amostras Coletadas:</span>
                        <span class="status-value" id="totalAmostras">0</span>
                    </div>
                    
                    <button class="btn btn-ia" onclick="treinarIA()" id="btnTreinarIa">
                     TREINAR IA COM CLASSIFICAÇÕES
                    </button>
                    
                </div>

                <!-- Feedback -->
                <div id="feedbackArea"></div>

                <!-- Controles -->
                <div style="margin-top: auto; padding-top: 20px; border-top: 1px solid #2d3b4d;">
                    <button class="btn btn-primary" onclick="atualizarStatus()">
                        Atualizar Status
                    </button>
                    <button class="btn" onclick="recarregarCamera()" 
                            style="background: #722ed1; color: white; margin-top: 10px;">
                        Recarregar Câmera
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal para Correção Rápida -->
    <div id="modalCorrecao" class="modal">
        <div class="modal-content">
            <h3>Correção Rápida da IA</h3>
            <p>Corrigir classificação atual da IA:</p>
            
            <div style="margin: 15px 0;">
                <strong>Classificação atual da IA:</strong>
                <span id="classeAtualIa" style="color: #e74c3c; font-weight: bold;"></span>
                <span id="confiancaAtualIa" style="color: #e74c3c;"></span>
            </div>
            
            <label for="classeCorreta">Classificação correta:</label>
            <select id="classeCorreta" style="width: 100%; padding: 10px; margin: 10px 0; border-radius: 5px;">
                <option value="APROVADO">APROVADO ✅</option>
                <option value="RUGAS_TECIDO">RUGAS NO TECIDO</option>
                <option value="FALHA_COSTURA">FALHA NA COSTURA</option>
                <option value="ERRO_MANUSEIO_ARRANHOES">ARRANHÕES</option>
                <option value="ERRO_MANUSEIO_SUJEIRA">SUJEIRA</option>
                <option value="ERRO_MANUSEIO_MONTAGEM">MONTAGEM ERRADA</option>
                <option value="DEFEITO_PINTURA_GOTEJAMENTO">MANCHAS NO BANCO</option>
                <option value="STRUCTURE_TRINCO_DANIFICADO">BASE DO BANCO COM DEFEITO</option>
                <option value="STRUCTURE_PARAFUSO_FALTANDO">PARAFUSO FALTANDO</option>
                <option value="STRUCTURE_SOLDA_DEFEITUOSA">SOLDA DEFEITUOSA</option>
            </select>
            
            <label for="observacoesCorrecao">Observações:</label>
            <textarea id="observacoesCorrecao" style="width: 100%; padding: 10px; margin: 10px 0; border-radius: 5px; height: 80px;" 
                      placeholder="Descreva o que a IA errou..."></textarea>
            
            <div class="modal-buttons">
                <button class="btn-cancel" onclick="fecharModalCorrecao()">Cancelar</button>
                <button class="btn-confirm" onclick="enviarCorrecao()">Confirmar Correção</button>
            </div>
        </div>
    </div>

    <!-- Modal para Explicação XAI -->
    <div id="modalXAI" class="modal">
        <div class="modal-content modal-large">
            <h3>Análise de Causa Raiz (XAI)</h3>
            <p>Regiões da imagem que influenciaram a decisão da IA:</p>
            
            <div id="conteudoXAI" class="xai-content">
                <!-- Conteúdo será preenchido via JavaScript -->
            </div>
            
            <div class="modal-buttons">
                <button class="btn-close" onclick="fecharModalXAI()">Fechar</button>
            </div>
        </div>
    </div>

    <script>

async function atualizarStatus() {
    try {
        const response = await fetch('/status-ia');
        const data = await response.json();
        
        document.getElementById('totalFrames').textContent = data.total_frames.toLocaleString();
        document.getElementById('classificacoesIa').textContent = data.classificacoes_ia;
        document.getElementById('aprovadosIa').textContent = data.aprovados_ia;
        document.getElementById('defeitosDetectados').textContent = data.defeitos_detectados;
        document.getElementById('amostrasColetadas').textContent = data.amostras_coletadas;
        document.getElementById('totalAmostras').textContent = data.amostras_coletadas;
        document.getElementById('statusIa').textContent = data.estado_ia;
        document.getElementById('modeloTreinado').textContent = data.modelo_treinado ? 'Sim' : 'Não';
        
        const iaStatus = document.getElementById('iaStatus');
        if (data.modo_manual) {
            iaStatus.textContent = `MODO: ${data.estado_ia} (MANUAL)`;
            iaStatus.style.background = 'rgba(255, 165, 0, 0.9)';
        } else {
            iaStatus.textContent = `MODO: ${data.estado_ia}`;
            iaStatus.style.background = 'rgba(0, 0, 0, 0.7)';
        }
        
        // Atualiza última classificação
        const ultima = data.ultima_classificacao;
        if (ultima) {
            document.getElementById('ultimaClassificacao').textContent = 
                `${ultima.descricao} (${(ultima.confianca * 100).toFixed(1)}%)`;
            document.getElementById('ultimaClassificacao').style.color = 
                ultima.classe === 'APROVADO' ? '#52c41a' : '#ff4d4f';
        }
        
        // Atualiza indicador de modo
        const modeIndicator = document.getElementById('modeIndicator');
        if (data.estado_ia === 'AUTOMATICO') {
            modeIndicator.textContent = data.modo_manual ? 
                'MODO AUTOMÁTICO (FIXADO)' : 'MODO AUTOMÁTICO';
            modeIndicator.className = 'mode-indicator mode-auto';
        } else if (data.estado_ia === 'TREINANDO') {
            modeIndicator.textContent = 'TREINANDO...';
            modeIndicator.className = 'mode-indicator';
            modeIndicator.style.background = 'rgba(255, 165, 0, 0.8)';
        } else {
            modeIndicator.textContent = data.modo_manual ? 
                'MODO ENSINO' : 'MODO ENSINO';
            modeIndicator.className = 'mode-indicator mode-teaching';
        }
        
        // Atualiza estatísticas de defeitos por tipo
        atualizarEstatisticasDefeitos(data.defeitos_por_tipo);
        
        // Atualiza amostras do disco
        await atualizarAmostrasReais();
        
    } catch (error) {
        console.error('Erro ao atualizar status:', error);
    }
}

function atualizarEstatisticasDefeitos(defeitosPorTipo) {
    const container = document.getElementById('defectStats');
    container.innerHTML = '';
    
    for (const [tipo, quantidade] of Object.entries(defeitosPorTipo)) {
        if (quantidade > 0) {
            const div = document.createElement('div');
            div.className = 'defect-stat';
            div.textContent = `${tipo}: ${quantidade}`;
            container.appendChild(div);
        }
    }
}

async function atualizarAmostrasReais() {
    try {
        const response = await fetch('/estatisticas-amostras');
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('amostrasColetadas').textContent = data.total;
            document.getElementById('totalAmostras').textContent = data.total;
            
            const defectStats = document.getElementById('defectStats');
            if (defectStats) {
                let html = '';
                
                const categorias = [
                    'APROVADO', 'RUGAS_TECIDO', 'FALHA_COSTURA',
                    'ERRO_MANUSEIO_ARRANHOES', 'ERRO_MANUSEIO_SUJEIRA', 
                    'ERRO_MANUSEIO_MONTAGEM', 'DEFEITO_PINTURA_GOTEJAMENTO',
                    'STRUCTURE_TRINCO_DANIFICADO', 'STRUCTURE_PARAFUSO_FALTANDO', 
                    'STRUCTURE_SOLDA_DEFEITUOSA'
                ];
                
                categorias.forEach(cat => {
                    const qtd = data.por_categoria[cat] || 0;
                    const cor = qtd >= 20 ? '#52c41a' : qtd >= 10 ? '#faad14' : '#ff4d4f';
                    const progresso = Math.min((qtd / 20) * 100, 100);
                    
                    html += `
                        <div class="defect-stat" style="margin: 5px 0; padding: 8px; background: rgba(255,255,255,0.05); border-radius: 4px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                                <span style="font-size: 0.85em;">${cat}</span>
                                <strong style="color: ${cor};">${qtd}</strong>
                            </div>
                            <div style="width: 100%; height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px;">
                                <div style="width: ${progresso}%; height: 100%; background: ${cor}; border-radius: 2px;"></div>
                            </div>
                        </div>
                    `;
                });
                
                defectStats.innerHTML = html;
            }
            
            console.log(`Amostras atualizadas: ${data.total} total`);
        }
    } catch (error) {
        console.error('Erro ao atualizar amostras:', error);
    }
}

document.addEventListener('keydown', function(e) {
    if (e.key === 'm' || e.key === 'M') {
        console.log('Alternando modo...');
        
        fetch('/alternar-modo', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                const modoTexto = data.manual ? 
                    `${data.modo} (FIXADO)` : data.modo;
                alert(`Modo alterado para: ${modoTexto}\n\n` +
                      `O modo agora está ${data.manual ? 'TRAVADO' : 'AUTOMÁTICO'}.\n` +
                      `Pressione M novamente para alternar.`);
                
                setTimeout(() => {
                    atualizarStatus();
                }, 500);
            } else {
                alert('Erro: ' + (data.erro || 'Desconhecido'));
            }
        })
        .catch(e => {
            console.error('Erro:', e);
            alert('Erro ao alternar modo: ' + e);
        });
    }
});

async function classificarManual(categoria) {
    const descricoes = {
        'APROVADO': 'Banco dentro do padrão de qualidade',
        'RUGAS_TECIDO': 'Rugas no tecido/estofamento',
        'FALHA_COSTURA': 'Costura irregular ou defeituosa',
        'ERRO_MANUSEIO_ARRANHOES': 'Arranhões causados por ferramentas ou manuseio',
        'ERRO_MANUSEIO_SUJEIRA': 'Sujeira, óleo ou manchas do operador',
        'ERRO_MANUSEIO_MONTAGEM': 'Montagem incorreta de peças',
        'DEFEITO_PINTURA_GOTEJAMENTO': 'Gotejamento ou excesso de tinta',
        'STRUCTURE_TRINCO_DANIFICADO': 'Trinco quebrado ou danificado',
        'STRUCTURE_PARAFUSO_FALTANDO': 'Parafuso faltando na estrutura',
        'STRUCTURE_SOLDA_DEFEITUOSA': 'Solda mal executada ou frágil'
    };
    
    const descricao = descricoes[categoria] || categoria;
    const confirmacao = confirm(`CLASSIFICAR COMO:\n${categoria}\n\n${descricao}\n\nConfirmar?`);
    
    if (!confirmacao) return;
    
    const feedback = document.getElementById('feedbackArea');
    feedback.innerHTML = '<div class="feedback-message"> Ensinando IA...</div>';
    
    try {
        const response = await fetch('/classificar-manual', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                categoria: categoria,
                descricao_detalhada: descricao
            })
        });
        
        const resultado = await response.json();
        
        if (resultado.sucesso) {
            feedback.innerHTML = `
                <div class="feedback-message success-feedback">
                    ✅ ${resultado.mensagem}
                </div>
            `;
            await atualizarStatus();
            await atualizarAmostrasReais();
        } else {
            feedback.innerHTML = `
                <div class="feedback-message error-feedback">
                 ${resultado.mensagem}
                </div>
            `;
        }
        
    } catch (error) {
        feedback.innerHTML = `
            <div class="feedback-message error-feedback">
             Erro: ${error}
            </div>
        `;
    }
}

function simularProgressoTreinamento() {
    const container = document.getElementById('progressoContainer');
    const barra = document.getElementById('progressoBarra');
    const texto = document.getElementById('progressoTexto');
    const etapa = document.getElementById('etapaTreinamento');
    
    container.style.display = 'block';
    
    const etapas = [
        {progresso: 10, texto: "10%", etapa: "Lendo dados de treinamento"},
        {progresso: 25, texto: "25%", etapa: "Pré-processamento de imagens"},
        {progresso: 40, texto: "40%", etapa: "Inicializando rede neural"},
        {progresso: 60, texto: "60%", etapa: "Treinando camadas convolucionais"},
        {progresso: 75, texto: "75%", etapa: "Validando precisão"},
        {progresso: 90, texto: "90%", etapa: "Salvando modelo treinado"},
        {progresso: 100, texto: "100%", etapa: "Treinamento concluído!"}
    ];
    
    let etapaAtual = 0;
    
    const intervalo = setInterval(() => {
        if (etapaAtual < etapas.length) {
            const etapaInfo = etapas[etapaAtual];
            barra.style.width = etapaInfo.progresso + '%';
            texto.textContent = etapaInfo.texto;
            etapa.textContent = etapaInfo.etapa;
            etapaAtual++;
        } else {
            clearInterval(intervalo);
            // Mantém a barra visível por mais 2 segundos
            setTimeout(() => {
                container.style.display = 'none';
            }, 2000);
        }
    }, 3000); // Muda a cada 3 segundos
}


async function treinarIA() {
    const btn = document.getElementById('btnTreinarIa');
    const feedback = document.getElementById('feedbackArea');
    const totalAmostras = parseInt(document.getElementById('amostrasColetadas').textContent);
    if (totalAmostras < 20) {
        feedback.innerHTML = `
            <div class="feedback-message error-feedback">
                Amostras insuficientes!<br>
                Colete pelo menos 20 amostras antes de treinar.<br>
                Atualmente: ${totalAmostras} amostras
            </div>
        `;
        return;
    }
    
    // salva estado original do botão
    const textoOriginal = btn.textContent;
    const corOriginal = btn.style.background;
    
    // atualiza UI para estado de carregamento
    btn.disabled = true;
    btn.textContent = "TREINANDO...";
    btn.style.background = "#f39c12";
    
    simularProgressoTreinamento();
    
    feedback.innerHTML = '<div class="feedback-message">Iniciando treinamento da IA...</div>';
    
    try {
        const response = await fetch('/treinar-ia-manual', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        });
        
        const resultado = await response.json();
        
        if (resultado.sucesso) {
            feedback.innerHTML = `
                <div class="feedback-message success-feedback">
                    ✅ ${resultado.mensagem}
                </div>
                <div class="feedback-message" style="background: #e8f4fd; color: #1890ff; margin-top: 10px;">
                     <strong>Treinamento em andamento:</strong><br>
                    • Processando imagens coletadas<br>
                    • Ajustando pesos da rede neural<br>
                    • Validando precisão<br>
                     Isto pode levar 2-5 minutos...
                </div>
            `;
            
            // Aguarda o treinamento terminar
            await aguardarTreinamentoCompleto();
            
        } else {
            throw new Error(resultado.mensagem);
        }
        
    } catch (error) {
        feedback.innerHTML = `
            <div class="feedback-message error-feedback">
                 Erro: ${error}
            </div>
        `;
    } finally {
        btn.disabled = false;
        btn.textContent = textoOriginal;
        btn.style.background = corOriginal;
    }
}

async function aguardarTreinamentoCompleto() {
    const feedback = document.getElementById('feedbackArea');
    
    const verificarStatus = setInterval(async () => {
        await atualizarStatus();
        const statusIa = document.getElementById('statusIa').textContent;
        
        if (statusIa === 'AUTOMATICO') {
            clearInterval(verificarStatus);
            feedback.innerHTML = `
                <div class="feedback-message success-feedback">
                    🎉 IA TREINADA COM SUCESSO!<br>
                    • Modo automático ativado<br>
                    • Reconhecimento em tempo real<br>
                    • Detecção de múltiplos defeitos
                </div>
            `;
        } else if (statusIa === 'MODO_ENSINO') {
            clearInterval(verificarStatus);
            feedback.innerHTML = `
                <div class="feedback-message error-feedback">
                    ❌ Treinamento falhou!<br>
                    Continue coletando mais amostras e tente novamente.
                </div>
            `;
        }
    }, 3000);
}

function abrirModalCorrecao() {
    const ultimaClassificacao = document.getElementById('ultimaClassificacao').textContent;
    const modal = document.getElementById('modalCorrecao');
    
    if (ultimaClassificacao === '-') {
        alert('Nenhuma classificação disponível para correção.');
        return;
    }
    
    const partes = ultimaClassificacao.split(' (');
    const classe = partes[0];
    const confianca = partes[1] ? partes[1].replace('%)', '') : '0';
    
    document.getElementById('classeAtualIa').textContent = classe;
    document.getElementById('confiancaAtualIa').textContent = ` (${confianca}%)`;
    modal.style.display = 'block';
}

function fecharModalCorrecao() {
    document.getElementById('modalCorrecao').style.display = 'none';
}

async function enviarCorrecao() {
    const classeCorreta = document.getElementById('classeCorreta').value;
    const observacoes = document.getElementById('observacoesCorrecao').value;
    const classeAtual = document.getElementById('classeAtualIa').textContent;
    const confiancaAtual = parseFloat(document.getElementById('confiancaAtualIa').textContent.replace(/[()%]/g, '')) / 100;
    
    try {
        const response = await fetch('/corrigir-classificacao', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                classe_ia: classeAtual,
                confianca_ia: confiancaAtual,
                classe_correta: classeCorreta,
                observacoes: observacoes
            })
        });
        
        const data = await response.json();
        
        if (data.sucesso) {
            alert('✅ ' + data.mensagem);
            fecharModalCorrecao();
            atualizarStatus();
        } else {
            alert('❌ ' + data.mensagem);
        }
    } catch (error) {
        alert('❌ Erro: ' + error);
    }
}

\\xai
async function gerarExplicacaoXAI() {
    const ultimaClassificacao = document.getElementById('ultimaClassificacao').textContent;
    
    if (ultimaClassificacao === '-') {
        alert('Nenhuma classificação disponível para análise.');
        return;
    }
    
    const partes = ultimaClassificacao.split(' (');
    const classe = partes[0];
    const confianca = parseFloat(partes[1].replace('%)', '')) / 100;
    
    try {
        const response = await fetch('/explicacao-xai', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                classe_predita: classe,
                confianca: confianca
            })
        });
        
        const data = await response.json();
        
        if (data.sucesso) {
            const modal = document.getElementById('modalXAI');
            const conteudo = document.getElementById('conteudoXAI');
            
            conteudo.innerHTML = `
                <h4>Explicação para: ${classe} (${(confianca * 100).toFixed(1)}%)</h4>
                <img src="data:image/jpeg;base64,${data.imagem_explicacao}" class="xai-image">
                <div class="xai-explanation">
                    <strong>Áreas em vermelho:</strong> Regiões que mais influenciaram a decisão da IA<br>
                    <strong>Áreas em azul:</strong> Regiões com menor influência
                </div>
            `;
            
            modal.style.display = 'block';
        } else {
            alert('❌ ' + data.mensagem);
        }
    } catch (error) {
        alert('❌ Erro: ' + error);
    }
}

function fecharModalXAI() {
    document.getElementById('modalXAI').style.display = 'none';
}

// ==========================================
// FUNÇÕES AUXILIARES
// ==========================================
function recarregarCamera() {
    fetch('/recarregar-camera')
        .then(response => response.json())
        .then(data => {
            alert(data.mensagem);
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        })
        .catch(error => {
            alert('Erro ao recarregar câmera: ' + error);
        });
}

// Fecha modais ao clicar fora
window.onclick = function(event) {
    const modalCorrecao = document.getElementById('modalCorrecao');
    const modalXAI = document.getElementById('modalXAI');
    
    if (event.target === modalCorrecao) {
        modalCorrecao.style.display = 'none';
    }
    if (event.target === modalXAI) {
        modalXAI.style.display = 'none';
    }
}

// ==========================================
// INICIALIZAÇÃO
// ==========================================
console.log('✅ Sistema de IA carregado');
console.log('⌨️  Pressione M para alternar entre MODO ENSINO e MODO AUTOMÁTICO');
console.log('🔒 O modo ficará TRAVADO até você alternar novamente');

// Atualiza status inicial
atualizarStatus();
atualizarAmostrasReais();

// Atualiza periodicamente
setInterval(atualizarStatus, 3000);
setInterval(atualizarAmostrasReais, 5000);

// Atualiza feed da câmera
setInterval(() => {
    const img = document.getElementById('cameraFeed');
    if (img) {
        img.src = "{{ url_for('video_feed') }}?t=" + new Date().getTime();
    }
}, 100);

    </script>
</body>
</html>
"""