##################################################
##################################################
# Building OCIO and OIIO:
#
# Order of building:
# 1) OCIO (core): no apps (CLI utilities)
# 2) OIIO: against OCIO (core)
# 3) OCIO (full): with apps
#
# The reason is that OIIO requires OCIO and OCIO CLI tools require OIIO.
#
# Both 'core' and 'full' OCIO builds will come from the same repo, but from different
# branches:
#     branch: rez-vX.X.X (core)
#     branch: rez-vX.X.X-tools (full)
#
# Once released, 2 different REZ packages will be available: "ocio" and "ocio_tools"
##################################################
##################################################


# name = "ocio"
name = "ocio_tools"

version = "2.3.2.hh.1.0.3"

authors = [
    "Sony Pictures Imageworks & AcademySoftwareFoundation",
]

description = """Color management"""

with scope("config") as c:
    import os

    c.release_packages_path = os.environ["HH_REZ_REPO_RELEASE_EXT"]


@early()
def requires():
    if this.name == "ocio":
        return [
            "glew",
            # "libexpat",
            "pybind11",
            "imath",
        ]
    elif this.name == "ocio_tools":
        return [
            "glew",
            # "libexpat",
            "pybind11",
            "imath",
            # "lcms",
            "oiio",
            "zlib",
        ]
    else:
        raise ValueError("Wrong package name")


private_build_requires = [
    "visual_studio",
]

variants = [
    ["python-3.9"],
    ["python-3.10"],
    ["python-3.11"],
]


def commands():
    env.REZ_OCIO_ROOT = "{root}"
    env.OCIO_ROOT = "{root}"
    env.OCIO_LOCATION = "{root}"
    env.OCIO_INCLUDE_DIR = "{root}/include"
    env.OCIO_LIBRARY_DIR = "{root}/lib"

    env.LD_LIBRARY_PATH.append("{root}/bin")
    env.LD_LIBRARY_PATH.append("{root}/lib/site-packages")
    # Require dlls to be found in PATH for Maya to load the plugin.
    env.PATH.append("{root}/bin")
    env.PATH.append("{root}/lib")
    env.PATH.append("{root}/ext/dist/include")


    if building:
        env.PKG_CONFIG_PATH.append("{root}/lib/cmake/OpenColorIO")

    if "python" in resolve:
        env.PYTHONPATH.append("{root}/lib/site-packages/PyOpenColorIO")
        env.UE_PYTHONPATH.append("{root}/lib/site-packages/PyOpenColorIO")

uuid = "repository.OpenColorIO"
