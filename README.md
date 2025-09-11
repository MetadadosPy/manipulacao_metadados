# ManipulaçãoMetadados-CPU 2.0

## Descrição
Backend para transcrição automática de vídeos e áudios utilizando o modelo Whisper, com armazenamento dos resultados em banco de dados MySQL. Inclui rotas CRUD para gerenciamento dos vídeos transcritos, facilitando integração com frontend para visualização, cadastro, atualização e exclusão dos registros.

## Especificações Técnicas
- **Framework:** FastAPI
- **Banco de dados:** MySQL
- **Transcrição:** OpenAI Whisper (modelos: tiny, base, small, medium, large)
- **Processamento de áudio/vídeo:** ffmpeg
- **Estrutura de pastas:**
  - `app/` - Código principal do backend
    - `models.py` - Modelo de dados dos vídeos
    - `crud.py` - Funções CRUD para vídeos
    - `database.py` - Conexão com MySQL
    - `config.py` - Configurações do banco
    - `utils.py` - Funções utilitárias
    - `whisper_model.py` - Carregamento do modelo Whisper
    - `audio_processing.py` - Extração de áudio de vídeos
    - `routes/` - Rotas da API
      - `transcribe.py` - Endpoint de transcrição
      - `videos.py` - Endpoints CRUD de vídeos
    - `main.py` - Inicialização da API

## Instalação e Execução
1. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure o banco de dados:**
   - Edite `app/config.py` com suas credenciais MySQL.
   - Execute o script SQL para criar a tabela `videos`.
3. **Execute o backend:**
   ```bash
   uvicorn app.main:app --reload
   ```

## Endpoints da API
### Transcrição
- `POST /transcribe/`
  - Envia um vídeo ou áudio para transcrição.
  - Retorna os segmentos transcritos ou os dados já cadastrados.
  - Exemplo de uso (frontend):
    ```js
    const formData = new FormData();
    formData.append('file', arquivoVideoOuAudio);
    fetch('http://localhost:8000/transcribe/', {
      method: 'POST',
      body: formData
    })
    ```

### CRUD de Vídeos
- `GET /videos` - Lista todos os vídeos cadastrados.
- `POST /videos` - Cria um novo vídeo manualmente.
- `PUT /videos/{video_id}` - Atualiza um vídeo existente.
- `DELETE /videos/{video_id}` - Remove um vídeo do banco.

#### Exemplo de integração (frontend):
```js
// Listar vídeos
fetch('http://localhost:8000/videos')
  .then(res => res.json())
  .then(data => console.log(data));

// Criar vídeo
fetch('http://localhost:8000/videos', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ nome: 'Exemplo', ... })
});

// Atualizar vídeo
fetch('http://localhost:8000/videos/1', {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ nome: 'Novo nome', ... })
});

// Deletar vídeo
fetch('http://localhost:8000/videos/1', {
  method: 'DELETE'
});
```

## Esquema da Tabela `videos`
```sql
CREATE TABLE `videos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) DEFAULT NULL,
  `dados` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`dados`)),
  `nome_arquivo` varchar(255) DEFAULT NULL,
  `caminho_audio` text DEFAULT NULL,
  `caminho_txt` text DEFAULT NULL,
  `caminho_json` text DEFAULT NULL,
  `texto` longtext DEFAULT NULL,
  `idioma` varchar(10) DEFAULT NULL,
  `duracao` decimal(10,2) DEFAULT NULL,
  `data_transcricao` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_nome_arquivo` (`nome_arquivo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
```

## Modelos Whisper
- `tiny` (mais rápido, menos preciso)
- `base` (rápido, precisão intermediária)
- `small` (bom equilíbrio)
- `medium` (mais preciso, mais lento)
- `large` (máxima precisão, mais lento e pesado)

Para trocar o modelo, edite `app/whisper_model.py`:
```python
model = whisper.load_model("tiny")  # ou "base", "small", "medium", "large"
```

## Dicas para manutenção e evolução
- Todas as funções e rotas estão documentadas com docstrings e comentários explicativos.
- Para adicionar novos campos à tabela, atualize o modelo, CRUD e rotas conforme o padrão existente.
- Para integração com frontend, basta consumir os endpoints HTTP já prontos.
- Para novos endpoints, siga o padrão de organização e documentação dos arquivos existentes.
- Para dúvidas sobre o backend, consulte os comentários nos arquivos ou este README.

## Contato e colaboração
- Para dúvidas, sugestões ou colaboração, entre em contato com o responsável pelo backend.
- Pull requests e issues são bem-vindos!

## Requisitos do Sistema
### Mínimos
- **Sistema Operacional:** Windows 10, Linux ou macOS
- **Processador:** Intel i3 ou equivalente
- **Memória RAM:** 4 GB
- **Armazenamento:** 2 GB livres
- **Python:** 3.8 ou superior
- **MySQL:** 5.7 ou superior
- **ffmpeg:** Instalado e disponível no PATH

### Recomendados
- **Sistema Operacional:** Windows 10/11, Ubuntu 20.04+, macOS Monterey+
- **Processador:** Intel i5/i7, AMD Ryzen 5/7 ou superior
- **Memória RAM:** 8 GB ou mais
- **Armazenamento:** SSD com 10 GB livres
- **Python:** 3.11+
- **MySQL:** 8.0+
- **ffmpeg:** Última versão estável
- **GPU:** (Opcional) NVIDIA para aceleração do Whisper (CUDA)
