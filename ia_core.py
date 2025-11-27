from common_imports import *
from dashboard import DashboardPerformance, AnaliseCausaRaiz

logger = logging.getLogger(__name__)

class SistemaIATreinamento:
    def __init__(self):
        self.modelo = None
        self.historico_treinamento = None
        # tabela de erros SIMPLIFICADA
        self.classes = [
            'APROVADO',                          #  Banco perfeito ✅
            'RUGAS_TECIDO',                     #  Rugas no tecido
            'FALHA_COSTURA',                    #  Falha na costura (simplificado)
            'ERRO_MANUSEIO_ARRANHOES',          #  Arranhões do operador
            'ERRO_MANUSEIO_SUJEIRA',            #  Sujeira/óleo
            'ERRO_MANUSEIO_MONTAGEM',           #  Montagem incorreta
            'DEFEITO_PINTURA_GOTEJAMENTO',      #  Gotejamento de tinta
            'STRUCTURE_TRINCO_DANIFICADO',      #  Trinco quebrado
            'STRUCTURE_PARAFUSO_FALTANDO',      #  Parafuso faltando
            'STRUCTURE_SOLDA_DEFEITUOSA'        #  Solda ruim
        ]
        self.input_shape = (224, 224, 3)
        self.caminho_modelo = "C:/VisualTrace/IA/modelo_treinado.h5"
        self.caminho_dados = "C:/VisualTrace/IA/DadosTreinamento"
        
        # NOVO: Inicializar dashboard e XAI
        self.dashboard = DashboardPerformance()
        self.analise_causa_raiz = None
        
        self._criar_estrutura()
        self.carregar_modelo()
        
        # Carrega métricas históricas
        self.dashboard.carregar_metricas()
    
    def _criar_estrutura(self):
        """Cria estrutura de pastas para cada tipo específico de defeito"""
        diretorios = ["C:/VisualTrace/IA"]
        
        # para criar pastas da tabela de erros
        for classe in self.classes:
            dir_path = f"C:/VisualTrace/IA/DadosTreinamento/{classe}"
            diretorios.append(dir_path)
        
        diretorios.extend([
            "C:/VisualTrace/IA/Modelos",
            "C:/VisualTrace/IA/Relatorios", 
            "C:/VisualTrace/IA/Logs",
            "C:/VisualTrace/IA/Classificacoes_Manuais",  # para mim classificar
            "C:/VisualTrace/IA/Dashboard",  # NOVO: Pasta para dashboard
            "C:/VisualTrace/IA/Correcoes"   # NOVO: Pasta para correções
        ])
        
        for dir in diretorios:
            Path(dir).mkdir(parents=True, exist_ok=True)
        
        logger.info("📁 Estrutura de IA para defeitos específicos criada")
    
    def criar_modelo(self):
        try:
            # identificar multiplos defeitos
            modelo = keras.Sequential([
                layers.Conv2D(32, (3, 3), activation='relu', input_shape=self.input_shape),
                layers.BatchNormalization(),
                layers.MaxPooling2D(2, 2),
                
                layers.Conv2D(64, (3, 3), activation='relu'),
                layers.BatchNormalization(),
                layers.MaxPooling2D(2, 2),
                
                layers.Conv2D(128, (3, 3), activation='relu'),
                layers.BatchNormalization(),
                layers.MaxPooling2D(2, 2),
                
                layers.Conv2D(256, (3, 3), activation='relu'),
                layers.BatchNormalization(),
                layers.MaxPooling2D(2, 2),
                
                layers.Conv2D(512, (3, 3), activation='relu'),
                layers.BatchNormalization(),
                layers.MaxPooling2D(2, 2),
                
                layers.GlobalAveragePooling2D(),
                layers.Dense(512, activation='relu'),
                layers.Dropout(0.5),
                layers.Dense(256, activation='relu'),
                layers.Dropout(0.3),
                layers.Dense(len(self.classes), activation='softmax')
            ])
            
            modelo.compile(
                optimizer=keras.optimizers.Adam(learning_rate=0.001),
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy', 'precision', 'recall']
            )
            
            self.modelo = modelo
            logger.info("Modelo de IA para defeitos específicos criado!")
            
            # NOVO: Inicializa análise de causa raiz
            self.analise_causa_raiz = AnaliseCausaRaiz(self.modelo, self.classes)
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao criar modelo: {e}")
            return False
    
    def preparar_dados_treinamento(self):
        try:
            X = []
            y = []
            
            for classe_idx, classe in enumerate(self.classes):
                classe_path = os.path.join(self.caminho_dados, classe)
                
                if not os.path.exists(classe_path):
                    logger.warning(f"Diretório {classe} não encontrado")
                    continue
                
                for arquivo in os.listdir(classe_path):
                    if arquivo.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                        caminho_imagem = os.path.join(classe_path, arquivo)
                        
                        try:
                            imagem = Image.open(caminho_imagem)
                            imagem = imagem.convert('RGB')
                            imagem = imagem.resize(self.input_shape[:2])
                            imagem_array = np.array(imagem) / 255.0
                            
                            X.append(imagem_array)
                            y.append(classe_idx)
                            
                        except Exception as e:
                            logger.warning(f"Erro ao processar {arquivo}: {e}")
            
            if len(X) == 0:
                logger.error("❌ Nenhum dado de treinamento encontrado!")
                return None, None, None, None
            
            X = np.array(X)
            y = np.array(y)
            
            X_treino, X_teste, y_treino, y_teste = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            logger.info(f"Dados preparados: {len(X_treino)} treino, {len(X_teste)} teste")
            
            return X_treino, X_teste, y_treino, y_teste
            
        except Exception as e:
            logger.error(f"Erro ao preparar dados: {e}")
            return None, None, None, None
    
    def treinar_modelo(self, epochs=50, batch_size=32):
        try:
            X_treino, X_teste, y_treino, y_teste = self.preparar_dados_treinamento()
            
            if X_treino is None:
                return False
            
            if self.modelo is None:
                self.criar_modelo()
            
            callbacks = [
                keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True),
                keras.callbacks.ReduceLROnPlateau(patience=5, factor=0.5),
                keras.callbacks.ModelCheckpoint(
                    self.caminho_modelo, 
                    save_best_only=True, 
                    monitor='val_accuracy'
                ),
                # NOVO: Callback para atualizar dashboard
                keras.callbacks.LambdaCallback(
                    on_epoch_end=lambda epoch, logs: self.dashboard.adicionar_metricas_treinamento(self.historico_treinamento, epoch)
                )
            ]
            
            self.historico_treinamento = self.modelo.fit(
                X_treino, y_treino,
                batch_size=batch_size,
                epochs=epochs,
                validation_data=(X_teste, y_teste),
                callbacks=callbacks,
                verbose=1
            )
            
            resultado = self.modelo.evaluate(X_teste, y_teste, verbose=0)
            logger.info(f"Modelo treinado! Acurácia: {resultado[1]:.2%}")
            
            # NOVO: Atualiza análise de causa raiz com novo modelo
            self.analise_causa_raiz = AnaliseCausaRaiz(self.modelo, self.classes)
            
            self.salvar_modelo()
            self.gerar_relatorio_treinamento(X_teste, y_teste)
            
            return True
            
        except Exception as e:
            logger.error(f"Erro no treinamento: {e}")
            return False
    
    def classificar_imagem(self, frame):
        try:
            if self.modelo is None:
                return "MODELO_NAO_CARREGADO", 0.0, None
            
            imagem = cv2.resize(frame, self.input_shape[:2])
            imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
            imagem = imagem / 255.0
            imagem = np.expand_dims(imagem, axis=0)
            
            predicoes = self.modelo.predict(imagem, verbose=0)
            classe_idx = np.argmax(predicoes[0])
            confianca = float(predicoes[0][classe_idx])
            
            classe = self.classes[classe_idx]
            
            # retorna as coordenadas simuladas do defeito (para demonstração)
            # detecção por objetos com bounding boxes
            h, w = frame.shape[:2]
            defect_bbox = self._simular_bbox_defeito(classe, w, h)
            
            return classe, confianca, defect_bbox
            
        except Exception as e:
            logger.error(f"Erro na classificação: {e}")
            return "ERRO_CLASSIFICACAO", 0.0, None
    
    def _simular_bbox_defeito(self, classe, img_width, img_height):
        """
        Simula bounding boxes para diferentes tipos de defeitos
        """
        # coordenadas relativas baseadas no tipo de defeito
        defect_locations = {
            'RUGAS_TECIDO': {'x': 0.3, 'y': 0.4, 'w': 0.4, 'h': 0.3},  # centro-superior
            'FALHA_COSTURA': {'x': 0.1, 'y': 0.6, 'w': 0.8, 'h': 0.2},  # horizontal inferior
            'ERRO_MANUSEIO_ARRANHOES': {'x': 0.6, 'y': 0.3, 'w': 0.3, 'h': 0.4},  # lateral direito
            'ERRO_MANUSEIO_SUJEIRA': {'x': 0.2, 'y': 0.7, 'w': 0.3, 'h': 0.2},  # canto inferior esquerdo
            'ERRO_MANUSEIO_MONTAGEM': {'x': 0.5, 'y': 0.1, 'w': 0.4, 'h': 0.3},  # superior direito
            'DEFEITO_PINTURA_GOTEJAMENTO': {'x': 0.7, 'y': 0.6, 'w': 0.25, 'h': 0.3},  # canto inferior direito
            'STRUCTURE_TRINCO_DANIFICADO': {'x': 0.8, 'y': 0.4, 'w': 0.15, 'h': 0.2},  # lateral direito
            'STRUCTURE_PARAFUSO_FALTANDO': {'x': 0.05, 'y': 0.8, 'w': 0.1, 'h': 0.1},  # canto inferior esquerdo
            'STRUCTURE_SOLDA_DEFEITUOSA': {'x': 0.4, 'y': 0.8, 'w': 0.2, 'h': 0.15},  # inferior central
        }
        
        if classe in defect_locations:
            loc = defect_locations[classe]
            x1 = int(loc['x'] * img_width)
            y1 = int(loc['y'] * img_height)
            x2 = int((loc['x'] + loc['w']) * img_width)
            y2 = int((loc['y'] + loc['h']) * img_height)
            return (x1, y1, x2, y2)
        
        return None
    
    def salvar_modelo(self):
        try:
            if self.modelo is not None:
                self.modelo.save(self.caminho_modelo)
                logger.info(f"Modelo salvo em: {self.caminho_modelo}")
                return True
        except Exception as e:
            logger.error(f"Erro ao salvar modelo: {e}")
        return False
    
    def carregar_modelo(self):
        try:
            if os.path.exists(self.caminho_modelo):
                self.modelo = keras.models.load_model(self.caminho_modelo)
                logger.info("Modelo de IA carregado com sucesso!")
                
                # NOVO: Inicializa análise de causa raiz quando carrega modelo
                self.analise_causa_raiz = AnaliseCausaRaiz(self.modelo, self.classes)
                
                return True
            else:
                logger.info("Nenhum modelo treinado encontrado. Criando novo...")
                return self.criar_modelo()
        except Exception as e:
            logger.error(f"Erro ao carregar modelo: {e}")
            return self.criar_modelo()
    
    def gerar_relatorio_treinamento(self, X_teste, y_teste):
        """Gera relatório detalhado do treinamento"""
        try:
            if self.historico_treinamento is None:
                return
            
            # cria gráfico de acurácia
            plt.figure(figsize=(12, 4))
            
            plt.subplot(1, 2, 1)
            plt.plot(self.historico_treinamento.history['accuracy'], label='Treino')
            plt.plot(self.historico_treinamento.history['val_accuracy'], label='Validação')
            plt.title('Acurácia do Modelo')
            plt.ylabel('Acurácia')
            plt.xlabel('Época')
            plt.legend()
            
            plt.subplot(1, 2, 2)
            plt.plot(self.historico_treinamento.history['loss'], label='Treino')
            plt.plot(self.historico_treinamento.history['val_loss'], label='Validação')
            plt.title('Loss do Modelo')
            plt.ylabel('Loss')
            plt.xlabel('Época')
            plt.legend()
            
            relatorio_path = "C:/VisualTrace/IA/Relatorios/relatorio_treinamento.png"
            plt.tight_layout()
            plt.savefig(relatorio_path)
            plt.close()
            
            logger.info(f"Relatório de treinamento salvo: {relatorio_path}")
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório: {e}")

