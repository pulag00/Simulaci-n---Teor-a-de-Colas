
# ==============================================================
# CELDA 1 - Importaciones (solo librerías estándar de Colab)
# ==============================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 10,
    'figure.dpi': 150,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

COLORES = ['#2196F3', '#FF5722']

# ==============================================================
# CELDA 2 - Datos embebidos (extraídos del archivo Excel original)
# Formato de cada fila: (usuario, llegada, inicio_servicio, fin_servicio)
# ==============================================================

DATOS_SESION_1 = [
    (1,  '11:41:00', '11:41:00', '11:43:00'),
    (2,  '11:46:00', '11:46:00', '11:48:00'),
    (3,  '11:55:00', '11:55:00', '11:57:00'),
    (4,  '11:56:00', '11:57:00', '12:01:00'),
    (5,  '12:00:00', '12:02:00', '12:06:00'),
    (6,  '12:01:00', '12:07:00', '12:09:00'),
    (7,  '12:03:00', '12:10:00', '12:13:00'),
    (8,  '12:07:00', '12:13:00', '12:15:00'),
    (9,  '12:10:00', '12:16:00', '12:17:00'),
    (10, '12:11:00', '12:17:00', '12:19:00'),
    (11, '12:14:00', '12:19:00', '12:21:00'),
    (12, '12:14:00', '12:22:00', '12:25:00'),
    (13, '12:21:00', '12:25:00', '12:26:00'),
    (14, '12:26:00', '12:27:00', '12:28:00'),
    (15, '12:31:00', '12:31:00', '12:33:00'),
    (16, '12:32:00', '12:33:00', '12:35:00'),
    (17, '12:32:00', '12:36:00', '12:39:00'),
    (18, '12:38:00', '12:39:00', '12:41:00'),
    (19, '12:40:00', '12:41:00', '12:42:00'),
]

DATOS_SESION_2 = [
    (1,  '11:47:00', '11:48:00', '11:50:00'),
    (2,  '11:51:00', '11:51:00', '11:53:00'),
    (3,  '12:00:00', '12:01:00', '12:02:00'),
    (4,  '12:02:00', '12:03:00', '12:05:00'),
    (5,  '12:06:00', '12:06:00', '12:09:00'),
    (6,  '12:07:00', '12:10:00', '12:12:00'),
    (7,  '12:07:00', '12:13:00', '12:16:00'),
    (8,  '12:08:00', '12:16:00', '12:19:00'),
    (9,  '12:12:00', '12:19:00', '12:21:00'),
    (10, '12:15:00', '12:22:00', '12:24:00'),
    (11, '12:19:00', '12:24:00', '12:29:00'),
    (12, '12:25:00', '12:30:00', '12:33:00'),
    (13, '12:33:00', '12:33:00', '12:36:00'),
    (14, '12:34:00', '12:36:00', '12:39:00'),
    (15, '12:34:00', '12:39:00', '12:42:00'),
]

T_OBSERVACION = 62   # minutos (igual para ambas sesiones)
REF_HORA      = '11:40:00'  # hora de inicio de observación

# ==============================================================
# CELDA 3 - Procesamiento de datos
# ==============================================================

def a_minutos(hora_str, ref_str=REF_HORA):
    """Convierte 'HH:MM:SS' a minutos desde la hora de referencia."""
    fmt = '%H:%M:%S'
    return (datetime.strptime(hora_str, fmt) -
            datetime.strptime(ref_str,  fmt)).total_seconds() / 60.0

def construir_df(datos, t_obs):
    registros = []
    for usuario, llegada, inicio, fin in datos:
        t_ll = a_minutos(llegada)
        t_in = a_minutos(inicio)
        t_fi = a_minutos(fin)
        registros.append({
            'usuario': usuario,
            'Wq'    : max(t_in - t_ll, 0),   # espera en cola
            'S'     : max(t_fi - t_in, 0),   # tiempo de servicio
            'W'     : max(t_fi - t_ll, 0),   # tiempo total en sistema
            'T_obs' : t_obs,
        })
    return pd.DataFrame(registros)

s1 = construir_df(DATOS_SESION_1, T_OBSERVACION)
s2 = construir_df(DATOS_SESION_2, T_OBSERVACION)

print("✅ Datos cargados correctamente")
print(f"\nSesión 1 ({len(s1)} usuarios):")
print(s1[['usuario','Wq','S','W']].round(2).to_string(index=False))
print(f"\nSesión 2 ({len(s2)} usuarios):")
print(s2[['usuario','Wq','S','W']].round(2).to_string(index=False))

# ==============================================================
# CELDA 4 - Cálculo de indicadores M/M/1
# ==============================================================

def calcular_indicadores(df):
    N   = len(df)
    T   = df['T_obs'].iloc[0]
    lam = N / T
    S_p = df['S'].mean()
    mu  = 1.0 / S_p
    rho = lam / mu
    P0      = 1 - rho
    Lq      = (lam**2) / (mu * (mu - lam))
    L       = lam / (mu - lam)
    Wq_teo  = lam / (mu * (mu - lam))
    W_teo   = 1.0 / (mu - lam)
    return dict(N=N, T_obs=T, S_prom=S_p,
                Wq_obs=df['Wq'].mean(), W_obs=df['W'].mean(),
                lam=lam, mu=mu, rho=rho, P0=P0,
                Lq=Lq, L=L, Wq_teo=Wq_teo, W_teo=W_teo)

