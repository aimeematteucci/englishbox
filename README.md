# englishbox — transcrição de áudio

Script simples para transcrever áudios (`.m4a`, `.mp3`, `.wav`, `.ogg`, ...)
usando [faster-whisper](https://github.com/SYSTRAN/faster-whisper). Gera um
`.txt` (texto corrido) e um `.srt` (com marcação de tempo).

## Instalação

```bash
pip install -r requirements.txt
```

O áudio é decodificado pelo próprio faster-whisper (via PyAV), então formatos
como `.m4a` funcionam direto — **não é preciso instalar ffmpeg** no sistema.

## Uso

```bash
# Português (padrão), modelo "small"
python transcribe.py caminho/do/audio.m4a

# Escolher o modelo e o idioma
python transcribe.py audio.m4a --model medium --language pt

# Detecção automática de idioma
python transcribe.py audio.m4a --language auto
```

Saída (ao lado do áudio, por padrão):

- `audio.txt` — texto corrido
- `audio.srt` — legendas com timestamps

### Opções principais

| Opção             | Padrão  | Descrição                                                        |
| ----------------- | ------- | ---------------------------------------------------------------- |
| `--model`         | `small` | `tiny`, `base`, `small`, `medium`, `large-v3` (maior = melhor)   |
| `--language`      | `pt`    | Código do idioma ou `auto` para detectar                         |
| `--device`        | `cpu`   | `cpu` ou `cuda`                                                  |
| `--compute-type`  | `int8`  | `int8`, `float16`, `float32`, ... (`int8` é ideal para CPU)      |
| `--no-vad`        | —       | Desliga o filtro de detecção de voz                              |
| `-o/--output-dir` | —       | Diretório de saída (padrão: ao lado do áudio)                    |

## Acesso de rede (importante no Claude Code na web)

Na **primeira execução** de cada modelo, os pesos são baixados do HuggingFace.
Se estiver rodando no Claude Code na web, o ambiente precisa ter uma política de
rede que permita o acesso a:

- `huggingface.co`
- `*.huggingface.co`
- `cas-bridge.xethub.hf.co`

Sem esse acesso, o download do modelo falha com erro `403 Forbidden` no proxy.
Depois de baixado uma vez, o modelo fica em cache e não precisa mais de rede.