class DetectorDefeitosVisual:
    """Classe para adicionar anotações visuais nos defeitos detectados"""
    
    def __init__(self):
        # cores específicas para cada tipo de defeito
        self.cores_defeitos = {
            'RUGAS_TECIDO': (0, 165, 255),        # laranja
            'FALHA_COSTURA': (255, 0, 0),         # azul
            'ERRO_MANUSEIO_ARRANHOES': (0, 0, 255), # vermelho
            'ERRO_MANUSEIO_SUJEIRA': (128, 0, 128), # roxo
            'ERRO_MANUSEIO_MONTAGEM': (0, 255, 255), # ciano
            'DEFEITO_PINTURA_GOTEJAMENTO': (0, 255, 0), # verde
            'STRUCTURE_TRINCO_DANIFICADO': (255, 165, 0), # laranja escuro
            'STRUCTURE_PARAFUSO_FALTANDO': (128, 128, 128), # cinza
            'STRUCTURE_SOLDA_DEFEITUOSA': (255, 192, 203)  # rosa
        }
        
        self.descricoes_curtas = {
            'RUGAS_TECIDO': 'RUGAS',
            'FALHA_COSTURA': 'COSTURA',
            'ERRO_MANUSEIO_ARRANHOES': 'ARRANHÕES',
            'ERRO_MANUSEIO_SUJEIRA': 'SUJEIRA',
            'ERRO_MANUSEIO_MONTAGEM': 'MONTAGEM ERRADA',
            'DEFEITO_PINTURA_GOTEJAMENTO': 'GOTEJAMENTO',
            'STRUCTURE_TRINCO_DANIFICADO': 'TRINCO DANIF.',
            'STRUCTURE_PARAFUSO_FALTANDO': 'PARAFUSO FALT.',
            'STRUCTURE_SOLDA_DEFEITUOSA': 'SOLDA RUIM'
        }
    
    def adicionar_anotacao_defeito(self, frame, classe, confianca, bbox):
        """adiciona bounding box e texto ao redor do defeito detectado"""
        if classe == 'APROVADO' or bbox is None:
            return frame
        
        # extrai coordenadas da bounding box
        x1, y1, x2, y2 = bbox
        
        # cor baseada no tipo de defeito
        cor = self.cores_defeitos.get(classe, (0, 0, 255))  # Vermelho padrão
        
        # espessura da linha baseada na confiança
        espessura = max(2, int(confianca * 6))
        
        # desenha bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), cor, espessura)
        
        # prepara o texto
        texto_descricao = self.descricoes_curtas.get(classe, classe)
        texto_confianca = f"{confianca:.1%}"
        texto_completo = f"{texto_descricao} ({texto_confianca})"
        
        # tamanho da fonte baseado no tamanho da bounding box
        tamanho_fonte = max(0.5, min(1.0, (x2 - x1) / 300))
        espessura_fonte = max(1, int(tamanho_fonte * 2))
        
        # calcula tamanho do texto para fundo
        (largura_texto, altura_texto), baseline = cv2.getTextSize(
            texto_completo, cv2.FONT_HERSHEY_SIMPLEX, tamanho_fonte, espessura_fonte
        )
        
        # posição do texto (acima da bounding box)
        texto_x = x1
        texto_y = max(y1 - 10, altura_texto + 10)
        
        # desenha fundo para o texto
        cv2.rectangle(frame, 
                     (texto_x, texto_y - altura_texto - 10),
                     (texto_x + largura_texto + 10, texto_y + 10),
                     cor, -1)
        
        # desenha texto
        cv2.putText(frame, texto_completo,
                   (texto_x + 5, texto_y - 5),
                   cv2.FONT_HERSHEY_SIMPLEX, tamanho_fonte,
                   (255, 255, 255), espessura_fonte)
        
        # adiciona ponto central para indicar localização exata
        centro_x = (x1 + x2) // 2
        centro_y = (y1 + y2) // 2
        cv2.circle(frame, (centro_x, centro_y), 5, cor, -1)
        
        return frame
    
    def adicionar_heatmap_defeito(self, frame, classe, bbox):
        """Adiciona um efeito de heatmap ao redor do defeito"""
        if classe == 'APROVADO' or bbox is None:
            return frame
        
        x1, y1, x2, y2 = bbox
        
        # cria máscara para heatmap
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)
        mask = cv2.GaussianBlur(mask, (51, 51), 0)
        
        # cria heatmap (vermelho para defeitos)
        heatmap = np.zeros_like(frame)
        heatmap[:, :, 2] = mask  # Canal vermelho
        
        # combina heatmap com frame original
        alpha = 0.3
        frame = cv2.addWeighted(frame, 1, heatmap, alpha, 0)
        
        return frame

