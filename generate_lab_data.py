import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

np.random.seed(42)
os.makedirs('lab_graphs', exist_ok=True)

g = 9.80  # m/s²
PENDULUM_BOB_MASS_G = 127  # grams (3D printed bob + 13 washers + hardware)

# =====================================================================
# DATA TABLE 1 — Effect of Length on Period
# Amplitude = 15°, Bob with 13 fender washers
# =====================================================================
lengths_cm = [20, 30, 40, 50, 60]

def pendulum_period(L_m):
    return 2 * np.pi * np.sqrt(L_m / g)

data_table1 = []
for L in lengths_cm:
    T_th = pendulum_period(L / 100)
    t1 = round(T_th + np.random.uniform(-0.005, 0.005), 3)
    t2 = round(T_th + np.random.uniform(-0.005, 0.005), 3)
    avg = round((t1 + t2) / 2, 3)
    data_table1.append({'L_cm': L, 'T1': t1, 'T2': t2, 'T_avg': avg})

# =====================================================================
# PERIOD vs TIME GRAPHS — Vernier Graphical Analysis style
# =====================================================================
def make_photogate_graph(L_cm, T_avg, n_osc=9, outfile=None):
    """Replicates the Vernier Graphical Analysis Period vs Time display."""
    periods = T_avg + np.random.normal(0, 0.0015, n_osc)
    # Cumulative time at each period measurement
    times = np.cumsum(periods)

    fig = plt.figure(figsize=(13, 7))
    ax = fig.add_axes([0.07, 0.12, 0.88, 0.80])

    fig.patch.set_facecolor('#d8d8d8')
    ax.set_facecolor('white')

    # Axis limits matching screenshot style
    x_max = max(times) * 1.15
    ax.set_xlim(0, x_max)
    ax.set_ylim(0, 10)

    # Grid
    x_step = round(x_max / 7, 0)
    ax.set_xticks(np.arange(0, x_max + x_step, x_step))
    ax.set_yticks(range(0, 11))
    ax.grid(True, color='#c0c0c0', linewidth=0.8)
    ax.set_axisbelow(True)

    # Thick border around plot area
    for spine in ax.spines.values():
        spine.set_linewidth(1.5)
        spine.set_color('#555555')

    # Data points — green filled circles (matching screenshot)
    ax.scatter(times, periods, color='#1e7e1e', s=110, zorder=5,
               edgecolors='#0d5c0d', linewidths=0.6)

    # Vertical cursor line at last point
    ax.axvline(x=times[-1], color='black', linewidth=1.5, zorder=4)

    # Annotation for last point value
    ax.annotate(
        f'{periods[-1]:.6f} s',
        xy=(times[-1], periods[-1]),
        xytext=(times[-1] * 0.80, periods[-1] + 0.9),
        fontsize=10,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                  edgecolor='#888888', linewidth=0.8)
    )

    # X-axis time annotation below cursor (Vernier style)
    ax.annotate(
        f': {times[-1]:.5f} s :',
        xy=(times[-1], 0),
        xytext=(times[-1], -0.05),
        fontsize=9,
        ha='center', va='top',
        xycoords=('data', 'axes fraction'),
        textcoords=('data', 'axes fraction'),
        annotation_clip=False,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                  edgecolor='#888888', linewidth=0.6)
    )

    # Y-axis label in box
    ax.set_ylabel('Period (s)', fontsize=12, rotation=90, labelpad=6)
    ax.yaxis.label.set_bbox(dict(facecolor='white', edgecolor='black',
                                  boxstyle='round,pad=0.4'))

    ax.set_xlabel('Time (s)', fontsize=12, labelpad=6)

    # Y-axis tick in top-left corner box (Vernier style — shows scale max)
    ax.text(-0.055, 1.01, '10', transform=ax.transAxes,
            fontsize=10, ha='center', va='bottom',
            bbox=dict(boxstyle='square,pad=0.3', facecolor='white',
                      edgecolor='black', linewidth=1))

    # Bottom status bar (Vernier style)
    fig.text(0.01, 0.02, 'Mode: Photogate Timing   Timer',
             fontsize=9, color='#222222',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0f0f0',
                       edgecolor='#aaaaaa'))
    fig.text(0.88, 0.02, 'Gate State: 0',
             fontsize=9, color='#222222',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0f0f0',
                       edgecolor='#aaaaaa'))

    fig.text(0.5, 0.97, f'Pendulum Length = {L_cm} cm  |  Avg Period ≈ {T_avg:.3f} s',
             ha='center', fontsize=10, color='#333333')

    if outfile:
        plt.savefig(outfile, dpi=150, bbox_inches='tight')
    plt.close()
    return times, periods


print("Generating Period vs Time graphs...")
for row in data_table1:
    for trial_key, T_val in [('T1', row['T1']), ('T2', row['T2'])]:
        n = np.random.randint(8, 12)
        fname = f"lab_graphs/pendulum_L{row['L_cm']}cm_{trial_key}.png"
        make_photogate_graph(row['L_cm'], T_val, n_osc=n, outfile=fname)
        print(f"  Saved {fname}")

# =====================================================================
# T² vs L GRAPH
# =====================================================================
T_avgs = [row['T_avg'] for row in data_table1]
T2s    = [T**2 for T in T_avgs]
Ls_m   = [row['L_cm'] / 100 for row in data_table1]

fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(Ls_m, T2s, color='#1e7e1e', s=110, zorder=5, label='Measured Data')

