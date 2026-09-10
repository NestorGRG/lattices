import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from itertools import product

# --- AÑADIR ESTA CONFIGURACIÓN ---
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['font.size'] = 25
plt.rcParams['mathtext.fontset'] = 'stix' 

def draw_cubic_cell(ax, points, title, color='royalblue'):
    """Dibuja una celda cúbica con sus aristas y átomos, forzando proporción 1:1:1."""
    r = [0, 1]
    vertices = list(product(r, r, r))
    
    # draw solid edges
    for s, e in product(vertices, vertices):
        if sum(np.abs(np.array(s) - np.array(e))) == 1:
            ax.plot3D(*zip(s, e), color="black", linestyle="-", linewidth=1.5, alpha=0.6)
            
    # draw atoms
    xs, ys, zs = zip(*points)
    ax.scatter(xs, ys, zs, color=color, s=300, depthshade=True, edgecolors='k', linewidth=1.5, zorder=5)
    
    ax.set_title(title, pad=10, loc='left', fontweight='normal')
    ax.set_axis_off()
    ax.set_xlim([-0.2, 1.2])
    ax.set_ylim([-0.2, 1.2])
    ax.set_zlim([-0.2, 1.2])
    
    # unified perspective
    ax.set_box_aspect([1, 1, 1]) 
    ax.view_init(elev=20, azim=30)

def draw_hcp_cell(ax, title, color='#00828D'):
    """Dibuja el prisma HCP con la celda primitiva resaltada y perspectiva unificada."""
    a = 1.0
    c = 1.633 * a  # Relación c/a ideal
    
    # hexagonal base coordinates
    theta = np.linspace(0, 2*np.pi, 7)
    hex_x = a * np.cos(theta)
    hex_y = a * np.sin(theta)
    
    # 1. Draw dashed lines for the prism edges
    ax.plot(hex_x, hex_y, np.zeros_like(hex_x), 'k--', alpha=0.3) 
    ax.plot(hex_x, hex_y, np.full_like(hex_x, c), 'k--', alpha=0.3) 
    for x, y in zip(hex_x[:-1], hex_y[:-1]):
        ax.plot([x, x], [y, y], [0, c], 'k--', alpha=0.3) 
        
    for x, y in zip(hex_x[:-1], hex_y[:-1]):
        ax.plot([0, x], [0, y], [0, 0], 'k--', alpha=0.3)
        ax.plot([0, x], [0, y], [c, c], 'k--', alpha=0.3)

    # 2. Solid lines
    prim_x = [0, hex_x[1], hex_x[0], hex_x[5], 0]
    prim_y = [0, hex_y[1], hex_y[0], hex_y[5], 0]
    
    ax.plot(prim_x, prim_y, np.zeros_like(prim_x), 'k-', linewidth=2.5, alpha=0.8)
    ax.plot(prim_x, prim_y, np.full_like(prim_x, c), 'k-', linewidth=2.5, alpha=0.8)
    for px, py in zip(prim_x[:-1], prim_y[:-1]):
        ax.plot([px, px], [py, py], [0, c], 'k-', linewidth=2.5, alpha=0.8) 
        
    # 3. Atomic coordinates
    A_x = np.append(hex_x[:-1], 0)
    A_y = np.append(hex_y[:-1], 0)
    
    theta_B = np.array([np.pi/2, 7*np.pi/6, 11*np.pi/6])
    B_x = (a / np.sqrt(3)) * np.cos(theta_B)
    B_y = (a / np.sqrt(3)) * np.sin(theta_B)

    ax.scatter(A_x, A_y, np.zeros_like(A_x), s=300, c=color, edgecolors='k', linewidth=1.5, depthshade=True, zorder=5)
    ax.scatter(A_x, A_y, np.full_like(A_x, c), s=300, c=color, edgecolors='k', linewidth=1.5, depthshade=True, zorder=5)
    ax.scatter(B_x, B_y, np.full_like(B_x, c/2), s=300, c='#E78932', edgecolors='k', linewidth=1.5, depthshade=True, zorder=6)

    ax.set_title(title, pad=10, loc='left', fontweight='normal')
    ax.set_axis_off()
    
    # prismatic proportion
    ax.set_box_aspect([1, 1, 1.633]) 
    
    # Unified perspective 
    ax.view_init(elev=20, azim=30)

# ==========================================
# FIGURE
# ==========================================
fig = plt.figure(figsize=(18, 5))
plt.subplots_adjust(wspace=0.05) 

# SC
ax1 = fig.add_subplot(141, projection='3d')
sc_points = list(product([0, 1], [0, 1], [0, 1]))
draw_cubic_cell(ax1, sc_points, "a)", color='#7CB9E8')

# BCC
ax2 = fig.add_subplot(142, projection='3d')
bcc_points = sc_points + [(0.5, 0.5, 0.5)]
draw_cubic_cell(ax2, bcc_points, "b)", color='#00308F')

# FCC
ax3 = fig.add_subplot(143, projection='3d')
fcc_points = sc_points + [(0.5, 0.5, 0), (0.5, 0, 0.5), (0, 0.5, 0.5), 
                          (0.5, 1, 0.5), (1, 0.5, 0.5), (0.5, 0.5, 1)]
draw_cubic_cell(ax3, fcc_points, "c)", color="#03801A")

# HCP
ax4 = fig.add_subplot(144, projection='3d')
draw_hcp_cell(ax4, "d)")

# Export
plt.tight_layout()
plt.savefig("bravais_lattices_tesis.png", dpi=600, bbox_inches='tight', transparent=True)
plt.show()