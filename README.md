[![PyPI version](https://badge.fury.io/py/sos-bash.svg)](https://badge.fury.io/py/sos-bash)
[![Build Status](https://travis-ci.org/vatlab/sos-bash.svg?branch=master)](https://travis-ci.org/vatlab/sos-bash)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f0436250e331467e8974f9d478890b2f)](https://www.codacy.com/app/BoPeng/sos-bash?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=vatlab/sos-bash&amp;utm_campaign=Badge_Grade)
[![Coverage Status](https://coveralls.io/repos/github/vatlab/sos-bash/badge.svg)](https://coveralls.io/github/vatlab/sos-bash)

# sos-bash
SoS extension for Bash scripts. Please refer to [SoS Homepage](http://vatlab.github.io/SoS/) for details.

# Installation

- If you are using conda, you can install `sos-bash` with command
  ```
  conda install sos-bash -c conda-forge
  ```
  This will install `sos-bash` (and `sos-notebook` if needed), [`bash`](https://anaconda.org/conda-forge/bash) (linux and Mac) or [`m2-bash`](https://anaconda.org/msys2/m2-bash) (windows), and [`calysto_bash`](https://github.com/Calysto/calysto_bash) kernel. The `calysto_bash` kernel is used instead of [`bash_kernel`](https://github.com/takluyver/bash_kernel) because the former supports all operating systems including `windows`.
  
 - If you are not using conda, you can install `sos-bash` with command
   ```
   pip install sos-bash
   ```
   but you will have to make sure that your system has `bash`, and a Jupyter kernel for `bash`. `sos-bash` currently supports [`bash_kernel`](https://github.com/takluyver/bash_kernel) and [`calysto_bash`](https://github.com/Calysto/calysto_bash) kernel.
   
 # Usage
 
 In a SoS notebook, you should be able to see `Bash` in the drop down box, and execute bash commands in it. You can use magics `%get` and `%put` to exchange variables between bash and other kernels but all variables will be converted to string because `bash` only supports strings.
