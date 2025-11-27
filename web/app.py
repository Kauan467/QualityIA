import sys
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))


from src.core.common_imports import *
from src.monitoramento.sistema_monitoramento import SistemaMonitoramentoIA
from web.templates import HTML_MONITORAMENTO_IA
from src.core.camera_manager import GerenciadorCamera  

logger = logging.getLogger(__name__)
app = Flask(__name__)

sistema_ia = SistemaMonitoramentoIA()

def generate_frames():
    while True:
        try:
            frame = sistema_ia.get_frame_com_overlay()
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            time.sleep(0.033)
            
        except Exception as e:
            logger.error(f"Erro no streaming: {e}")
            time.sleep(1)

@app.route("/")
def index():
    return render_template_string(HTML_MONITORAMENTO_IA, sistema_ia=sistema_ia)

@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/status-ia")
def status_ia():
    try:
        status = sistema_ia.estatisticas.copy()
        status['modelo_carregado'] = sistema_ia.ia.modelo is not None
        status['camera_ativa'] = sistema_ia.camera.esta_ativa()
        status['nome_ia'] = sistema_ia.nome_ia
        status['versao_ia'] = sistema_ia.versao_ia
        return jsonify(status)
    except Exception as e:
        return jsonify({'erro': str(e)})

@app.route("/classificar-manual", methods=["POST"])
def classificar_manual():
    """Rota para VOCÊ ensinar a IA classificando manualmente"""
    try:
        data = request.json
        categoria = data.get("categoria")
        descricao_detalhada = data.get("descricao_detalhada", "")
        
        # Pega o último frame da câmera
        frame = sistema_ia.ultimo_frame_classificado
        if frame is None:
            return jsonify({
                "sucesso": False,
                "mensagem": "Nenhum frame disponível para classificação"
            })
        
        # Classifica manualmente (você ensina a IA)
        sucesso = sistema_ia.classificar_manual(frame, categoria, descricao_detalhada)
        
        if sucesso:
            return jsonify({
                "sucesso": True,
                "mensagem": f"IA ensinada: {categoria}\n📝 {descricao_detalhada}"
            })
        else:
            return jsonify({
                "sucesso": False,
                "mensagem": "Erro ao classificar manualmente"
            })
            
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "mensagem": f"Erro: {str(e)}"
        })

@app.route("/dashboard-performance")
def dashboard_performance():
    """Rota para o dashboard de performance"""
    try:
        img_data = sistema_ia.get_dashboard_metrics()
        correcao_stats = sistema_ia.get_correction_stats()
        
        html_dashboard = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dashboard de Performance - IA</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
                .header { background: #2c3e50; color: white; padding: 20px; border-radius: 10px; }
                .metrics-container { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin: 20px 0; }
                .chart-section { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                .stats-section { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                .stat-item { margin: 10px 0; padding: 10px; background: #ecf0f1; border-radius: 5px; }
                .nav-buttons { margin: 20px 0; }
                .btn { padding: 10px 20px; margin: 5px; background: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Dashboard de Performance da IA</h1>
                <p>Monitoramento em tempo real das métricas de classificação</p>
            </div>
            
            <div class="nav-buttons">
                <button class="btn" onclick="window.location.href='/'">← Voltar para Monitoramento</button>
                <button class="btn" onclick="location.reload()">Atualizar Dashboard</button>
            </div>
            
            <div class="metrics-container">
                <div class="chart-section">
                    <h2>Métricas de Performance em Tempo Real</h2>
                    {% if grafico_performance %}
                        <img src="data:image/png;base64,{{ grafico_performance }}" style="width: 100%;">
                    {% else %}
                        <p>Nenhum dado de performance disponível ainda.</p>
                    {% endif %}
                </div>
                
                <div class="stats-section">
                    <h2>Estatísticas de Correção</h2>
                    <div class="stat-item">
                        <strong>Total de Correções:</strong> {{ correcao_stats.total_correcoes }}
                    </div>1
                    <div class="stat-item">
                        <strong>Correções Pendentes:</strong> {{ correcao_stats.correcoes_pendentes }}
                    </div>
                    
                    <h3>Tipos de Correção Mais Frequentes:</h3>
                    {% for tipo, quantidade in correcao_stats.correcoes_por_tipo.items() %}
                    <div class="stat-item">
                        <strong>{{ tipo }}:</strong> {{ quantidade }}
                    </div>
                    {% endfor %}
                    
                    <div style="margin-top: 20px; padding: 15px; background: #e8f4fd; border-radius: 5px;">
                        <h4>Insights</h4>
                        <p>• Correções frequentes indicam onde a IA precisa melhorar</p>
                        <p>• Usar informações para focar o treinamento</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        return render_template_string(html_dashboard, 
                                   grafico_performance=img_data,
                                   correcao_stats=correcao_stats)
        
    except Exception as e:
        return jsonify({"erro": str(e)})

@app.route("/corrigir-classificacao", methods=["POST"])
def corrigir_classificacao():
    """Rota para correção rápida de classificação"""
    try:
        data = request.json
        classe_ia = data.get("classe_ia")
        confianca_ia = data.get("confianca_ia")
        classe_correta = data.get("classe_correta")
        observacoes = data.get("observacoes", "")
        
        # Pega o último frame
        frame = sistema_ia.ultimo_frame_classificado
        if frame is None:
            return jsonify({
                "sucesso": False,
                "mensagem": "Nenhum frame disponível para correção"
            })
        
        sucesso = sistema_ia.corrigir_classificacao(
            frame, classe_ia, confianca_ia, classe_correta, observacoes
        )
        
        if sucesso:
            return jsonify({
                "sucesso": True,
                "mensagem": f"Correção registrada: {classe_ia} → {classe_correta}"
            })
        else:
            return jsonify({
                "sucesso": False,
                "mensagem": "Erro ao registrar correção"
            })
            
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "mensagem": f"Erro: {str(e)}"
        })

@app.route("/explicacao-xai", methods=["POST"])
def explicacao_xai():
    """Rota para gerar explicação XAI da classificação"""
    try:
        data = request.json
        classe_predita = data.get("classe_predita")
        confianca = data.get("confianca")
        
        frame = sistema_ia.ultimo_frame_classificado
        if frame is None:
            return jsonify({
                "sucesso": False,
                "mensagem": "Nenhum frame disponível"
            })
        
        explicacao_img, heatmap = sistema_ia.gerar_explicacao_xai(frame, classe_predita, confianca)
        
        if explicacao_img is not None:
            # Converte a imagem para base64
            _, buffer = cv2.imencode('.jpg', explicacao_img)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            
            return jsonify({
                "sucesso": True,
                "imagem_explicacao": img_base64,
                "mensagem": f"Explicação gerada para {classe_predita}"
            })
        else:
            return jsonify({
                "sucesso": False,
                "mensagem": "Erro ao gerar explicação"
            })
            
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "mensagem": f"Erro: {str(e)}"
        })

@app.route("/coletar-amostra", methods=["POST"])
def coletar_amostra():
    try:
        data = request.json
        categoria = data.get("categoria")
        observacoes = data.get("observacoes", "")
        
        resultado = sistema_ia.coletar_amostra(categoria, observacoes)
        return jsonify(resultado)
        
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "mensagem": f"Erro: {str(e)}"
        })

