#!/usr/bin/env python3
"""Transcreve arquivos de áudio (m4a, mp3, wav, ogg, ...) usando faster-whisper.

Uso básico:
    python transcribe.py caminho/do/audio.m4a

Exemplos:
    # Português (padrão), modelo "small", salvando .txt e .srt ao lado do áudio
    python transcribe.py audio.m4a

    # Escolher modelo e idioma explicitamente
    python transcribe.py audio.m4a --model medium --language pt

    # Deixar o idioma ser detectado automaticamente
    python transcribe.py audio.m4a --language auto

O áudio é decodificado pelo próprio faster-whisper (via PyAV), então formatos
como .m4a funcionam direto, sem precisar de ffmpeg instalado no sistema.

Requisitos: veja requirements.txt (pip install -r requirements.txt).
Observação: na primeira execução o modelo é baixado do HuggingFace, então o
ambiente precisa ter acesso de rede a huggingface.co.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def format_timestamp(seconds: float) -> str:
    """Formata segundos como HH:MM:SS,mmm (padrão SRT)."""
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Transcreve áudio com faster-whisper.")
    p.add_argument("audio", help="Caminho do arquivo de áudio a transcrever.")
    p.add_argument(
        "--model",
        default="small",
        help="Tamanho do modelo Whisper: tiny, base, small, medium, large-v3. "
        "Maior = mais preciso e mais lento (padrão: small).",
    )
    p.add_argument(
        "--language",
        default="pt",
        help="Código do idioma (ex.: pt, en, es) ou 'auto' para detectar (padrão: pt).",
    )
    p.add_argument(
        "--device",
        default="cpu",
        help="cpu ou cuda (padrão: cpu).",
    )
    p.add_argument(
        "--compute-type",
        default="int8",
        help="Tipo de cálculo do CTranslate2, ex.: int8, int8_float16, float16, "
        "float32 (padrão: int8, ideal para CPU).",
    )
    p.add_argument(
        "--no-vad",
        action="store_true",
        help="Desliga o filtro de detecção de voz (VAD).",
    )
    p.add_argument(
        "-o",
        "--output-dir",
        default=None,
        help="Diretório de saída dos arquivos .txt/.srt (padrão: ao lado do áudio).",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    audio_path = Path(args.audio).expanduser()
    if not audio_path.is_file():
        print(f"Erro: arquivo não encontrado: {audio_path}", file=sys.stderr)
        return 1

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print(
            "Erro: faster-whisper não está instalado.\n"
            "Instale com: pip install -r requirements.txt",
            file=sys.stderr,
        )
        return 1

    out_dir = Path(args.output_dir).expanduser() if args.output_dir else audio_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = audio_path.stem
    txt_path = out_dir / f"{stem}.txt"
    srt_path = out_dir / f"{stem}.srt"

    language = None if args.language.lower() == "auto" else args.language

    print(
        f"Carregando modelo '{args.model}' ({args.device}/{args.compute_type})... "
        "(baixado do HuggingFace na primeira vez)",
        file=sys.stderr,
    )
    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)

    print(f"Transcrevendo: {audio_path.name}", file=sys.stderr)
    segments, info = model.transcribe(
        str(audio_path),
        language=language,
        vad_filter=not args.no_vad,
    )
    print(
        f"Idioma: {info.language} (prob. {info.language_probability:.2f}) | "
        f"duração: {info.duration:.1f}s",
        file=sys.stderr,
    )

    plain_lines: list[str] = []
    with srt_path.open("w", encoding="utf-8") as srt_f:
        for i, seg in enumerate(segments, start=1):
            text = seg.text.strip()
            # Mostra o progresso na tela enquanto processa.
            print(f"[{format_timestamp(seg.start)} -> {format_timestamp(seg.end)}] {text}")
            srt_f.write(
                f"{i}\n"
                f"{format_timestamp(seg.start)} --> {format_timestamp(seg.end)}\n"
                f"{text}\n\n"
            )
            plain_lines.append(text)

    txt_path.write_text(" ".join(plain_lines).strip() + "\n", encoding="utf-8")

    print(f"\nSalvo:\n  {txt_path}\n  {srt_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
