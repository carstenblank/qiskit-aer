# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2018, 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# This file is part of QuTiP: Quantum Toolbox in Python.
#
#    Copyright (c) 2011 and later, The QuTiP Project
#    All rights reserved.
#
#    Redistribution and use in source and binary forms, with or without
#    modification, are permitted provided that the following conditions are
#    met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#    3. Neither the name of the QuTiP: Quantum Toolbox in Python nor the names
#       of its contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#    HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###############################################################################
"""Utility for making the build options for compiling the Hamiltonian"""
import sys
import os
import pyximport
from pyximport import install

__all__ = ["install"]

OLD_EXT = pyximport.pyximport.get_distutils_extension


def new_get_distutils_extension(modname, pyxfilename, language_level=None):
    """Get the distutils extension"""
    extension_mod, setup_args = OLD_EXT(modname, pyxfilename, language_level)
    extension_mod.language = 'c++'
    # If on Win and Python version >= 3.5 and not in MSYS2 (i.e. Visual studio compile)
    if sys.platform == 'win32' and \
        (int(str(sys.version_info[0]) + str(sys.version_info[1])) >= 35) \
            and os.environ.get('MSYSTEM') is None:

        extension_mod.extra_compile_args = ['/w', '/O1']
    else:
        extension_mod.extra_compile_args = ['-w', '-O1']
        if sys.platform == 'darwin':
            extension_mod.extra_compile_args.append('-mmacosx-version-min=10.9')
            extension_mod.extra_link_args = ['-mmacosx-version-min=10.9']
    return extension_mod, setup_args


pyximport.pyximport.get_distutils_extension = new_get_distutils_extension
