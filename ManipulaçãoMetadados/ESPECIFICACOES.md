# Especificações Mínimas para Rodar a Aplicação de Transcrição com Whisper

Este documento apresenta os requisitos mínimos para executar a aplicação de transcrição de áudio/vídeo utilizando o modelo Whisper, tanto em ambientes com GPU quanto apenas com CPU. Também é feita uma comparação entre as duas abordagens, destacando pontos positivos e negativos, além de informações sobre desempenho e eficiência.

---

## 1. Execução em CPU

### Especificações Mínimas:
- **Processador (CPU):** Intel Core i5 (8ª geração ou superior) ou AMD Ryzen 5 equivalente
- **Memória RAM:** 8 GB (16 GB recomendado para arquivos grandes ou uso simultâneo)
- **Sistema Operacional:** Windows 10/11, Ubuntu 18.04+ ou equivalente
- **Armazenamento:** SSD recomendado para melhor desempenho de leitura/gravação
- **Dependências:**
  - Python 3.8+
  - ffmpeg instalado e disponível no PATH
  - Bibliotecas Python: whisper, fastapi, mysql-connector-python, etc.

### Pontos Positivos:
- Não requer hardware dedicado (placa de vídeo)
- Pode ser executado em servidores cloud ou máquinas comuns
- Menor custo de infraestrutura

### Pontos Negativos:
- **Desempenho significativamente inferior**: transcrições podem demorar de minutos a horas, dependendo do tamanho do áudio/vídeo
- Consome mais tempo de CPU, podendo impactar outras aplicações
- Menor escalabilidade para múltiplos usuários simultâneos

---

## 2. Execução em GPU

### Especificações Mínimas:
- **Placa de Vídeo (GPU):** NVIDIA GTX 1060 (6GB) ou superior, com suporte a CUDA
- **Memória VRAM:** 4 GB (8 GB recomendado para modelos maiores ou arquivos longos)
- **Drivers:**
  - Driver NVIDIA atualizado
  - CUDA Toolkit (versão compatível com PyTorch)
  - cuDNN instalado
- **Processador (CPU):** Intel Core i5 ou AMD Ryzen 5 (ou superior)
- **Memória RAM:** 8 GB (16 GB recomendado)
- **Sistema Operacional:** Windows 10/11, Ubuntu 18.04+ ou equivalente
- **Armazenamento:** SSD recomendado
- **Dependências:**
  - Python 3.8+
  - ffmpeg instalado
  - PyTorch instalado com suporte a CUDA
  - whisper, fastapi, mysql-connector-python, etc.

### Pontos Positivos:
- **Desempenho muito superior**: transcrições até 10x-30x mais rápidas que em CPU
- Permite processar arquivos grandes e múltiplos usuários simultaneamente
- Mais eficiente em termos de consumo energético para tarefas intensivas

### Pontos Negativos:
- Requer hardware dedicado (placa NVIDIA compatível)
- Custo de aquisição e manutenção mais alto
- Configuração de drivers/CUDA pode ser complexa para iniciantes

---

## 3. Comparação Direta: CPU vs GPU

| Critério           | CPU                                 | GPU (NVIDIA CUDA)                  |
|--------------------|-------------------------------------|------------------------------------|
| Velocidade         | Lenta (minutos a horas)             | Muito rápida (segundos a minutos)  |
| Eficiência         | Baixa para grandes volumes          | Alta para grandes volumes          |
| Custo              | Baixo                              | Alto (hardware dedicado)           |
| Facilidade de uso  | Simples                            | Requer configuração de drivers     |
| Escalabilidade     | Limitada                            | Alta                               |
| Consumo energético | Alto para tarefas longas            | Menor para tarefas intensivas      |

**Conclusão:**
- Para uso profissional, grande volume de dados ou múltiplos usuários, a GPU é indispensável pela velocidade e eficiência.
- Para testes, uso pessoal ou pequenos volumes, a CPU pode ser suficiente, mas será muito mais lenta.

---

**Observação:**
- GPUs AMD atualmente não são suportadas pelo Whisper via PyTorch/CUDA.
- Sempre prefira SSD para armazenamento temporário de arquivos.
