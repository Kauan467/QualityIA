from common_imports import *
logger = logging.getLogger(__name__)

class DashboardPerformance:
    """Dashboard de Performance em Tempo Real"""
    
    def __init__(self):
        self.historico_metricas = {
            'timestamp': [],
            'acuracia': [],
            'precisao': [],
            'recall': [],
            'f1_score': [],
            'perdas_treino': [],
            'perdas_validacao': []
        }
        self.caminho_dashboard = "C:/VisualTrace/IA/Dashboard"
        Path(self.caminho_dashboard).mkdir(parents=True, exist_ok=True)
    
    def adicionar_metricas_treinamento(self, historico, epoch):
        """Adiciona métricas do treinamento ao histórico"""
        try:
            timestamp = datetime.now()
            
            # Últimos valores da época atual
            acuracia = historico.history['accuracy'][-1]
            precisao = historico.history['precision'][-1]
            recall = historico.history['recall'][-1]
            loss_treino = historico.history['loss'][-1]
            
            # Validação se disponível
            loss_val = historico.history.get('val_loss', [0])[-1]
            val_accuracy = historico.history.get('val_accuracy', [0])[-1]
            
            self.historico_metricas['timestamp'].append(timestamp)
            self.historico_metricas['acuracia'].append(acuracia)
            self.historico_metricas['precisao'].append(precisao)
            self.historico_metricas['recall'].append(recall)
            self.historico_metricas['f1_score'].append(2 * (precisao * recall) / (precisao + recall + 1e-7))
            self.historico_metricas['perdas_treino'].append(loss_treino)
            self.historico_metricas['perdas_validacao'].append(loss_val)
            
            self.salvar_metricas()
            
        except Exception as e:
            logger.error(f"Erro ao adicionar métricas: {e}")
    
    def adicionar_metricas_tempo_real(self, y_true, y_pred, classes):
        """Adiciona métricas de classificação em tempo real"""
        try:
            if len(y_true) == 0 or len(y_pred) == 0:
                return
            
            timestamp = datetime.now()
            acuracia = np.mean(np.array(y_true) == np.array(y_pred))
            
            # Calcula precisão e recall para cada classe
            precisao_macro = precision_score(y_true, y_pred, average='macro', zero_division=0)
            recall_macro = recall_score(y_true, y_pred, average='macro', zero_division=0)
            f1 = f1_score(y_true, y_pred, average='macro', zero_division=0)
            
            self.historico_metricas['timestamp'].append(timestamp)
            self.historico_metricas['acuracia'].append(acuracia)
            self.historico_metricas['precisao'].append(precisao_macro)
            self.historico_metricas['recall'].append(recall_macro)
            self.historico_metricas['f1_score'].append(f1)
            self.historico_metricas['perdas_treino'].append(0)  # Placeholder
            self.historico_metricas['perdas_validacao'].append(0)  # Placeholder
            
            # Mantém apenas os últimos 100 pontos
            for key in self.historico_metricas:
                if len(self.historico_metricas[key]) > 100:
                    self.historico_metricas[key] = self.historico_metricas[key][-100:]
            
            self.salvar_metricas()
            
        except Exception as e:
            logger.error(f"Erro ao adicionar métricas tempo real: {e}")
    
    def gerar_graficos_performance(self):
        """Gera gráficos de performance para o dashboard"""
        try:
            if len(self.historico_metricas['timestamp']) == 0:
                return None
            
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle('Dashboard de Performance da IA - Tempo Real', fontsize=16, fontweight='bold')
            
            # Gráfico 1: Acurácia e F1-Score
            axes[0, 0].plot(self.historico_metricas['timestamp'], self.historico_metricas['acuracia'], 
                           label='Acurácia', linewidth=2, color='blue')
            axes[0, 0].plot(self.historico_metricas['timestamp'], self.historico_metricas['f1_score'], 
                           label='F1-Score', linewidth=2, color='green')
            axes[0, 0].set_title('Acurácia e F1-Score')
            axes[0, 0].set_ylabel('Métrica')
            axes[0, 0].legend()
            axes[0, 0].grid(True, alpha=0.3)
            axes[0, 0].tick_params(axis='x', rotation=45)
            
            # Gráfico 2: Precisão e Recall
            axes[0, 1].plot(self.historico_metricas['timestamp'], self.historico_metricas['precisao'], 
                           label='Precisão', linewidth=2, color='red')
            axes[0, 1].plot(self.historico_metricas['timestamp'], self.historico_metricas['recall'], 
                           label='Recall', linewidth=2, color='orange')
            axes[0, 1].set_title('Precisão e Recall')
            axes[0, 1].set_ylabel('Métrica')
            axes[0, 1].legend()
            axes[0, 1].grid(True, alpha=0.3)
            axes[0, 1].tick_params(axis='x', rotation=45)
            
            # Gráfico 3: Loss de Treino e Validação
            if any(loss != 0 for loss in self.historico_metricas['perdas_treino']):
                axes[1, 0].plot(self.historico_metricas['timestamp'], self.historico_metricas['perdas_treino'], 
                               label='Loss Treino', linewidth=2, color='purple')
                axes[1, 0].plot(self.historico_metricas['timestamp'], self.historico_metricas['perdas_validacao'], 
                               label='Loss Validação', linewidth=2, color='brown')
                axes[1, 0].set_title('Loss de Treinamento')
                axes[1, 0].set_ylabel('Loss')
                axes[1, 0].legend()
                axes[1, 0].grid(True, alpha=0.3)
                axes[1, 0].tick_params(axis='x', rotation=45)
            
            # Gráfico 4: Métricas Consolidadas
            time_points = range(len(self.historico_metricas['timestamp']))
            axes[1, 1].plot(time_points, self.historico_metricas['acuracia'], label='Acurácia', color='blue')
            axes[1, 1].plot(time_points, self.historico_metricas['precisao'], label='Precisão', color='red')
            axes[1, 1].plot(time_points, self.historico_metricas['recall'], label='Recall', color='orange')
            axes[1, 1].plot(time_points, self.historico_metricas['f1_score'], label='F1-Score', color='green')
            axes[1, 1].set_title('Todas as Métricas (Normalizado)')
            axes[1, 1].set_xlabel('Tempo/Amostras')
            axes[1, 1].set_ylabel('Valor')
            axes[1, 1].legend()
            axes[1, 1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Salva a imagem
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
            img_buffer.seek(0)
            img_data = base64.b64encode(img_buffer.getvalue()).decode()
            plt.close()
            
            return img_data
            
        except Exception as e:
            logger.error(f"Erro ao gerar gráficos: {e}")
            return None
    
    def salvar_metricas(self):
        """Salva as métricas em arquivo JSON"""
        try:
            metricas_path = os.path.join(self.caminho_dashboard, "metricas_performance.json")
            
            # Converte timestamps para string
            metricas_salvar = self.historico_metricas.copy()
            metricas_salvar['timestamp'] = [ts.isoformat() for ts in metricas_salvar['timestamp']]
            
            with open(metricas_path, 'w', encoding='utf-8') as f:
                json.dump(metricas_salvar, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Erro ao salvar métricas: {e}")
    
    def carregar_metricas(self):
        """Carrega métricas salvas"""
        try:
            metricas_path = os.path.join(self.caminho_dashboard, "metricas_performance.json")
            if os.path.exists(metricas_path):
                with open(metricas_path, 'r', encoding='utf-8') as f:
                    metricas_carregadas = json.load(f)
                
                # Converte strings de volta para datetime
                self.historico_metricas['timestamp'] = [datetime.fromisoformat(ts) for ts in metricas_carregadas['timestamp']]
                for key in ['acuracia', 'precisao', 'recall', 'f1_score', 'perdas_treino', 'perdas_validacao']:
                    self.historico_metricas[key] = metricas_carregadas[key]
                    
        except Exception as e:
            logger.error(f"Erro ao carregar métricas: {e}")

class InterfaceCorrecaoRapida:
    """Interface para Correção Rápida de classificações da IA"""
    
    def __init__(self, sistema_ia):
        self.sistema_ia = sistema_ia
        self.correcoes_pendentes = []
        self.historico_correcoes = []
        self.caminho_correcoes = "C:/VisualTrace/IA/Correcoes"
        Path(self.caminho_correcoes).mkdir(parents=True, exist_ok=True)
    
    def registrar_correcao(self, frame, classe_ia, confianca_ia, classe_correta, observacoes=""):
        """Registra uma correção feita pelo operador"""
        try:
            correcao_id = f"correcao_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
            
            correcao_data = {
                'id': correcao_id,
                'timestamp': datetime.now().isoformat(),
                'classe_ia': classe_ia,
                'confianca_ia': confianca_ia,
                'classe_correta': classe_correta,
                'observacoes': observacoes,
                'processada': False
            }
            
            # Salva a imagem da correção
            img_path = os.path.join(self.caminho_correcoes, f"{correcao_id}.jpg")
            cv2.imwrite(img_path, frame)
            
            # Salva metadados
            metadata_path = os.path.join(self.caminho_correcoes, f"{correcao_id}.json")
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(correcao_data, f, indent=2, ensure_ascii=False)
            
            self.correcoes_pendentes.append(correcao_data)
            self.historico_correcoes.append(correcao_data)
            
            logger.info(f"Correção registrada: {classe_ia} -> {classe_correta}")
            
            # Adiciona automaticamente ao conjunto de treinamento
            self._adicionar_ao_treinamento(frame, classe_correta, correcao_data)
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao registrar correção: {e}")
            return False
    
    def _adicionar_ao_treinamento(self, frame, classe_correta, metadata):
        """Adiciona a correção ao conjunto de treinamento"""
        try:
            # Usa o coletor existente para salvar a amostra
            metadata_treinamento = {
                'origem': 'correcao_rapida',
                'correcao_id': metadata['id'],
                'classe_anterior_ia': metadata['classe_ia'],
                'confianca_anterior': metadata['confianca_ia'],
                'observacoes': metadata['observacoes'],
                'timestamp_correcao': metadata['timestamp']
            }
            
            sucesso = self.sistema_ia.coletor.salvar_amostra(frame, classe_correta, metadata_treinamento)
            
            if sucesso:
                # Marca como processada
                for correcao in self.correcoes_pendentes:
                    if correcao['id'] == metadata['id']:
                        correcao['processada'] = True
                        break
                
                logger.info(f"Correção adicionada ao treinamento: {classe_correta}")
                
                # Dispara retreinamento automático se há muitas correções
                if len([c for c in self.correcoes_pendentes if c['processada']]) >= 10:
                    self._sugerir_retreinamento()
            
            return sucesso
            
        except Exception as e:
            logger.error(f"Erro ao adicionar ao treinamento: {e}")
            return False
    
    def _sugerir_retreinamento(self):
        """Sugere retreinamento quando há correções suficientes"""
        logger.info("⚠️ 10+ correções pendentes - Sugerindo retreinamento da IA...")
        # Esta sugestão pode ser mostrada na interface
    
    def get_estatisticas_correcoes(self):
        """Retorna estatísticas das correções"""
        total_correcoes = len(self.historico_correcoes)
        correcoes_pendentes = len([c for c in self.correcoes_pendentes if not c['processada']])
        
        # Contagem por tipo de correção
        correcoes_por_tipo = {}
        for correcao in self.historico_correcoes:
            chave = f"{correcao['classe_ia']}→{correcao['classe_correta']}"
            correcoes_por_tipo[chave] = correcoes_por_tipo.get(chave, 0) + 1
        
        return {
            'total_correcoes': total_correcoes,
            'correcoes_pendentes': correcoes_pendentes,
            'correcoes_por_tipo': correcoes_por_tipo
        }

class AnaliseCausaRaiz:
    """Análise de Causa Raiz usando técnicas de XAI (Explainable AI)"""
    
    def __init__(self, modelo, classes):
        self.modelo = modelo
        self.classes = classes
    
    def gerar_heatmap_explicacao(self, frame, classe_predita, confianca):
        """Gera heatmap explicativo usando Grad-CAM"""
        try:
            # Preprocessamento da imagem
            img_array = self._preprocessar_imagem(frame)
            
            # Cria modelo para Grad-CAM
            grad_model = tf.keras.models.Model(
                inputs=[self.modelo.inputs],
                outputs=[self.modelo.get_layer('conv2d_4').output, self.modelo.output]
            )
            
            # Calcula gradientes
            with tf.GradientTape() as tape:
                conv_outputs, predictions = grad_model(img_array)
                loss = predictions[:, self.classes.index(classe_predita)]
            
            # Extrai gradientes
            grads = tape.gradient(loss, conv_outputs)
            pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
            
            # Combina mapas de ativação com gradientes
            conv_outputs = conv_outputs[0]
            heatmap = tf.reduce_mean(tf.multiply(pooled_grads, conv_outputs), axis=-1)
            
            # Processa heatmap
            heatmap = np.maximum(heatmap, 0)
            heatmap /= np.max(heatmap) + 1e-8
            
            # Redimensiona heatmap para tamanho original
            heatmap = cv2.resize(heatmap, (frame.shape[1], frame.shape[0]))
            heatmap = np.uint8(255 * heatmap)
            
            # Aplica colormap
            heatmap_colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
            
            # Combina com imagem original
            explicacao = cv2.addWeighted(frame, 0.6, heatmap_colored, 0.4, 0)
            
            return explicacao, heatmap
            
        except Exception as e:
            logger.error(f"Erro ao gerar heatmap XAI: {e}")
            # Fallback: retorna imagem original com bounding box
            return self._fallback_explicacao(frame, classe_predita), None
    
    def _preprocessar_imagem(self, frame):
        """Preprocessa imagem para o modelo"""
        img = cv2.resize(frame, (224, 224))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img / 255.0
        img = np.expand_dims(img, axis=0)
        return img
    
    def _fallback_explicacao(self, frame, classe_predita):
        """Fallback quando o XAI não funciona - destaca áreas comuns do defeito"""
        h, w = frame.shape[:2]
        
        # Áreas de interesse baseadas no tipo de defeito
        areas_interesse = {
            'RUGAS_TECIDO': [(w//4, h//4, w//2, h//2)],  # Centro
            'FALHA_COSTURA': [(0, h*3//4, w, h//8)],  # Horizontal inferior
            'ERRO_MANUSEIO_ARRANHOES': [(w//2, h//4, w//2, h//2)],  # Lateral direita
            'ERRO_MANUSEIO_SUJEIRA': [(w//4, h*3//4, w//2, h//4)],  # Inferior esquerdo
            'ERRO_MANUSEIO_MONTAGEM': [(w*3//4, h//2, w//4, h//2)],  # Lateral direita
        }
        
        explicacao = frame.copy()
        
        if classe_predita in areas_interesse:
            for area in areas_interesse[classe_predita]:
                x, y, w_area, h_area = area
                cv2.rectangle(explicacao, (x, y), (x + w_area, y + h_area), (0, 255, 255), 3)
                cv2.putText(explicacao, "AREA SUSPEITA", (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        return explicacao
    
    def gerar_relatorio_explicacao(self, frame, classe_predita, confianca, heatmap):
        """Gera relatório detalhado da explicação"""
        try:
            # Cria figura com subplots
            fig, axes = plt.subplots(1, 3, figsize=(15, 5))
            fig.suptitle(f'Análise de Causa Raiz - {classe_predita} (Confiança: {confianca:.1%})', 
                        fontsize=16, fontweight='bold')
            
            # Imagem original
            axes[0].imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            axes[0].set_title('Imagem Original')
            axes[0].axis('off')
            
            # Heatmap
            if heatmap is not None:
                axes[1].imshow(heatmap, cmap='jet')
                axes[1].set_title('Mapa de Ativação (Grad-CAM)')
                axes[1].axis('off')
            else:
                axes[1].imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                axes[1].set_title('Áreas de Interesse (Fallback)')
                axes[1].axis('off')
            
            # Imagem combinada
            explicacao_img, _ = self.gerar_heatmap_explicacao(frame, classe_predita, confianca)
            axes[2].imshow(cv2.cvtColor(explicacao_img, cv2.COLOR_BGR2RGB))
            axes[2].set_title('Explicação Sobreposta')
            axes[2].axis('off')
            
            plt.tight_layout()
            
            # Converte para base64
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
            img_buffer.seek(0)
            img_data = base64.b64encode(img_buffer.getvalue()).decode()
            plt.close()
            
            return img_data
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório XAI: {e}")
            return None