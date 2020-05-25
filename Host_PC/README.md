# Thermal_MaskAI_On_HostPC

# Make sure you have setup your Jetson Device following the instructions outlined in the README under "Jetson" folder of this repository

# Step 1: Install mvGenTL_Acquire x86_64 (On Host PC)

1. Install "mvGenTL_Acquire-x86_64-2.37.1.exe" from this link: http://static.matrix-vision.com/mvIMPACT_Acquire/2.37.1/

# Step 2: Build and install python binding package (On Host PC)

1. Install the CCompiler corresponding to your python version (3.6.x ==> MSVC Build Tools 14.2): https://wiki.python.org/moin/WindowsCompilers#Which_Microsoft_Visual_C.2B-.2B-_compiler_to_use_with_a_specific_Python_version_.3F
2. go to "C:\Program Files\MATRIX VISION\mvIMPACT Acquire\LanguageBindings\Python" and run "compileWrapperCode.bat" as administrator