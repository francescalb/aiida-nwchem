#!/usr/bin/env runaiida
# -*- coding: utf-8 -*-
###########################################################################
# Copyright (c), The AiiDA team. All rights reserved.                     #
# This file is part of the AiiDA code.                                    #
#                                                                         #
# The code is hosted on GitHub at https://github.com/aiidateam/aiida_core #
# For further information on the license, see the LICENSE.txt file        #
# For further information please visit http://www.aiida.net               #
###########################################################################

import os
import sys

from aiida.common.example_helpers import test_and_get_code
from aiida.plugins import DataFactory

################################################################

ParameterData = DataFactory('parameter')
StructureData = DataFactory('core.structure')
try:
    dontsend = sys.argv[1]
    if dontsend == '--dont-send':
        submit_test = True
    elif dontsend == '--send':
        submit_test = False
    else:
        raise IndexError
except IndexError:
    print('The first parameter can only be either --send or --dont-send',
          file=sys.stderr)
    sys.exit(1)

try:
    codename = sys.argv[2]
except IndexError:
    codename = None

queue = None
#queue = "Q_aries_free"
settings = None
#####

code = test_and_get_code(codename, expected_code_type='nwchem.pymatgen')

calc = code.new_calc()
calc.label = 'Test NWChem'
calc.description = 'Test calculation with the NWChem SCF code'
calc.set_max_wallclock_seconds(30 * 60)  # 30 min
calc.set_resources({'num_machines': 1})

if queue is not None:
    calc.set_queue_name(queue)

parameters = ParameterData(
    dict={
        'tasks': [{
            'theory': 'scf',
            'basis_set': {
                'O': '6-31g',
                'H': '6-31g'
            },
            'charge': 0,
            'spin_multiplicity': None,
            'title': None,
            'operation': '',
            'theory_directives': [],
            'alternate_directives': {}
        }],
        'directives': [],
        'geometry_options': ['units', 'angstroms'],
        'symmetry_options': [],
        'memory_options': [],
        'mol': {
            'sites': [
                {
                    'species': [{
                        'element': 'O',
                        'occu': 1
                    }],
                    'xyz': [0, 0, 0]
                },
                {
                    'species': [{
                        'element': 'H',
                        'occu': 1
                    }],
                    'xyz': [0, 1.43042809, -1.107152660]
                },
                {
                    'species': [{
                        'element': 'H',
                        'occu': 1
                    }],
                    'xyz': [0, -1.43042809, -1.107152660]
                },
            ]
        }
    })

calc.use_parameters(parameters)

if submit_test:
    subfolder, script_filename = calc.submit_test()
    print(f"Test_submit for calculation (uuid='{calc.uuid}')")
    print(
        f'Submit file in {os.path.join(os.path.relpath(subfolder.abspath), script_filename)}'
    )
else:
    calc.store_all()
    print(
        f"created calculation; calc=Calculation(uuid='{calc.uuid}') # ID={calc.dbnode.pk}"
    )
    calc.submit()
    print(
        f"submitted calculation; calc=Calculation(uuid='{calc.uuid}') # ID={calc.dbnode.pk}"
    )
