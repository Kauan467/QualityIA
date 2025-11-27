from src.core.common_imports import *
logger = logging.getLogger(__name__)

class GerenciadorCamera:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None
        self.ultimo_frame = None
        self.frame_lock = threading.Lock()
        self.captura_ativa = True
        self.inicializar_camera()
        
    def inicializar_camera(self):
        logger.info("🎯 Inicializando câmera...")
        
        for i in range(0, 4):
            try:
                logger.info(f"Tentando câmera índice {i}...")
                self.cap = cv2.VideoCapture(i)
                
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                self.cap.set(cv2.CAP_PROP_FPS, 30)
                
                ret, frame = self.cap.read()
                if ret and frame is not None:
                    self.camera_index = i
                    with self.frame_lock:
                        self.ultimo_frame = frame
                    logger.info(f"Câmera encontrada no índice {i}")
                    
                    self.captura_thread = threading.Thread(target=self._captura_continua, daemon=True)
                    self.captura_thread.start()
                    return
                else:
                    self.cap.release()
                    self.cap = None
                    
            except Exception as e:
                logger.error(f"Erro na câmera índice {i}: {e}")
                if self.cap:
                    self.cap.release()
                    self.cap = None
        
        logger.error("❌ Nenhuma câmera encontrada!")
        self.ultimo_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    def _captura_continua(self):
        logger.info("Iniciando captura contínua...")
        
        while self.captura_ativa:
            try:
                if self.cap and self.cap.isOpened():
                    ret, frame = self.cap.read()
                    if ret and frame is not None:
                        with self.frame_lock:
                            self.ultimo_frame = frame.copy()
                    else:
                        logger.warning("Erro ao capturar frame")
                        time.sleep(0.1)
                else:
                    logger.warning("Câmera não disponível")
                    time.sleep(1)
                
                time.sleep(0.033)
                
            except Exception as e:
                logger.error(f"Erro na captura: {e}")
                time.sleep(1)
    
    def get_frame_para_stream(self):
        """Retorna frame para streaming"""
        with self.frame_lock:
            if self.ultimo_frame is not None:
                return self.ultimo_frame.copy()
        
        return np.zeros((480, 640, 3), dtype=np.uint8)
    
    def capturar_frame_qualidade(self):
        """Captura frame com verificação de qualidade"""
        with self.frame_lock:
            if self.ultimo_frame is None:
                return False, None, "Sem frame disponível"
            
            frame = self.ultimo_frame.copy()
        
        # verifica qualidade
        if frame is None or frame.size == 0:
            return False, None, "Frame vazio"
        
        return True, frame, "Qualidade OK"
    
    def esta_ativa(self):
        """Verifica se a câmera está ativa"""
        return self.cap is not None and self.cap.isOpened()
    
    def liberar(self):
        """Libera recursos da câmera"""
        self.captura_ativa = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()