@app.route("/treinar-ia", methods=["POST"])
def treinar_ia():
    try:
        data = request.json
        epochs = data.get("epochs", 50)
        
        resultado = sistema_ia.treinar_ia(epochs=epochs)
        return jsonify(resultado)
        
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "mensagem": f"Erro no treinamento: {str(e)}"
        })

@app.route("/treinar-ia-manual", methods=["POST"])
def treinar_ia_manual():
    """Rota para treinar a IA com todas as classificações manuais"""
    try:
        resultado = sistema_ia.treinar_com_classificacoes_manuais()
        return jsonify(resultado)
        
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "mensagem": f"Erro no treinamento: {str(e)}"
        })

@app.route("/estatisticas-coleta")
def estatisticas_coleta():
    try:
        estatisticas = sistema_ia.coletor.get_estatisticas_coleta()
        return jsonify(estatisticas)
    except Exception as e:
        return jsonify({"erro": str(e)})

@app.route("/recarregar-modelo")
def recarregar_modelo():
    try:
        sucesso = sistema_ia.ia.carregar_modelo()
        if sucesso:
            return jsonify({
                "sucesso": True,
                "mensagem": " Modelo de IA recarregado com sucesso!"
            })
        else:
            return jsonify({
                "sucesso": False,
                "mensagem": " Erro ao recarregar modelo"
            })
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "mensagem": f" Erro: {str(e)}"
        })

@app.route("/recarregar-camera")
def recarregar_camera():
    try:
        sistema_ia.camera.liberar()
        time.sleep(2)
        sistema_ia.camera = GerenciadorCamera()
        return jsonify({
            "sucesso": True,
            "mensagem": " Câmera recarregada com sucesso!"
        })
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "mensagem": f" Erro ao recarregar câmera: {str(e)}"
        })

if __name__ == "__main__":
    logger.info(" SISTEMA DE ENSINO DE IA INICIADO")
    logger.info(f" NOME DA IA: {sistema_ia.nome_ia} v{sistema_ia.versao_ia}")
    logger.info(" CATEGORIAS SIMPLIFICADAS:")
    logger.info("   ✅ APROVADO")
    logger.info("   ❌ RUGAS_TECIDO") 
    logger.info("   ❌ FALHA_COSTURA (simplificada)")
    logger.info("   ❌ ERRO_MANUSEIO_ARRANHOES")
    logger.info("   ❌ ERRO_MANUSEIO_SUJEIRA")
    logger.info("   ❌ ERRO_MANUSEIO_MONTAGEM")
    logger.info("   ❌ DEFEITO_PINTURA_GOTEJAMENTO")
    logger.info("   ❌ STRUCTURE_TRINCO_DANIFICADO")
    logger.info("   ❌ STRUCTURE_PARAFUSO_FALTANDO")
    logger.info("   ❌ STRUCTURE_SOLDA_DEFEITUOSA")
    logger.info(" Acesse: http://localhost:5050")
    
    try:
        app.run(host="0.0.0.0", port=5050, debug=True)
    except KeyboardInterrupt:
        logger.info(" Encerrando sistema...")
    finally:
        sistema_ia.parar_monitoramento()