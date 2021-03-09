# rst Imports
import numpy as np
from pygeo import pyGeo

# rst Airfoil file
naf = 10

airfoil_list = ["rae2822.dat"] * naf

# rst Wing definition
# Airfoil leading edge positions
x = np.linspace(0.0, 7.5, naf)
y = np.linspace(0.0, 0.0, naf)
z = np.linspace(0.0, 14.0, naf)

offset = np.zeros((naf, 2))  # x-y offset applied to airfoil position before scaling

# Airfoil rotations
rot_x = [0.0] * naf
rot_y = [0.0] * naf
rot_z = [0.0] * naf

# Airfoil scaling
# chord = [5.0, 1.5]  # chord lengths
chord = np.linspace(5.0, 1.5, naf)

# rst Run pyGeo
wing = pyGeo(
    "liftingSurface",
    xsections=airfoil_list,
    scale=chord,
    offset=offset,
    x=x,
    y=y,
    z=z,
    rotX=rot_x,
    rotY=rot_y,
    rotZ=rot_z,
    tip="rounded",
    bluntTe=True,
    squareTeTip=True,
    teHeight=0.25 * 0.0254,
)

# rst Write output files
wing.writeTecplot("wing.dat")
wing.writeIGES("wing.igs")
#wing.writeTin("wing.tin")
