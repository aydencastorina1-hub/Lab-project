"""
Lab 18 – Simple Harmonic Motion: Pendulums and Springs
Generates fake data and graphs styled to match Vernier Graphical Analysis app.
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

matplotlib.rcParams.update({
    'font.family': 'Liberation Sans',
    'font.size': 12,
})

np.random.seed(42)
os.makedirs('lab_graphs', exist_ok=True)

# ══════════════════════════════════════════════════════════════════
#  VERNIER GRAPHICAL ANALYSIS COLOUR / STYLE CONSTANTS
#  (matched pixel-by-pixel from the app screenshot)
# ══════════════════════════════════════════════════════════════════
BG          = '#C4C4C4'   # overall gray background
PLOT_BG     = '#FFFFFF'   # white axes area
GRID        = '#E2E2E2'   # thin light-gray grid lines
DOT         = '#2E7D32'   # dark-green data dots
DOT_EDGE    = '#1B5E20'   # slightly darker edge on dots
BOX_EDGE    = '#4A4A4A'   # border on axis-label / scale boxes
STATUS_BG   = '#DEDEDE'   # status-bar pill background
TICK_COL    = '#111111'   # tick-label colour


# ──────────────────────────────────────────────────────────────────
#  PHYSICS DATA
# ──────────────────────────────────────────────────────────────────
g = 9.80
PENDULUM_MASS_G = 127   # 3-D printed bob + 13 washers + hardware

lengths_cm = [20, 30, 40, 50, 60]

def T_pendulum(L_m):
    return 2 * np.pi * np.sqrt(L_m / g)

data_table1 = []
for L in lengths_cm:
    T_th = T_pendulum(L / 100)
    t1   = round(T_th + np.random.uniform(-0.005, 0.005), 3)
    t2   = round(T_th + np.random.uniform(-0.005, 0.005), 3)
    data_table1.append({'L_cm': L, 'T1': t1, 'T2': t2,
                         'T_avg': round((t1 + t2) / 2, 3)})


# ══════════════════════════════════════════════════════════════════
#  CORE GRAPH BUILDER — Period vs Time (Photogate)
# ══════════════════════════════════════════════════════════════════
def make_photogate_graph(L_cm, T_avg, n_osc=10, outfile=None):
    """
    Replicates the exact look of Vernier Graphical Analysis in
    Photogate Timing / Period mode.
    """
    # ── generate realistic period measurements ──────────────────
    # Real lab sessions run 45-55 oscillations — that's what fills
    # the x-axis the way the real Vernier app looks.
    periods = T_avg + np.random.normal(0, 0.0011, n_osc)
    times   = np.cumsum(periods)
    last_t  = times[-1]
    last_p  = periods[-1]

    # ── x-axis nice range ────────────────────────────────────────
    x_raw = last_t * 1.10
    if   x_raw <=  6:  x_step =  1
    elif x_raw <= 15:  x_step =  2
    elif x_raw <= 35:  x_step =  5
    else:              x_step = 10
    x_max = float(np.ceil(x_raw / x_step) * x_step)

    # ── figure — exact iPad landscape proportions ────────────────
    fig = plt.figure(figsize=(13.44, 8.19), dpi=150)
    fig.patch.set_facecolor(BG)

    # axes margins measured from real app screenshots:
    #   left  ≈ 8.5 %   (y-label box + tick labels)
    #   bottom ≈ 16 %   (x-tick labels + Time(s) box + status bar)
    #   right ≈  1 %
    #   top   ≈  5 %
    L_frac = 0.085
    B_frac = 0.160
    W_frac = 0.910
    H_frac = 0.800
    ax = fig.add_axes([L_frac, B_frac, W_frac, H_frac])
    ax.set_facecolor(PLOT_BG)

    # ── axis limits & ticks ──────────────────────────────────────
    ax.set_xlim(0, x_max)
    ax.set_ylim(0, 10)
    ax.set_yticks(range(0, 10))           # 0–9 on axis; "10" in corner box
    ax.set_xticks(np.arange(0, x_max + x_step, x_step))

    # ── grid — very light, matching real app ─────────────────────
    ax.grid(True, color=GRID, linewidth=0.85, linestyle='-', zorder=0)
    ax.set_axisbelow(True)

    # ── spines ───────────────────────────────────────────────────
    for sp in ax.spines.values():
        sp.set_color('#BBBBBB')
        sp.set_linewidth(0.5)

    # ── tick labels — no tick marks, Liberation Sans 13 pt ───────
    ax.tick_params(axis='both', which='both',
                   length=0, labelsize=13,
                   colors=TICK_COL, pad=6)
    ax.set_xlabel('')
    ax.set_ylabel('')

    # ── DATA DOTS ─────────────────────────────────────────────────
    # Size 160 → approximately matches the dot diameter in the app
    ax.scatter(times, periods,
               color=DOT, s=160,
               edgecolors=DOT_EDGE, linewidths=0.6,
               zorder=5)

    # ── VERTICAL CURSOR LINE ──────────────────────────────────────
    ax.axvline(x=last_t, color='black', lw=1.6, zorder=6)

    # figure-x of cursor (for annotations that need figure coords)
    fig_cx = L_frac + (last_t / x_max) * W_frac

    # ── "×" CLOSE HANDLE — just above the white plot, in gray ────
    # In the real app the × sits to the right of the cursor line,
    # a few px above the top edge of the plot.
    fig.text(fig_cx + 0.008, 0.953, '×',
             ha='center', va='center',
             fontsize=16, color='#111111', fontweight='bold',
             fontfamily='Liberation Sans')

    # ── PERIOD ANNOTATION BUBBLE ──────────────────────────────────
    # Positioned to the right of cursor at the y-level of the last dot.
    # No arrow — the real app just floats the box next to the cursor.
    space_right = x_max - last_t
    ann_x = last_t + max(space_right * 0.08, 0.04 * x_max)
    ann_y = last_p + 0.65
    if ann_x + 0.18 * x_max > x_max:     # too close to right edge → go left
        ann_x = last_t - 0.23 * x_max
    ax.text(ann_x, ann_y,
            f'{last_p:.6f} s',
            fontsize=12, color='#111111',
            fontfamily='Liberation Sans',
            bbox=dict(boxstyle='round,pad=0.38',
                      facecolor='white', edgecolor='#BBBBBB', linewidth=0.9),
            zorder=8)

    # ── CURSOR TIME LABEL — below x-axis tick labels ─────────────
    # In the real app: ": 64.30888 s :" centred under the cursor,
    # sitting just below the numeric x-axis labels.
    fig.text(fig_cx, 0.092,
             f': {last_t:.5f} s :',
             ha='center', va='center',
             fontsize=10, color='#111111',
             fontfamily='Liberation Sans',
             bbox=dict(boxstyle='round,pad=0.28',
                       facecolor='white', edgecolor='#BBBBBB', linewidth=0.8))

    # ── "Period (s)" LABEL — rotated white rounded-rect box ──────
    # Hugs the left edge of the figure, vertically centred on axes.
    fig.text(0.015, B_frac + H_frac * 0.50,
             'Period (s)',
             ha='center', va='center',
             rotation=90,
             fontsize=14, color='#111111',
             fontfamily='Liberation Sans',
             bbox=dict(boxstyle='round,pad=0.52',
                       facecolor='white', edgecolor=BOX_EDGE, linewidth=1.4))

    # ── "Time (s)" LABEL — white rounded-rect box, bottom centre ─
    fig.text(L_frac + W_frac * 0.50, 0.012,
             'Time (s)',
             ha='center', va='center',
             fontsize=14, color='#111111',
             fontfamily='Liberation Sans',
             bbox=dict(boxstyle='round,pad=0.52',
                       facecolor='white', edgecolor=BOX_EDGE, linewidth=1.4))

    # ── "10" SCALE BOX — exact top-left corner of axes ───────────
    ax.text(-0.036, 1.002, '10',
            transform=ax.transAxes,
            ha='center', va='bottom',
            fontsize=12, color='#111111',
            fontfamily='Liberation Sans',
            bbox=dict(boxstyle='square,pad=0.36',
                      facecolor='white', edgecolor=BOX_EDGE, linewidth=1.4),
            zorder=10,
            clip_on=False)

    # ── BOTTOM STATUS BAR ─────────────────────────────────────────
    fig.text(0.008, 0.050,
             '  Mode: Photogate Timing   Timer  ',
             ha='left', va='center',
             fontsize=10.5, color='#111111',
             fontfamily='Liberation Sans',
             bbox=dict(boxstyle='round,pad=0.38',
                       facecolor=STATUS_BG, edgecolor='#BBBBBB', linewidth=0.8))

    fig.text(0.992, 0.050,
             '  Gate State: 0  ',
             ha='right', va='center',
             fontsize=10.5, color='#111111',
             fontfamily='Liberation Sans',
             bbox=dict(boxstyle='round,pad=0.38',
                       facecolor=STATUS_BG, edgecolor='#BBBBBB', linewidth=0.8))

    # ── SAVE ─────────────────────────────────────────────────────
    if outfile:
        plt.savefig(outfile, dpi=150,
                    facecolor=BG,
                    bbox_inches='tight',
                    pad_inches=0.04)
    plt.close()
    return times, periods


# ══════════════════════════════════════════════════════════════════
#  GENERATE ALL PENDULUM PERIOD-vs-TIME GRAPHS
#  Use 48-54 oscillations — matches what real Vernier sessions show
# ══════════════════════════════════════════════════════════════════
print("Generating Period vs Time graphs (Vernier style)…")
for row in data_table1:
    for key, T_val in [('T1', row['T1']), ('T2', row['T2'])]:
        n   = np.random.randint(48, 55)
        out = f"lab_graphs/pendulum_L{row['L_cm']}cm_{key}.png"
        make_photogate_graph(row['L_cm'], T_val, n_osc=n, outfile=out)
        print(f"  ✓  {out}")


# ══════════════════════════════════════════════════════════════════
#  T² vs L  ANALYSIS GRAPH
# ══════════════════════════════════════════════════════════════════
T_avgs = [r['T_avg'] for r in data_table1]
T2s    = [T**2 for T in T_avgs]
Ls_m   = [r['L_cm'] / 100 for r in data_table1]

fig, ax = plt.subplots(figsize=(9, 6))
fig.patch.set_facecolor(BG)
ax.set_facecolor(PLOT_BG)

ax.scatter(Ls_m, T2s, color=DOT, s=130, edgecolors=DOT_EDGE,
           linewidths=0.7, zorder=5, label='Measured data')

coeffs  = np.polyfit(Ls_m, T2s, 1)
L_fit   = np.linspace(0, 0.70, 200)
ax.plot(L_fit, np.polyval(coeffs, L_fit), 'b-', lw=1.8,
        label=f'Linear fit:  T² = {coeffs[0]:.3f} L + {coeffs[1]:.4f}')

th_slope = 4 * np.pi**2 / g     # theoretical ≈ 4.027 s²/m
ax.plot(L_fit, th_slope * L_fit, 'r--', lw=1.3,
        label=f'Theoretical:  T² = {th_slope:.3f} L')

ax.set_xlabel('Pendulum Length (m)', fontsize=13, fontfamily='Liberation Sans')
ax.set_ylabel('T²  (s²)',            fontsize=13, fontfamily='Liberation Sans')
ax.set_title('Period² vs Pendulum Length',
             fontsize=13, fontfamily='Liberation Sans')
ax.set_xlim(0, 0.70)
ax.set_ylim(0, max(T2s) * 1.30)
ax.legend(fontsize=10)
ax.grid(True, linestyle='--', alpha=0.45)
for sp in ax.spines.values():
    sp.set_color('#AAAAAA'); sp.set_linewidth(0.6)

plt.tight_layout()
plt.savefig('lab_graphs/T2_vs_Length.png', dpi=150, facecolor=BG)
plt.close()
print("  ✓  lab_graphs/T2_vs_Length.png")


# ══════════════════════════════════════════════════════════════════
#  SPRING DATA TABLES
# ══════════════════════════════════════════════════════════════════
k = 9.25   # N/m  →  T ≈ 0.801 s at 150 g

def T_spring(m_kg):
    return 2 * np.pi * np.sqrt(m_kg / k)

T_150 = T_spring(0.150)

data_table2 = []
for run, amp_cm in [(1, 1.2), (2, 2.3), (3, 3.2)]:
    T = round(T_150 + np.random.normal(0, 0.002), 3)
    data_table2.append({'Run': run, 'Mass_g': 150,
                         'T': T, 'T2': round(T**2, 4),
                         'A_m': round(amp_cm / 100, 3),
                         'f': round(1 / T, 3)})

data_table3 = []
for m_g in [50, 100, 150, 200]:
    T = round(T_spring(m_g / 1000) + np.random.normal(0, 0.003), 3)
    data_table3.append({'Mass_g': m_g, 'T': T, 'T2': round(T**2, 4)})


# ══════════════════════════════════════════════════════════════════
#  SPRING POSITION & VELOCITY vs TIME  (Vernier Motion-Sensor style)
# ══════════════════════════════════════════════════════════════════
def make_spring_graph(run_num, mass_g, amp_m, T_s, outfile=None):
    """Two-panel Position / Velocity vs Time, Vernier Motion-Detector style."""
    omega = 2 * np.pi / T_s
    dt    = 0.02          # 50 Hz (Vernier default)
    t     = np.arange(0, 5.0, dt)

    pos = amp_m  * np.cos(omega * t) + np.random.normal(0, 0.0004, len(t))
    vel = -amp_m * omega * np.sin(omega * t) + np.random.normal(0, 0.002, len(t))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13.5, 8.6),
                                   gridspec_kw={'hspace': 0.08})
    fig.patch.set_facecolor(BG)

    for ax, ydata, ylabel, colour in [
        (ax1, pos * 100, 'Position (cm)', '#1565C0'),
        (ax2, vel * 100, 'Velocity (cm/s)', '#C62828'),
    ]:
        ax.set_facecolor(PLOT_BG)
        ax.plot(t, ydata, color=colour, lw=1.35, zorder=3)
        ax.axhline(0, color='#888888', lw=0.7, zorder=2)
        ax.grid(True, color=GRID, linewidth=0.9, zorder=0)
        ax.set_axisbelow(True)
        ax.set_xlim(0, 5)
        ax.tick_params(labelsize=12, colors=TICK_COL, length=0, pad=4)
        for sp in ax.spines.values():
            sp.set_color('#AAAAAA'); sp.set_linewidth(0.5)
        ax.set_ylabel('')
        ax.set_xlabel('')

        # Y-label box (Vernier style)
        ax.text(-0.075, 0.5, ylabel,
                transform=ax.transAxes,
                ha='center', va='center', rotation=90,
                fontsize=12, color='#111111',
                fontfamily='Liberation Sans',
                bbox=dict(boxstyle='round,pad=0.45',
                          facecolor='white', edgecolor=BOX_EDGE, linewidth=1.2),
                clip_on=False)

    # X-label box on bottom panel only
    ax2.text(0.50, -0.10, 'Time (s)',
             transform=ax2.transAxes,
             ha='center', va='center',
             fontsize=13, color='#111111',
             fontfamily='Liberation Sans',
             bbox=dict(boxstyle='round,pad=0.50',
                       facecolor='white', edgecolor=BOX_EDGE, linewidth=1.3),
             clip_on=False)

    fig.suptitle(
        f'Spring SHM — Run {run_num}:  mass = {mass_g} g, '
        f'amplitude ≈ {amp_m*100:.1f} cm,  T ≈ {T_s:.3f} s',
        fontsize=11, y=0.98, fontfamily='Liberation Sans', color='#111111')

    # bottom status bar
    fig.text(0.010, 0.018, '  Mode: Motion Detector  ',
             ha='left', va='center', fontsize=10.5, color='#111111',
             bbox=dict(boxstyle='round,pad=0.38',
                       facecolor=STATUS_BG, edgecolor='#BBBBBB', linewidth=0.85))

    if outfile:
        plt.savefig(outfile, dpi=150, facecolor=BG,
                    bbox_inches='tight', pad_inches=0.05)
    plt.close()


print("\nGenerating spring Position/Velocity graphs…")
for row in data_table2:
    out = f"lab_graphs/spring_run{row['Run']}.png"
    make_spring_graph(row['Run'], row['Mass_g'], row['A_m'], row['T'], outfile=out)
    print(f"  ✓  {out}")


# ══════════════════════════════════════════════════════════════════
#  PRINT DATA TABLES
# ══════════════════════════════════════════════════════════════════
print()
print("=" * 72)
print(f"  DATA TABLE 1 — Effect of Length on Period")
print(f"  Bob mass = {PENDULUM_MASS_G} g  |  Amplitude = 15°")
print("=" * 72)
print(f"  {'Length (cm)':<14} {'Trial 1 T (s)':<17} {'Trial 2 T (s)':<17} {'Avg T (s)'}")
print("  " + "─" * 66)
for r in data_table1:
    print(f"  {r['L_cm']:<14} {r['T1']:<17} {r['T2']:<17} {r['T_avg']}")

print()
print("=" * 72)
print("  DATA TABLE 2 — Amplitude & Period (Spring, 150 g)")
print("=" * 72)
print(f"  {'Run':<6} {'Mass(g)':<10} {'T(s)':<10} {'T²(s²)':<13} {'A(m)':<10} {'f(Hz)'}")
print("  " + "─" * 66)
for r in data_table2:
    print(f"  {r['Run']:<6} {r['Mass_g']:<10} {r['T']:<10} {r['T2']:<13} {r['A_m']:<10} {r['f']}")

print()
print("=" * 46)
print("  DATA TABLE 3 — Mass & Period (Spring)")
print("=" * 46)
print(f"  {'Mass (g)':<14} {'T (s)':<13} {'T² (s²)'}")
print("  " + "─" * 42)
for r in data_table3:
    print(f"  {r['Mass_g']:<14} {r['T']:<13} {r['T2']}")

print()
print("All files saved to  lab_graphs/")