class ColetorDadosIA:
    def __init__(self):
        self.caminho_base = "C:/VisualTrace/IA/DadosTreinamento"
        self.categorias = [
            'APROVADO',
            'RUGAS_TECIDO', 
            'FALHA_COSTURA',
            'ERRO_MANUSEIO_ARRANHOES',
            'ERRO_MANUSEIO_SUJEIRA',
            'ERRO_MANUSEIO_MONTAGEM',
            'DEFEITO_PINTURA_GOTEJAMENTO',
            'STRUCTURE_TRINCO_DANIFICADO',
            'STRUCTURE_PARAFUSO_FALTANDO',
            'STRUCTURE_SOLDA_DEFEITUOSA'
        ]
        
        for categoria in self.categorias:
            Path(os.path.join(self.caminho_base, categoria)).mkdir(parents=True, exist_ok=True)
    
    def salvar_amostra(self, frame, categoria, metadata=None):
        try:
            if categoria not in self.categorias:
                logger.error(f"❌ Categoria inválida: {categoria}")
                return False
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            nome_arquivo = f"{categoria}_{timestamp}.jpg"
            caminho_arquivo = os.path.join(self.caminho_base, categoria, nome_arquivo)
            
            # salvar a imagem
            cv2.imwrite(caminho_arquivo, frame)
            
            # salva metadados detalhados
            if metadata is None:
                metadata = {}
            
            metadata.update({
                'categoria': categoria,
                'timestamp': datetime.now().isoformat(),
                'resolucao': f"{frame.shape[1]}x{frame.shape[0]}",
                'tipo_defeito': self._obter_descricao_defeito(categoria)
            })
            
            metadata_arquivo = caminho_arquivo.replace('.jpg', '_metadata.json')
            with open(metadata_arquivo, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Amostra salva: {categoria} - {self._obter_descricao_defeito(categoria)}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao salvar amostra: {e}")
            return False
    
    def _obter_descricao_defeito(self, categoria):
        """Retorna descrição amigável do tipo de defeito"""
        descricoes = {
            'APROVADO': 'Banco dentro do padrão de qualidade',
            'RUGAS_TECIDO': 'Rugas no tecido/couro',
            'FALHA_COSTURA': 'Falha na costura',
            'ERRO_MANUSEIO_ARRANHOES': 'Arranhões do operador',
            'ERRO_MANUSEIO_SUJEIRA': 'Sujeira do no banco',
            'ERRO_MANUSEIO_MONTAGEM': 'Montagem incorreta',
            'DEFEITO_PINTURA_GOTEJAMENTO': 'Defeito na pintura',
            'STRUCTURE_TRINCO_DANIFICADO': 'estrutura quebrada ou danificada',
            'STRUCTURE_PARAFUSO_FALTANDO': 'Parafuso faltando',
            'STRUCTURE_SOLDA_DEFEITUOSA': 'Solda defeituosa'
        }
        return descricoes.get(categoria, 'Desconhecido')
    
    def get_estatisticas_coleta(self):
        try:
            estatisticas = {}
            total = 0
            
            for categoria in self.categorias:
                categoria_path = os.path.join(self.caminho_base, categoria)
                if os.path.exists(categoria_path):
                    quantidade = len([f for f in os.listdir(categoria_path) if f.endswith('.jpg')])
                    estatisticas[categoria] = quantidade
                    total += quantidade
            
            estatisticas['TOTAL'] = total
            return estatisticas
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {e}")
            return {}