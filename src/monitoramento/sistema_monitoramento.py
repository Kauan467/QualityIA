from src.core.common_imports import *
from src.analise.dashboard import DashboardPerformance, InterfaceCorrecaoRapida, AnaliseCausaRaiz
from src.ia.ia_core import SistemaIATreinamento, DetectorDefeitosVisual, ColetorDadosIA
from src.core.camera_manager import GerenciadorCamera

logger = logging.getLogger(__name__)

class SistemaMonitoramentoIA:
    def __init__(self):
        self.camera = GerenciadorCamera()
        self.ia = SistemaIATreinamento()
        self.coletor = ColetorDadosIA()
        self.detector_visual = DetectorDefeitosVisual()
        
        # NOVO: Inicializar interface de correção
        self.interface_correcao = InterfaceCorrecaoRapida(self)
        
        # NOVO: Adicionar nome da IA
        self.nome_ia = "VisualInspector AI"
        self.versao_ia = "2.0"
        
        # NOVO: Histórico para métricas em tempo real
        self.historico_classificacoes = {
            'y_true': [],
            'y_pred': []
        }
        
        # ensinar a IA
        self.modo_ensino = True
        self.ultimo_frame_classificado = None
        self.aguardando_classificacao = False
        
        # estatísticas detalhadas
        self.estatisticas = {
            'total_frames': 0,
            'classificacoes_ia': 0,
            'aprovados_ia': 0,
            'defeitos_detectados': 0,
            'defeitos_por_tipo': {classe: 0 for classe in self.ia.classes if classe != 'APROVADO'},
            'ultima_classificacao': None,
            'confianca_media': 0.0,
            'estado_ia': 'MODO_ENSINO',  # começa no modo ensino
            'amostras_coletadas': 0,
            'modelo_treinado': False
        }
        
        self.monitorando = True
        self.monitor_thread = threading.Thread(target=self._monitorar_continuo, daemon=True)
        self.monitor_thread.start()
        
        logger.info("SISTEMA EM MODO ENSINO - Classificar manualmente para ensinar a IA")
    
    def classificar_manual(self, frame, categoria, descricao_detalhada=""):
        """VOCÊ ENSINA A IA - Classificação manual com descrição detalhada"""
        try:
            # salva a amostra com metadados
            metadata = {
                'classificado_por': 'Especialista_Qualidade',
                'descricao_detalhada': descricao_detalhada,
                'data_classificacao': datetime.now().isoformat(),
                'tipo_defeito_especifico': categoria,
                'confianca_humana': 1.0,  # tem que ter 100 % de certeza que está ok
                'observacoes_treinamento': f"ENSINADO: {descricao_detalhada}",
                'modo': 'CLASSIFICACAO_MANUAL'
            }
            
            sucesso = self.coletor.salvar_amostra(frame, categoria, metadata)
            
            if sucesso:
                self.estatisticas['amostras_coletadas'] += 1
                logger.info(f"IA ENSINADA: {categoria} - {descricao_detalhada}")

                if categoria != 'APROVADO':
                    self.estatisticas['defeitos_por_tipo'][categoria] += 1
                
                return True
            return False
            
        except Exception as e:
            logger.error(f"Erro ao classificar manualmente: {e}")
            return False

    # NOVO: Método para correção rápida
    def corrigir_classificacao(self, frame, classe_ia, confianca_ia, classe_correta, observacoes=""):
        """Corrige uma classificação da IA e adiciona ao treinamento"""
        return self.interface_correcao.registrar_correcao(
            frame, classe_ia, confianca_ia, classe_correta, observacoes
        )

    # NOVO: Método para gerar explicação XAI
    def gerar_explicacao_xai(self, frame, classe_predita, confianca):
        """Gera explicação XAI para a classificação"""
        if self.ia.analise_causa_raiz:
            return self.ia.analise_causa_raiz.gerar_heatmap_explicacao(frame, classe_predita, confianca)
        return frame, None

    # NOVO: Método para obter dashboard
    def get_dashboard_metrics(self):
        """Retorna dados do dashboard"""
        return self.ia.dashboard.gerar_graficos_performance()

    # NOVO: Método para obter estatísticas de correção
    def get_correction_stats(self):
        """Retorna estatísticas de correção"""
        return self.interface_correcao.get_estatisticas_correcoes()
    
    def _monitorar_continuo(self):
        """Monitoramento - começa no MODO ENSINO, depois muda para MODO AUTOMATICO"""
        while self.monitorando:
            try:
                frame = self.camera.get_frame_para_stream()
                if frame is None:
                    time.sleep(0.1)
                    continue
                
                self.ultimo_frame_classificado = frame.copy()
                
                # só irá classificar automaticamente se o modelo estiver treinado
                if self.estatisticas['modelo_treinado'] and self.ia.modelo is not None:
                    if self.estatisticas['total_frames'] % 10 == 0:
                        classe, confianca, bbox = self.ia.classificar_imagem(frame)
                        
                        if classe in self.ia.classes:
                            self.estatisticas['classificacoes_ia'] += 1
                            self.estatisticas['ultima_classificacao'] = {
                                'classe': classe,
                                'confianca': confianca,
                                'descricao': self._obter_descricao_classe(classe),
                                'bbox': bbox,
                                'timestamp': datetime.now().isoformat(),
                                'modo': 'AUTOMATICO'
                            }
                            
                            if classe == 'APROVADO':
                                self.estatisticas['aprovados_ia'] += 1
                            else:
                                self.estatisticas['defeitos_detectados'] += 1
                                self.estatisticas['defeitos_por_tipo'][classe] += 1
                            
                            # atualiza a "confiança" da IA
                            total_conf = self.estatisticas['confianca_media'] * (self.estatisticas['classificacoes_ia'] - 1)
                            self.estatisticas['confianca_media'] = (total_conf + confianca) / self.estatisticas['classificacoes_ia']
                            
                            self.estatisticas['estado_ia'] = 'AUTOMATICO'
                
                self.estatisticas['total_frames'] += 1
                time.sleep(0.033)
                
            except Exception as e:
                logger.error(f"Erro no monitoramento: {e}")
                time.sleep(1)
    
    def _obter_descricao_classe(self, classe):
        """Retorna descrição amigável da classe"""
        descricoes = {
            'APROVADO': 'Banco Aprovado ✅',
            'RUGAS_TECIDO': 'Rugas no Tecido ❌',
            'FALHA_COSTURA': 'Falha na Costura ❌',
            'ERRO_MANUSEIO_ARRANHOES': 'Erro de Manuseio - Arranhões ❌',
            'ERRO_MANUSEIO_SUJEIRA': 'Erro de Manuseio - Sujeira ❌',
            'ERRO_MANUSEIO_MONTAGEM': 'Erro de Manuseio - Montagem ❌',
            'DEFEITO_PINTURA_GOTEJAMENTO': 'Defeito na Pintura - Gotejamento ❌',
            'STRUCTURE_TRINCO_DANIFICADO': 'Estrutura - Trinco Danificado ❌',
            'STRUCTURE_PARAFUSO_FALTANDO': 'Estrutura - Parafuso Faltando ❌',
            'STRUCTURE_SOLDA_DEFEITUOSA': 'Estrutura - Solda Defeituosa ❌'
        }
        return descricoes.get(classe, classe)
    
    def coletar_amostra(self, categoria, observacoes=""):
        """Coleta amostra com categoria específica de defeito"""
        sucesso, frame, mensagem = self.camera.capturar_frame_qualidade()
        
        if not sucesso:
            return {'sucesso': False, 'mensagem': f"Erro: {mensagem}"}
        
        metadata = {
            'timestamp': datetime.now().isoformat(),
            'observacoes': observacoes,
            'resolucao': f"{frame.shape[1]}x{frame.shape[0]}",
            'operador': 'Sistema',
            'linha_producao': 'Linha 1'
        }
        
        if self.coletor.salvar_amostra(frame, categoria, metadata):
            self.estatisticas['amostras_coletadas'] += 1
            return {
                'sucesso': True, 
                'mensagem': f"Amostra salva: {self.coletor._obter_descricao_defeito(categoria)}"
            }
        else:
            return {'sucesso': False, 'mensagem': "Erro ao salvar amostra"}
    
    def treinar_ia(self, epochs=50):
        logger.info("Iniciando treinamento da IA...")
        self.estatisticas['estado_ia'] = 'TREINANDO'
        
        def treinar_async():
            sucesso = self.ia.treinar_modelo(epochs=epochs)
            if sucesso:
                self.estatisticas['modelo_treinado'] = True
                self.estatisticas['estado_ia'] = 'AUTOMATICO'
                logger.info("IA TREINADA!")
            else:
                self.estatisticas['estado_ia'] = 'MODO_ENSINO'
                logger.error("Falha no treinamento. Continue classificando manualmente.")
        
        threading.Thread(target=treinar_async, daemon=True).start()
        
        return {'sucesso': True, 'mensagem': f"Treinamento iniciado com {epochs} épocas"}
    
    def treinar_com_classificacoes_manuais(self):
        """Treina a IA com TODAS as classificações manuais que você fez"""
        logger.info("Treinando IA com classificações manuais...")
        self.estatisticas['estado_ia'] = 'TREINANDO'
        
        def treinar_async():
            try:
                sucesso = self.ia.treinar_modelo(epochs=50)
                if sucesso:
                    self.estatisticas['modelo_treinado'] = True
                    self.estatisticas['estado_ia'] = 'AUTOMATICO'
                    logger.info("IA TREINADA! Agora reconhece automaticamente os defeitos!")
                else:
                    self.estatisticas['estado_ia'] = 'MODO_ENSINO'
                    logger.error("Falha no treinamento. Continue classificando manualmente.")
            except Exception as e:
                logger.error(f"Erro no treinamento: {e}")
                self.estatisticas['estado_ia'] = 'MODO_ENSINO'
        
        threading.Thread(target=treinar_async, daemon=True).start()
        return {'sucesso': True, 'mensagem': "Treinamento iniciado com classificações manuais"}
    
    def get_frame_com_overlay(self):
        frame = self.camera.get_frame_para_stream()
        if frame is None:
            return None
        
        return self._adicionar_overlay_ia(frame)
    
    def _adicionar_overlay_ia(self, frame):
        try:
            h, w = frame.shape[:2]
            
            cor_status = (0, 255, 0) if self.estatisticas['estado_ia'] == 'AUTOMATICO' else (0, 255, 255)
            if self.estatisticas['estado_ia'] == 'TREINANDO':
                cor_status = (255, 165, 0)
            elif self.estatisticas['estado_ia'] == 'MODO_ENSINO':
                cor_status = (0, 255, 255)
            
            # painel de status
            cv2.rectangle(frame, (10, 10), (w-10, 180), (0, 0, 0), -1)
            cv2.rectangle(frame, (10, 10), (w-10, 180), cor_status, 2)
            
            cv2.putText(frame, f"IA: {self.estatisticas['estado_ia']}", 
                       (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, f"CLASSIFICACOES: {self.estatisticas['classificacoes_ia']}", 
                       (20, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, f"APROVADOS: {self.estatisticas['aprovados_ia']}", 
                       (20, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, f"DEFEITOS: {self.estatisticas['defeitos_detectados']}", 
                       (20, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, f"AMOSTRAS: {self.estatisticas['amostras_coletadas']}", 
                       (20, 125), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, f"CONFIANCA: {self.estatisticas['confianca_media']:.1%}", 
                       (20, 145), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # adiciona anotações visuais se houver defeito detectado
            ultima = self.estatisticas.get('ultima_classificacao')
            if ultima and ultima['classe'] != 'APROVADO' and ultima['bbox'] is not None:
                frame = self.detector_visual.adicionar_anotacao_defeito(
                    frame, ultima['classe'], ultima['confianca'], ultima['bbox']
                )
                
                frame = self.detector_visual.adicionar_heatmap_defeito(
                    frame, ultima['classe'], ultima['bbox']
                )
            
            # texto da última classificação na parte inferior
            if ultima:
                cor_class = (0, 255, 0) if ultima['classe'] == 'APROVADO' else (0, 0, 255)
                texto = f"ULTIMA: {ultima['descricao']} ({ultima['confianca']:.1%})"
                cv2.putText(frame, texto, (20, h-20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, cor_class, 1)
            
            return frame
            
        except Exception as e:
            logger.error(f"Erro no overlay: {e}")
            return frame
    
    def parar_monitoramento(self):
        self.monitorando = False