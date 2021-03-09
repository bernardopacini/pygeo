"""
This script demonstrates the deformation of a geometry object using FFD and
the process for exporting the geometry as a tecplot or IGES file.
"""
from pygeo import pyGeo, DVGeometry
import numpy as np
import sys

def warp_liftingsurface():
    # =========================================================================
    # Load the desired pyGeo object
    # =========================================================================
    # rst LiftingSurface
    # ---------------------  Lifting Surface Definition --------------------- #
    # Airfoil file
    naf = 10  # number of airfoils
    airfoil_list = ["./geo/rae2822.dat"] * naf

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
    chord = np.linspace(5.0, 1.5, naf)

    # Run pyGeo
    geo = pyGeo(
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
    # rst LiftingSurface (end)

    # =========================================================================
    # Setup DVGeometry object
    # =========================================================================
    # rst DVGeometry
    DVGeo = DVGeometry("./ffd/ffd.xyz")

    # Create reference axis
    nRefAxPts = DVGeo.addRefAxis("wing", xFraction=0.25, alignIndex="k")

    # set the twist variable
    def twist(val, geo):
        for i in range(nRefAxPts):
            geo.rot_z["wing"].coef[i] = val[i]

    # set initial twist, we set the root twist to 5 deg so wingSurfMeshNew should reflect this
    twist0 = [0] * nRefAxPts
    twist0[0] = 5

    # add the twist design variable to DVGeo
    DVGeo.addGeoDVGlobal(dvName="twist", value=twist0, func=twist, lower=-10, upper=10, scale=1.0)
    # rst DVGeometry (end)

    # =========================================================================
    # Update pyGeo Object and output result
    # =========================================================================
    # rst UpdatePyGeo
    DVGeo.updatePyGeo(geo, "tecplot", "wingNew", nRefU=10, nRefV=10)
    # rst UpdatePyGeo (end)

def warp_iges():
    # =========================================================================
    # Load the desired pyGeo object
    # =========================================================================
    # rst IGES
    # ------------------------------ IGES File ------------------------------ #
    geo = pyGeo(fileName="./geo/wing.igs", initType="iges")
    geo.doConnectivity()
    # rst IGES (end)

    # =========================================================================
    # Setup DVGeometry object
    # =========================================================================
    DVGeo = DVGeometry("./ffd/ffd.xyz")

    # Create reference axis
    nRefAxPts = DVGeo.addRefAxis("wing", xFraction=0.25, alignIndex="k")

    # set the twist variable
    def twist(val, geo):
        for i in range(nRefAxPts):
            geo.rot_z["wing"].coef[i] = val[i]

    # set initial twist, we set the root twist to 5 deg so wingSurfMeshNew should reflect this
    twist0 = [0] * nRefAxPts
    twist0[0] = 5

    # add the twist design variable to DVGeo
    DVGeo.addGeoDVGlobal(dvName="twist", value=twist0, func=twist, lower=-10, upper=10, scale=1.0)

    # =========================================================================
    # Update pyGeo Object and output result
    # =========================================================================
    DVGeo.updatePyGeo(geo, "tecplot", "wingNew", nRefU=10, nRefV=10)

def warp_plot3d():
    # =========================================================================
    # Load the desired pyGeo object
    # =========================================================================
    # rst plot3d
    # ----------------------------- Plot3D File ----------------------------- #
    geo = pyGeo(fileName="./geo/wing.xyz", initType="plot3d")
    geo.doConnectivity()
    geo.fitGlobal()
    # rst plot3d (end)
    # =========================================================================
    # Setup DVGeometry object
    # =========================================================================
    DVGeo = DVGeometry("./ffd/ffd.xyz")

    # Create reference axis
    nRefAxPts = DVGeo.addRefAxis("wing", xFraction=0.25, alignIndex="k")

    # set the twist variable
    def twist(val, geo):
        for i in range(nRefAxPts):
            geo.rot_z["wing"].coef[i] = val[i]

    # set initial twist, we set the root twist to 5 deg so wingSurfMeshNew should reflect this
    twist0 = [0] * nRefAxPts
    twist0[0] = 5

    # add the twist design variable to DVGeo
    DVGeo.addGeoDVGlobal(dvName="twist", value=twist0, func=twist, lower=-10, upper=10, scale=1.0)

    # =========================================================================
    # Update pyGeo Object and output result
    # =========================================================================
    DVGeo.updatePyGeo(geo, "tecplot", "wingNew", nRefU=10, nRefV=10)

if __name__ == "__main__":
    if len(sys.argv) != 1:
        if sys.argv[1] == "liftingsurface":
            warp_liftingsurface()
        elif sys.argv[1] == "iges":
            warp_iges()
        elif sys.argv[1] == "plot3d":
            warp_plot3d()
        else:
            raise ValueError("Argument {} not recognized".format(sys.argv[1]))
    else:
        raise RuntimeError("Type argument must be specified, can be 'liftingsurface', 'iges', or 'plot3d'")
