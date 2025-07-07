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
cone_diameter = st.slider("Cone Opening Diameter (mm)", 0.3, 25.0, 12.0, step=0.05)
channel_length = st.slider("Channel (Land) Length (mm)", 1.0, min(35.0, plate_thickness), 10.0, step=0.1)
total_holes = st.number_input("Total Number of Holes Required", min_value=1, value=100)
number_of_rows = st.number_input("Number of Rows", min_value=1, value=5)

# PCD Inputs and Holes per Row
st.markdown("### Pitch Circle Diameters (PCD) and Holes per Row")
pcd_values = []
holes_per_row_list = []
for i in range(number_of_rows):
    cols = st.columns(2)
    with cols[0]:
        pcd = st.slider(f"PCD for Row {i+1} (mm)", 50.0, 600.0, 100.0, step=1.0, label_visibility='visible')
    with cols[1]:
        holes = st.number_input(f"Holes in Row {i+1}", min_value=1, value=10, step=1)
    pcd_values.append(pcd)
    holes_per_row_list.append(holes)

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
st.markdown("### Calculated Outputs")
st.write(f"Cone Length: {cone_length:.2f} mm")
st.write(f"Cone Angle: {cone_angle_deg:.2f}°")
st.write(f"Open Area of One Hole: {open_area_one_hole:.2f} mm²")
st.write(f"Total Plate Open Area: {total_open_area:.2f} mm²")
st.write(f"Open Area per Tonne: {open_area_per_tonne:.2f} mm²/t/h")
st.write(f"Expansion: {expansion:.2f} %")

# 2D Cross-Section Visualization
fig, ax = plt.subplots(figsize=(0.2, 0.3), dpi=300)
ax.set_xlim(-cone_diameter, cone_diameter)
ax.set_ylim(0, plate_thickness + 5)
ax.set_aspect('equal')
ax.axis('off')

# Cone section
cone = patches.Polygon(
    [[-cone_diameter/2, 0], [-final_diameter/2, cone_length], [-final_diameter/2, plate_thickness],
     [final_diameter/2, plate_thickness], [final_diameter/2, cone_length], [cone_diameter/2, 0]],
    closed=True, color='lightblue', edgecolor='black')
ax.add_patch(cone)

# Channel section
channel = patches.Rectangle((-final_diameter/2, cone_length), final_diameter, channel_length,
                            color='lightgreen', edgecolor='black')
ax.add_patch(channel)

# Annotate values
ax.text(cone_diameter/2 + 1, plate_thickness, f"Final Ø: {final_diameter:.2f} mm", fontsize=4)
ax.text(cone_diameter/2 + 1, cone_length + channel_length/2, f"Channel: {channel_length:.2f} mm", fontsize=4)
ax.text(cone_diameter/2 + 1, cone_length/2, f"Cone: {cone_length:.2f} mm", fontsize=4)
ax.text(cone_diameter/2 + 1, cone_length/3, f"Angle: {cone_angle_deg:.1f}°", fontsize=4)

st.pyplot(fig)

# Ring Layout Visualization
fig_ring, ax_ring = plt.subplots(figsize=(0.3, 0.3), dpi=300)
ax_ring.set_aspect('equal')
ax_ring.set_title("Die Hole Layout", fontsize=6)
for row in range(number_of_rows):
    radius = pcd_values[row] / 2
    holes_in_row = holes_per_row_list[row]
    for i in range(holes_in_row):
        angle = 2 * np.pi * i / holes_in_row
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        hole = patches.Circle((x, y), final_diameter / 2, color='gray', edgecolor='black')
        ax_ring.add_patch(hole)
ax_ring.set_xlim(-max(pcd_values)/2 - 10, max(pcd_values)/2 + 10)
ax_ring.set_ylim(-max(pcd_values)/2 - 10, max(pcd_values)/2 + 10)
ax_ring.axis('off')
st.pyplot(fig_ring)
