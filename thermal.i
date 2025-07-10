[Mesh]
        [mesh]
                type = GeneratedMeshGenerator
                nx = 10
                ny = 10
                nz = 10
                dim = 3
        []
[]

[Variables]
        [sigxx]
                order = FIRST
                family = LAGRANGE
                initial_condition = 0
        []

        [sigyy]
                order = FIRST
                family = LAGRANGE
                initial_condition = 0
        []

        [sigzz]
                order = FIRST
                family = LAGRANGE
                initial_condition = 0
        []

        [sigxy]
                order = FIRST
                family = LAGRANGE
                initial_condition = 0
        []

        [sigxz]
                order = FIRST
                family = LAGRANGE
                initial_condition = 0
        []

        [sigyz]
                order = FIRST
                family = LAGRANGE
                initial_condition = 0
        []

        [u]
                order = FIRST
                family = LAGRANGE
                initial_condition = 0
        []

        [v]
                order = FIRST
                family = LAGRANGE
                initial_condition = 0
        []

        [w]
                order = FIRST
                family = LAGRANGE
                initial_condition = 0
        []
[]

[Kernels]
        [ut]
                type = TimeDerivative
                variable = u
        []

        [vt]
                type = TimeDerivative
                variable = v
        []

        [wt]
                type = TimeDerivative
                variable = w
        []

        [sigxxt]
                type = TimeDerivative
                variable = sigxx
        []

        [sigxyt]
                type = TimeDerivative
                variable = sigxy
        []

        [sigxzt]
                type = TimeDerivative
                variable = sigxz
        []

        [sigyyt]
                type = TimeDerivative
                variable = sigyy
        []

        [sigyzt]
                type = TimeDerivative
                variable = sigyz
        []

        [sigzzt]
                type = TimeDerivative
                variable = sigzz
        []
[]

[BCs]
        [ubc]
                type = OutflowBC
                variable = u
                value = 0
                boundary = '0 1 2 3 4 5'
        []

        [vbc]
                type = OutflowBC
                variable = v
                value = 0
                boundary = '0 1 2 3 4 5'
        []

        [wbc]
                type = OutflowBC
                variable = w
                value = 0
                boundary = '0 1 2 3 4 5'
        []
[]

[Executioner]
        type = Transient
        dt = 0.01
        end_time = 1
        scheme = 'bdf2'
[]

[Outputs]
        exodus = false
        [other]
                type = VTK
        []
[]


