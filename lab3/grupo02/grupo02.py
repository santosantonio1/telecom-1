#!/usr/bin/env python3
"""Grupo 02 - enlace SDR com o ADALM-PLUTO, pelo terminal.

  python3 grupo02.py                      # com o Pluto (TX 920 MHz / RX 904 MHz)
  python3 grupo02.py --teste              # sem radio (loopback simulado)
  python3 grupo02.py --uri ip:192.168.2.1 --mensagem "outro texto"

Confere se o Pluto esta acessivel, compila o .grc (se preciso) e roda o fluxograma.
"""
import argparse
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))

VERIFIQUE = """
ERRO: Pluto nao encontrado.
Motivo: {motivo}

Verifique:
  1. O cabo USB esta na porta micro-USB do MEIO do Pluto (dados), nao na porta 'PWR'.
  2. O LED de energia esta aceso e o LED1 pisca (o Pluto terminou de iniciar; espere ~30 s).
  3. O computador ve o Pluto:  iio_info -s   (ou  ping 192.168.2.1)
  4. Nenhum outro programa (outro GNU Radio, SDR++, etc.) esta usando o Pluto.
  5. Com mais de um Pluto ligado, escolha um:  python3 grupo02.py --uri usb:1.2.5
  6. Para testar sem o radio:  python3 grupo02.py --teste
"""


def acha_pluto(uri):
    """Retorna a URI do Pluto ou encerra com uma mensagem clara do que verificar."""
    try:
        if not uri:
            from gnuradio import iio
            uri = iio.get_pluto_uri()  # erro se nenhum (ou mais de um) Pluto
        r = subprocess.run(['iio_info', '-u', uri], capture_output=True, text=True, timeout=20)
        if r.returncode != 0 or 'PlutoSDR' not in r.stdout:
            raise RuntimeError(f'nao foi possivel abrir "{uri}": {(r.stderr or r.stdout).strip()[-200:]}')
    except FileNotFoundError:
        print('Aviso: iio_info nao instalado; pulando a verificacao do Pluto.', file=sys.stderr)
    except Exception as e:
        sys.exit(VERIFIQUE.format(motivo=e))
    return uri


def main():
    ap = argparse.ArgumentParser(description='Grupo 02 - enlace SDR (TX 920 MHz / RX 904 MHz)')
    ap.add_argument('--teste', action='store_true', help='roda sem o radio (loopback com ruido e desvio simulados)')
    ap.add_argument('-u', '--uri', default='', help='URI do Pluto (ex.: usb:1.2.5, ip:192.168.2.1); vazio = detectar')
    ap.add_argument('-m', '--mensagem', default='Grupo 02 -> Grupo 01: ola do Pluto!', help='texto enviado (ate 48 bytes)')
    a = ap.parse_args()

    modo = 'teste' if a.teste else 'pluto'
    extra = [] if a.teste else ['--uri', acha_pluto(a.uri)]

    grc = os.path.join(AQUI, f'grupo02_{modo}.grc')
    py = grc[:-4] + '.py'
    if not os.path.exists(py) or os.path.getmtime(py) < os.path.getmtime(grc):
        r = subprocess.run(['grcc', '-o', AQUI, grc], capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit(f'ERRO ao compilar {grc}:\n{r.stdout}\n{r.stderr}')

    print(f'Rodando {os.path.basename(py)} (Ctrl+C ou feche a janela para parar)...', flush=True)
    os.execv(sys.executable, [sys.executable, '-u', py, '--mensagem', a.mensagem] + extra)


if __name__ == '__main__':
    main()