ind1 = calcular_indicadores(s1)
ind2 = calcular_indicadores(s2)

# ==============================================================
# CELDA 5 - Tabla resumen impresa
# ==============================================================

filas_tabla = [
    ('N usuarios observados',                ind1['N'],      ind2['N']),
    ('Tiempo de observación (min)',          ind1['T_obs'],  ind2['T_obs']),
    ('S promedio — tiempo de servicio (min)',ind1['S_prom'], ind2['S_prom']),
    ('Wq observado — espera en cola (min)', ind1['Wq_obs'], ind2['Wq_obs']),
    ('W observado — tiempo total (min)',     ind1['W_obs'],  ind2['W_obs']),
    ('λ — tasa de llegada (usu/min)',        ind1['lam'],    ind2['lam']),
    ('μ — tasa de servicio (usu/min)',       ind1['mu'],     ind2['mu']),
    ('ρ — factor de utilización',           ind1['rho'],    ind2['rho']),
    ('P₀ — prob. sistema vacío',            ind1['P0'],     ind2['P0']),
    ('Lq — usuarios promedio en cola',      ind1['Lq'],     ind2['Lq']),
    ('L  — usuarios promedio en sistema',   ind1['L'],      ind2['L']),
    ('Wq teórico — espera en cola (min)',   ind1['Wq_teo'], ind2['Wq_teo']),
    ('W  teórico — tiempo total (min)',     ind1['W_teo'],  ind2['W_teo']),
]

print("\n" + "="*68)
print("   TABLA DE INDICADORES M/M/1 — ZONA DE MICROONDAS")
print("="*68)
print(f"{'Indicador':<44} {'Sesión 1':>10} {'Sesión 2':>10}")
print("-"*68)
for label, v1, v2 in filas_tabla:
    f1 = f"{v1:.4f}" if isinstance(v1, float) else str(int(v1))
    f2 = f"{v2:.4f}" if isinstance(v2, float) else str(int(v2))
    print(f"{label:<44} {f1:>10} {f2:>10}")
print("="*68)

# ==============================================================
# CELDA 6 - Gráfica 1: Tiempo de espera por usuario
# ==============================================================

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle('Tiempo de Espera en Cola por Usuario\n(Sistema M/M/1 — Microondas Universitario)',
             fontsize=14, fontweight='bold', y=1.02)

for ax, df, ind, color, titulo in zip(
        axes, [s1, s2], [ind1, ind2], COLORES,
        ['Sesión 1 — 23 de Abril', 'Sesión 2 — 24 de Abril']):
    bars = ax.bar(df['usuario'], df['Wq'], color=color, alpha=0.82, edgecolor='white')
    ax.axhline(ind['Wq_obs'], color='black',  linestyle='--', linewidth=1.5,
               label=f"Promedio obs. = {ind['Wq_obs']:.2f} min")
    ax.axhline(ind['Wq_teo'], color='crimson', linestyle=':', linewidth=1.5,
               label=f"Wq teórico = {ind['Wq_teo']:.2f} min")
    for bar in bars:
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.1, f'{h:.0f}',
                    ha='center', va='bottom', fontsize=7.5)
    ax.set_title(titulo, fontsize=12)
    ax.set_xlabel('Usuario (orden de llegada)')
    ax.set_ylabel('Tiempo de espera (min)')
    ax.set_xticks(df['usuario'])
    ax.legend(loc='upper left', fontsize=9)
    ax.set_ylim(bottom=0)

plt.tight_layout()
plt.savefig('espera_por_usuario.png', bbox_inches='tight', dpi=150)
plt.show()
print("✅ espera_por_usuario.png")

# ==============================================================
# CELDA 7 - Gráfica 2: Tiempo de servicio por usuario
# ==============================================================

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle('Tiempo de Servicio por Usuario\n(Sistema M/M/1 — Microondas Universitario)',
             fontsize=14, fontweight='bold', y=1.02)

for ax, df, ind, color, titulo in zip(
        axes, [s1, s2], [ind1, ind2], COLORES,
        ['Sesión 1 — 23 de Abril', 'Sesión 2 — 24 de Abril']):
    bars = ax.bar(df['usuario'], df['S'], color=color, alpha=0.82, edgecolor='white')
    ax.axhline(ind['S_prom'], color='black', linestyle='--', linewidth=1.5,
               label=f"Promedio = {ind['S_prom']:.2f} min  |  μ = {ind['mu']:.4f} usu/min")
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.05, f'{h:.0f}',
                ha='center', va='bottom', fontsize=7.5)
    ax.set_title(titulo, fontsize=12)
    ax.set_xlabel('Usuario (orden de llegada)')
    ax.set_ylabel('Tiempo de servicio (min)')
    ax.set_xticks(df['usuario'])
    ax.legend(loc='upper right', fontsize=9)
    ax.set_ylim(bottom=0)

