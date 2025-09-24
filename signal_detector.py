import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal

try:
    fs_defeito, assinatura_defeito = wavfile.read('assinatura_defeito.wav')
    fs_operacao, operacao_completa = wavfile.read('operacao_completa.wav')

    if assinatura_defeito.ndim > 1: assinatura_defeito = assinatura_defeito[:, 0]
    if operacao_completa.ndim > 1: operacao_completa = operacao_completa[:, 0]
    assinatura_defeito = assinatura_defeito / np.max(np.abs(assinatura_defeito))
    operacao_completa = operacao_completa / np.max(np.abs(operacao_completa))
    print("Sinais em tempo discreto carregados com sucesso.")

except FileNotFoundError:
    print("ERRO: Arquivos 'assinatura_defeito.wav' e 'operacao_completa.wav' não encontrados!")
    exit()

correlacao = signal.correlate(operacao_completa, assinatura_defeito, mode='same')

tempo = np.arange(len(operacao_completa)) / fs_operacao
indice_pico = np.argmax(np.abs(correlacao))
tempo_defeito_detectado = tempo[indice_pico]

print(f"\nPico de correlação (máxima SNR na saída) detectado em: {tempo_defeito_detectado:.2f} segundos.")

fig, axs = plt.subplots(3, 1, figsize=(15, 10), sharex=True)
plt.style.use('seaborn-v0_8-darkgrid')

axs[0].plot(tempo, operacao_completa, color='blue')
axs[0].set_title("Sinal de Entrada do Sistema: x[n]", fontsize=14)
axs[0].set_ylabel("Amplitude")

ax2 = axs[1]
tempo_defeito = np.arange(len(assinatura_defeito)) / fs_defeito
ax2.plot(tempo_defeito, assinatura_defeito, color='green')
ax2.set_title("Sinal a ser Detectado (Molde): s[n]", fontsize=14)
ax2.set_ylabel("Amplitude")

axs[2].plot(tempo, correlacao, color='red')
axs[2].set_title("Sinal de Saída do Filtro Casado: y[n]", fontsize=14)
axs[2].set_xlabel("Tempo (s)", fontsize=12)
axs[2].set_ylabel("Amplitude da Correlação")
axs[2].axvline(x=tempo_defeito_detectado, color='black', linestyle='--', linewidth=2, label=f'Detecção em t={tempo_defeito_detectado:.2f}s')
axs[2].legend(fontsize=12)

plt.tight_layout()
plt.show()
