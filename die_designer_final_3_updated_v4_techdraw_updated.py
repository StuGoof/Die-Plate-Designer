import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Title
st.title("Die Designer")

# Target Parameters
st.sidebar.header("Target Parameters")
pellet_size = st.sidebar.slider("Pellet Size (mm)", 0.3, 20.0, 5.0, step=0.1)
bulk_density = st.sidebar.slider("Bulk Density (g/l)", 300, 750, 500, step=1)
final_fat = st.sidebar.slider("Final Fat (%)", 7, 44, 20, step=1)
dry_meal_throughput = st.sidebar.slider("Dry Meal Throughput (tonne/h)", 0.4, 30.0, 10.0, step=0.1)

# User Inputs
plate_thickness = st.slider("Total Plate Thickness (mm)", 1.0, 40.0, 20.0, step=0.5)
final_diameter = st.slider("Final Hole Diameter (mm)", 0.3, 20.0, 10.0, step=0.05)
cone_diameter = st.slider("Cone Opening Diameter (mm)", 0.3, 20.0, 15.0, step=0.05)
channel_length = st.slider("Channel (Land) Length (mm)", 1.0, min(35.0, plate_thickness), 10.0, step=0.1)
total_holes = st.number_input("Total Number of Holes Required", min_value=1, value=100)
number_of_rows = st.number_input("Number of Rows", min_value=1, value=5)

# PCD Inputs
st.markdown("### Pitch Circle Diameters (PCD)")
pcd_values = []
holes_per_row_values = []
for i in range(number_of_rows):
    cols = st.columns(2)
    with cols[0]:
            pcd = st.slider(f"PCD for Row {i+1} (mm)", value=100.0, step=1.0)
    with cols[1]:
        holes = st.number_input(f"Holes in Row {i+1}", min_value=1, value=10)
    pcd_values.append(pcd)
    holes_per_row_values.append(holes)

# Calculations
cone_length = plate_thickness - channel_length
cone_radius = (cone_diameter - final_diameter) / 2
cone_angle_rad = np.arctan(cone_radius / cone_length)
cone_angle_deg = np.degrees(cone_angle_rad)
open_area_one_hole = np.pi * (final_diameter / 2) ** 2
total_open_area = open_area_one_hole * total_holes
open_area_per_tonne = total_open_area / dry_meal_throughput
expansion = (1 - (final_diameter / pellet_size)) * 100

# Display Outputs
st.sidebar.markdown("### Calculated Outputs")
st.sidebar.write(f"Cone Length: {cone_length:.2f} mm")
st.sidebar.write(f"Cone Angle: {cone_angle_deg:.2f}°")
st.sidebar.write(f"One Hole OA: {open_area_one_hole:.2f} mm²")
st.sidebar.write(f"Total Plate OA: {total_open_area:.0f} mm²")
st.sidebar.write(f"OA per tonne: {open_area_per_tonne:.0f} mm²/t/h")
st.sidebar.write(f"Expansion: {expansion:.1f} %")

# 2D Cross-Section Visualization
fig, ax = plt.subplots(figsize=(1.4, 2.1), dpi=200)
ax.set_xlim(-cone_diameter, cone_diameter)
ax.set_ylim(0, plate_thickness + 5)
ax.set_aspect('equal')

# Cone section
cone = patches.Polygon(
[[-cone_diameter/2, 0], [-final_diameter/2, cone_length], [-final_diameter/2, plate_thickness],
[final_diameter/2, plate_thickness], [final_diameter/2, cone_length], [cone_diameter/2, 0]],
closed=True, facecolor='white', edgecolor='black', hatch='///', linewidth=1.0)
    [[-cone_diameter/2, 0], [-final_diameter/2, cone_length], [-final_diameter/2, plate_thickness],
     [final_diameter/2, plate_thickness], [final_diameter/2, cone_length], [cone_diameter/2, 0]],
    closed=True, color='lightblue', edgecolor='black')
ax.add_patch(cone)

# Channel section
channel = patches.Rectangle((-final_diameter/2, cone_length), final_diameter, channel_length,
facecolor='white', edgecolor='black', hatch='...', linewidth=1.0)
                            color='lightgreen', edgecolor='black')
ax.add_patch(channel)

ax.axis('off')
st.pyplot(fig)