plt.tight_layout()
plt.savefig('servicio_por_usuario.png', bbox_inches='tight', dpi=150)
plt.show()
print("✅ servicio_por_usuario.png")

# ==============================================================
# CELDA 8 - Gráfica 3: Comparación de promedios
# ==============================================================

categorias = ['Espera en cola\n(Wq obs.)', 'Tiempo de servicio\n(S prom.)', 'Tiempo total\n(W obs.)']
vals1 = [ind1['Wq_obs'], ind1['S_prom'], ind1['W_obs']]
vals2 = [ind2['Wq_obs'], ind2['S_prom'], ind2['W_obs']]

x, ancho = np.arange(len(categorias)), 0.35
fig, ax = plt.subplots(figsize=(9, 6))
b1 = ax.bar(x - ancho/2, vals1, ancho, label='Sesión 1 (23 Abr)', color=COLORES[0], alpha=0.85)
b2 = ax.bar(x + ancho/2, vals2, ancho, label='Sesión 2 (24 Abr)', color=COLORES[1], alpha=0.85)

for bar in list(b1) + list(b2):
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h + 0.05, f'{h:.2f}',
            ha='center', va='bottom', fontsize=9, fontweight='bold')

ax.set_title('Comparación de Tiempos Promedio entre Sesiones\n(Sistema M/M/1 — Microondas Universitario)',
             fontsize=13, fontweight='bold')
ax.set_ylabel('Tiempo (minutos)')
ax.set_xticks(x)
ax.set_xticklabels(categorias)
ax.set_ylim(bottom=0, top=max(max(vals1), max(vals2)) * 1.25)
ax.legend()

plt.tight_layout()
plt.savefig('comparacion_promedios.png', bbox_inches='tight', dpi=150)
plt.show()
print("✅ comparacion_promedios.png")

# ==============================================================
# CELDA 9 - Gráfica 4: Utilización del sistema (ρ)
# ==============================================================

fig, ax = plt.subplots(figsize=(7, 5))
sesiones = ['Sesión 1\n(23 Abr)', 'Sesión 2\n(24 Abr)']
rhos = [ind1['rho'], ind2['rho']]

bars = ax.bar(sesiones, rhos, color=COLORES, alpha=0.85, width=0.45)
ax.axhline(1.0, color='red',    linestyle='--', linewidth=1.5, label='Límite de saturación (ρ = 1)')
ax.axhline(0.8, color='orange', linestyle=':',  linewidth=1.2, label='Umbral de alta carga (ρ = 0.8)')

for bar, rho in zip(bars, rhos):
    ax.text(bar.get_x() + bar.get_width()/2, rho + 0.01,
            f'ρ = {rho:.4f}\n({rho*100:.1f}%)',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_title('Factor de Utilización del Sistema (ρ)\nM/M/1 — Microondas Universitario',
             fontsize=13, fontweight='bold')
ax.set_ylabel('Utilización  ρ = λ / μ')
ax.set_ylim(0, 1.3)
ax.legend()

plt.tight_layout()
plt.savefig('utilizacion_sistema.png', bbox_inches='tight', dpi=150)
plt.show()
print("✅ utilizacion_sistema.png")

# ==============================================================
# CELDA 10 - Gráfica 5: Indicadores M/M/1 teóricos
# ==============================================================

indicadores = ['Lq\n(usuarios en cola)', 'L\n(usuarios en sistema)',
               'Wq teórico\n(min en cola)', 'W teórico\n(min en sistema)']
vals_s1 = [ind1['Lq'], ind1['L'], ind1['Wq_teo'], ind1['W_teo']]
vals_s2 = [ind2['Lq'], ind2['L'], ind2['Wq_teo'], ind2['W_teo']]

x, ancho = np.arange(len(indicadores)), 0.35
fig, ax = plt.subplots(figsize=(11, 6))
b1 = ax.bar(x - ancho/2, vals_s1, ancho, label='Sesión 1 (23 Abr)', color=COLORES[0], alpha=0.85)
b2 = ax.bar(x + ancho/2, vals_s2, ancho, label='Sesión 2 (24 Abr)', color=COLORES[1], alpha=0.85)

for bar in list(b1) + list(b2):
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h + 0.02, f'{h:.3f}',
            ha='center', va='bottom', fontsize=9, fontweight='bold')

ax.set_title('Indicadores del Modelo M/M/1 por Sesión\nMicroondas Universitario',
             fontsize=13, fontweight='bold')
ax.set_ylabel('Valor del indicador')
ax.set_xticks(x)
ax.set_xticklabels(indicadores)
ax.set_ylim(bottom=0, top=max(max(vals_s1), max(vals_s2)) * 1.3)
ax.legend()

plt.tight_layout()
plt.savefig('indicadores_mm1.png', bbox_inches='tight', dpi=150)
plt.show()
print("✅ indicadores_mm1.png")

print("\n✅ Análisis M/M/1 completado. Todos los PNG exportados.")
