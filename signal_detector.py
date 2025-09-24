import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal
import os

try:
    matplotlib.use('TkAgg')
except ImportError:
    try:
        matplotlib.use('Qt5Agg')
    except ImportError:
        matplotlib.use('Agg')
        print("Interface gráfica não disponível. Salvando gráficos como arquivos PNG.")

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
    print("Execute primeiro: python generate_test_audio.py")
    exit()

correlacao = signal.correlate(operacao_completa, assinatura_defeito, mode='same')

tempo = np.arange(len(operacao_completa)) / fs_operacao
indice_pico = np.argmax(np.abs(correlacao))
tempo_defeito_detectado = tempo[indice_pico]

print(f"\nPico de correlação (máxima SNR na saída) detectado em: {tempo_defeito_detectado:.2f} segundos.")
fig, axs = plt.subplots(3, 1, figsize=(15, 10))

try:
    plt.style.use('seaborn-v0_8-darkgrid')
except:
    plt.style.use('default')

axs[0].plot(tempo, operacao_completa, color='blue', linewidth=1)
axs[0].set_title("Sinal de Entrada do Sistema: x[n]", fontsize=14, fontweight='bold')
axs[0].set_ylabel("Amplitude")
axs[0].grid(True, alpha=0.3)

tempo_defeito = np.arange(len(assinatura_defeito)) / fs_defeito
axs[1].plot(tempo_defeito, assinatura_defeito, color='green', linewidth=2)
axs[1].set_title("Sinal a ser Detectado (Molde): s[n]", fontsize=14, fontweight='bold')
axs[1].set_ylabel("Amplitude")
axs[1].grid(True, alpha=0.3)

axs[2].plot(tempo, correlacao, color='red', linewidth=1)
axs[2].set_title("Sinal de Saída do Filtro Casado: y[n]", fontsize=14, fontweight='bold')
axs[2].set_xlabel("Tempo (s)", fontsize=12)
axs[2].set_ylabel("Amplitude da Correlação")
axs[2].axvline(x=tempo_defeito_detectado, color='black', linestyle='--', linewidth=2, 
               label=f'Detecção em t={tempo_defeito_detectado:.2f}s')
axs[2].legend(fontsize=12)
axs[2].grid(True, alpha=0.3)

plt.tight_layout()

backend = matplotlib.get_backend()
if backend == 'Agg':
    filename = 'matched_filter_results.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Gráficos salvos em: {os.path.abspath(filename)}")
    print("Abra o arquivo para visualizar os resultados!")
else:
    try:
        plt.show()
        print("Gráficos exibidos na tela!")
    except Exception as e:
        filename = 'matched_filter_results.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Gráficos salvos em: {os.path.abspath(filename)}")
        print(f"Não foi possível exibir na tela: {e}")

print("\n" + "="*50)
print("RESUMO DOS RESULTADOS:")
print("="*50)
print(f"Duração da operação: {len(operacao_completa)/fs_operacao:.1f} segundos")
print(f"Molde do defeito: {len(assinatura_defeito)/fs_defeito:.1f} segundos")
print(f"Defeito detectado em: {tempo_defeito_detectado:.2f}s")
print(f"Valor máximo da correlação: {np.max(np.abs(correlacao)):.4f}")
print("="*50)