# 3D Visualization
fig3d = plt.figure(figsize=(3, 3))
ax3d = fig3d.add_subplot(111, projection='3d')
z_cone = np.linspace(0, cone_length, 30)
z_channel = np.linspace(cone_length, plate_thickness, 10)
theta = np.linspace(0, 2 * np.pi, 30)
theta_grid, z_cone_grid = np.meshgrid(theta, z_cone)
theta_grid2, z_channel_grid = np.meshgrid(theta, z_channel)

r_cone = (cone_diameter/2 - (cone_diameter - final_diameter)/2 * (z_cone / cone_length))
x_cone = r_cone[:, np.newaxis] * np.cos(theta_grid)
y_cone = r_cone[:, np.newaxis] * np.sin(theta_grid)
z_cone_plot = z_cone_grid

r_channel = np.full_like(z_channel, final_diameter/2)
x_channel = r_channel[:, np.newaxis] * np.cos(theta_grid2)
y_channel = r_channel[:, np.newaxis] * np.sin(theta_grid2)
z_channel_plot = z_channel_grid

ax3d.plot_surface(x_cone, y_cone, z_cone_plot, color='lightblue', alpha=0.8)
ax3d.plot_surface(x_channel, y_channel, z_channel_plot, color='lightgreen', alpha=0.8)
ax3d.set_xlabel("X (mm)")
ax3d.set_ylabel("Y (mm)")
ax3d.set_zlabel("Depth (mm)")
st.pyplot(fig3d)

# Ring Layout Visualization
fig_ring, ax_ring = plt.subplots(figsize=(3, 3), dpi=200)
ax_ring.set_aspect('equal')
ax_ring.set_title("Die Hole Layout")
for row in range(number_of_rows):
    radius = pcd_values[row] / 2
    for i in range(holes_per_row_values[row]):
        angle = 2 * np.pi * i / holes_per_row_values[row]
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        hole = patches.Circle((x, y), final_diameter / 2, color='gray', edgecolor='black')
        ax_ring.add_patch(hole)
    ax_ring.set_xlim(-radius - 10, radius + 10)
    ax_ring.set_ylim(-radius - 10, radius + 10)
ax_ring.axis('off')
st.pyplot(fig_ring)


# --- Technical Drawing Section ---
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as mlines
import numpy as np

# Parameters for drawing
fig, ax = plt.subplots(figsize=(6, 8), dpi=200)
ax.set_xlim(-20, 20)
ax.set_ylim(-5, plate_thickness + 10)
ax.set_aspect('equal')
ax.axis('off')

# Draw cone section
cone = patches.Polygon(
[[-cone_diameter/2, 0], [-final_diameter/2, cone_length], [-final_diameter/2, plate_thickness],
[final_diameter/2, plate_thickness], [final_diameter/2, cone_length], [cone_diameter/2, 0]],
closed=True, facecolor='white', edgecolor='black', hatch='///', linewidth=1.0)
    [[-cone_diameter/2, 0], [-final_diameter/2, cone_length], [-final_diameter/2, plate_thickness],
     [final_diameter/2, plate_thickness], [final_diameter/2, cone_length], [cone_diameter/2, 0]],
    closed=True, color='white', edgecolor='black', linewidth=1.0
)
ax.add_patch(cone)
ax.add_line(mlines.Line2D([0, 0], [-5, plate_thickness + 5], color='gray', linestyle='--', linewidth=0.8))

def draw_dimension(x1, y1, x2, y2, text, offset=2, vertical=True):
    if vertical:
        ax.annotate('', xy=(x1, y1), xytext=(x1, y2),
                    arrowprops=dict(arrowstyle='<->', color='black'))
        ax.text(x1 + offset, (y1 + y2) / 2, text, va='center', fontsize=8)
    else:
        ax.annotate('', xy=(x1, y1), xytext=(x2, y1),
                    arrowprops=dict(arrowstyle='<->', color='black'))
        ax.text((x1 + x2) / 2, y1 + offset, text, ha='center', fontsize=8)

draw_dimension(final_diameter/2 + 2, 0, final_diameter/2 + 2, cone_length, f'Cone Length: {cone_length:.1f} mm')
draw_dimension(final_diameter/2 + 2, cone_length, final_diameter/2 + 2, plate_thickness, f'Channel Length: {channel_length:.1f} mm')
draw_dimension(-cone_diameter/2, -2, cone_diameter/2, -2, f'Cone Ø: {cone_diameter:.1f} mm', offset=1, vertical=False)
draw_dimension(-final_diameter/2, plate_thickness + 2, final_diameter/2, plate_thickness + 2, f'Hole Ø: {final_diameter:.1f} mm', offset=1, vertical=False)
st.pyplot(fig)