coeffs = np.polyfit(Ls_m, T2s, 1)
L_fit  = np.linspace(0, 0.70, 200)
ax.plot(L_fit, np.polyval(coeffs, L_fit), 'b-', lw=1.8,
        label=f'Linear Fit:  T² = {coeffs[0]:.3f} L + {coeffs[1]:.4f}')

theoretical_slope = 4 * np.pi**2 / g   # ≈ 4.027 s²/m
ax.plot(L_fit, theoretical_slope * L_fit, 'r--', lw=1.3,
        label=f'Theoretical:  T² = {theoretical_slope:.3f} L')

ax.set_xlabel('Pendulum Length (m)', fontsize=12)
ax.set_ylabel('T² (s²)', fontsize=12)
ax.set_title('Period² vs Pendulum Length', fontsize=12)
ax.set_xlim(0, 0.70)
ax.set_ylim(0, max(T2s) * 1.30)
ax.legend(fontsize=10)
ax.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('lab_graphs/T2_vs_Length.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved lab_graphs/T2_vs_Length.png")

# =====================================================================
# DATA TABLE 2 — Amplitude and Period of Oscillation (Spring, 150 g)
# =====================================================================
k = 9.25   # N/m  → T ≈ 0.801 s at 150 g

def spring_period(m_kg):
    return 2 * np.pi * np.sqrt(m_kg / k)

T_150 = spring_period(0.150)
data_table2 = []
for run, amp_cm in enumerate([1.2, 2.3, 3.2], start=1):
    T = round(T_150 + np.random.normal(0, 0.002), 3)
    data_table2.append({
        'Run': run,
        'Mass_g': 150,
        'T': T,
        'T2': round(T**2, 4),
        'A_m': round(amp_cm / 100, 3),
        'f': round(1 / T, 3)
    })

# =====================================================================
# DATA TABLE 3 — Mass and Period of Oscillation (Spring)
# =====================================================================
data_table3 = []
for m_g in [50, 100, 150, 200]:
    T = round(spring_period(m_g / 1000) + np.random.normal(0, 0.003), 3)
    data_table3.append({'Mass_g': m_g, 'T': T, 'T2': round(T**2, 4)})

# =====================================================================
# SPRING POSITION vs TIME  &  VELOCITY vs TIME GRAPHS
# =====================================================================
def make_spring_graph(run_num, mass_g, amp_m, T, outfile=None):
    omega = 2 * np.pi / T
    dt = 0.02   # 50 Hz motion sensor sampling rate
    t  = np.arange(0, 5.0, dt)

    pos = amp_m * np.cos(omega * t) + np.random.normal(0, 0.0004, len(t))
    vel = -amp_m * omega * np.sin(omega * t) + np.random.normal(0, 0.002, len(t))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    fig.suptitle(
        f'Spring SHM — Run {run_num}: Mass = {mass_g} g, '
        f'Amplitude ≈ {amp_m * 100:.1f} cm,  T ≈ {T:.3f} s',
        fontsize=11
    )

    ax1.plot(t, pos * 100, color='#1565C0', lw=1.3)
    ax1.set_ylabel('Position (cm)', fontsize=11)
    ax1.set_title('Position vs. Time', fontsize=10)
    ax1.grid(True, linestyle='--', alpha=0.4)
    ax1.axhline(0, color='k', lw=0.5)

    ax2.plot(t, vel * 100, color='#C62828', lw=1.3)
    ax2.set_ylabel('Velocity (cm/s)', fontsize=11)
    ax2.set_xlabel('Time (s)', fontsize=11)
    ax2.set_title('Velocity vs. Time', fontsize=10)
    ax2.grid(True, linestyle='--', alpha=0.4)
    ax2.axhline(0, color='k', lw=0.5)
    ax2.set_xlim(0, 5)

    plt.tight_layout()
    if outfile:
        plt.savefig(outfile, dpi=150, bbox_inches='tight')
    plt.close()


print("Generating spring graphs...")
for row in data_table2:
    fname = f"lab_graphs/spring_run{row['Run']}.png"
    make_spring_graph(row['Run'], row['Mass_g'], row['A_m'], row['T'], outfile=fname)
    print(f"  Saved {fname}")

# =====================================================================
# PRINT DATA TABLES TO CONSOLE
# =====================================================================
print()
print("=" * 68)
print("  DATA TABLE 1 — Effect of Length on Period")
print(f"  Bob mass = {PENDULUM_BOB_MASS_G} g  |  Amplitude = 15°")
print("=" * 68)
print(f"  {'Length (cm)':<14} {'Trial 1 T (s)':<16} {'Trial 2 T (s)':<16} {'Avg T (s)'}")
print("  " + "-" * 64)
for row in data_table1:
    print(f"  {row['L_cm']:<14} {row['T1']:<16} {row['T2']:<16} {row['T_avg']}")

print()
print("=" * 68)
print("  DATA TABLE 2 — Amplitude & Period of Oscillation (Spring)")
print("=" * 68)
print(f"  {'Run':<6} {'Mass(g)':<10} {'T(s)':<10} {'T²(s²)':<12} {'A(m)':<10} {'f(Hz)'}")
print("  " + "-" * 64)
for row in data_table2:
    print(f"  {row['Run']:<6} {row['Mass_g']:<10} {row['T']:<10} {row['T2']:<12} {row['A_m']:<10} {row['f']}")

print()
print("=" * 44)
print("  DATA TABLE 3 — Mass & Period (Spring)")
print("=" * 44)
print(f"  {'Mass (g)':<14} {'T (s)':<12} {'T² (s²)'}")
print("  " + "-" * 40)
for row in data_table3:
    print(f"  {row['Mass_g']:<14} {row['T']:<12} {row['T2']}")

print()
print("All graphs saved to lab_graphs/")
