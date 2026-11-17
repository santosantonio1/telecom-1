# Grupo 02 — Enlace SDR com o ADALM-PLUTO

O Grupo 02 **transmite em 920 MHz** e **recebe em 904 MHz**. O Grupo 01 faz o inverso, então os dois enlaces funcionam ao mesmo tempo sem interferência. As duas frequências ficam em faixas de radiação restrita da Anatel (Ato nº 14.448/2017).

## Arquivos

| Arquivo | Para que serve |
|---|---|
| `grupo02_pluto.grc` | Fluxograma para o GNU Radio Companion, com o Pluto (TX e RX ao mesmo tempo) |
| `grupo02_teste.grc` | Versão de teste, sem rádio: o TX passa por um canal simulado (ruído, desvio de frequência e de relógio) e volta para o RX |
| `grupo02.py` | Script para o terminal: confere o Pluto, compila o `.grc` e roda o fluxograma |
| `LEIA-ME.md` | Este arquivo |

## Parâmetros de projeto

| Parâmetro | Valor |
|---|---|
| Frequência TX / RX | 920 MHz / 904 MHz |
| Taxa de amostragem | 1 MS/s |
| Modulação | QPSK diferencial (DQPSK), filtro RRC com roll-off 0,35 |
| Amostras por símbolo | 8 → 125 ksímbolos/s → 250 kbit/s |
| Banda ocupada | 125 k × (1 + 0,35) ≈ 169 kHz |
| Quadro | código de acesso de 64 bits + comprimento 2×16 bits + payload de 56 bytes = 544 bits |
| Payload | sequência (4 bytes) + texto (48 bytes) + CRC32 (4 bytes), branqueado |
| Taxa de quadros | 250 000 / 544 ≈ **460 quadros/s** |
| Atenuação TX | 10 dB (ajustável na janela, de 0 a 60 dB) |
| Ganho RX | AGC do Pluto (`slow_attack`) |

## Cadeias de transmissão e recepção

```
TX:  Quadros TX → Modulador de constelação (DQPSK, RRC) → ×0,125 → Pluto Sink (920 MHz)

RX:  Pluto Source (904 MHz) → AGC → FLL band-edge → Sincronismo de símbolo (PFB)
     → Costas (ordem 4) → Decisor → Decodificador diferencial → Mapa → Desempacota bits
     → Correlaciona código de acesso → Empacota bytes → PDU → Quadros RX (CRC, perdas, mensagem)
```

Gráficos:
- **Espectro**: sinal recebido (azul) e transmitido (vermelho).
- **Constelação**: saída do Costas.
- **Diagrama de olho**: I e Q depois do filtro casado.

O bloco **Quadros RX** imprime no console, a cada segundo:

```
[RX]   460 quadros/s | recebidos 4131 | perdidos 0 (0.00 %) | CRC ruim 0 | msg: "Grupo 01 -> Grupo 02: ..."
```

Um quadro perdido é um salto no número de sequência. Taxa de perda = perdidos / (recebidos + perdidos).

## Passo a passo

Requisito: GNU Radio 3.10 com o gr-iio (os blocos do Pluto).

### 1. Teste sem o rádio (faça antes do laboratório)

```
python3 grupo02.py --teste
```

Ou abra `grupo02_teste.grc` no GNU Radio Companion e clique em ▶. O esperado é cerca de 460 quadros/s com 0 perdidos. Os controles da janela mudam o ruído e o desvio de frequência.

### 2. Com o Pluto

1. Ligue o Pluto na porta micro-USB do **meio** (a porta de dados). Espere uns 30 s, até o LED1 piscar.
2. Confira se o computador vê o Pluto: `iio_info -s`
3. Rode o script:
   ```
   python3 grupo02.py
   python3 grupo02.py -m "nossa mensagem"          # outro texto (até 48 bytes)
   python3 grupo02.py --uri ip:192.168.2.1          # escolhe o Pluto, se houver mais de um
   ```
   Também dá para abrir `grupo02_pluto.grc` no GNU Radio Companion e clicar em ▶.
4. Combine com o Grupo 01 para os dois rodarem ao mesmo tempo. Cada grupo deve ver no console as mensagens do outro.
5. Se houver perdas, ajuste a **Atenuação TX**: menos atenuação se o sinal estiver fraco, mais se estiver saturando (a constelação fica espalhada).

Sem o Pluto conectado, o script mostra o erro e uma lista do que verificar.

## O que capturar para o relatório (nos dois sentidos)

- Espectro, constelação e diagrama de olho (captura de tela da janela).
- Mensagens recebidas e taxa de quadros perdidos (captura do console).
