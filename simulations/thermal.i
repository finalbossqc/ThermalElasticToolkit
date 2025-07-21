[Mesh]
        [mesh]
                type = GeneratedMeshGenerator
                nx = 161
                ny = 92
                nz = 100
                xmax = 480
                ymax = 280
                zmax = 300
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

        [Ru]
                type = RhoTerm
                variable = u
                sigix = sigxx
                sigiy = sigxy
                sigiz = sigxz
        []

        [vt]
                type = TimeDerivative
                variable = v
        []

        [Rv]
                type = RhoTerm
                variable = v
                sigix = sigxy
                sigiy = sigyy
                sigiz = sigyz
        []

        [wt]
                type = TimeDerivative
                variable = w
        []

        [Rw]
                type = RhoTerm
                variable = w
                sigix = sigxz
                sigiy = sigyz
                sigiz = sigzz
        []

        [sigxxt]
                type = TimeDerivative
                variable = sigxx
        []

        [Dsigxx]
                type = LambdaTerm
                variable = sigxx
                vx = u
                vy = v
                vz = w
        []

        [Msigxx]
                type = MuTerm
                variable = sigxx
                vx = u
                vy = 0
                vz = 0
                alpha = '2 0 0'
        []

        [SARxx]
                type = SAR
                variable = sigxx
                func = '1'
        []

        [sigxyt]
                type = TimeDerivative
                variable = sigxy
        []

        [Msigxy]
                type = MuTerm
                variable = sigxy
                vx = v
                vy = u
                vz = 0
                alpha = '1 1 1'
        []

        [sigxzt]
                type = TimeDerivative
                variable = sigxz
        []

        [Msigxz]
                type = MuTerm
                variable = sigxz
                vx = w
                vy = 0
                vz = u
                alpha = '1 1 1'
        []

        [sigyyt]
                type = TimeDerivative
                variable = sigyy
        []

        [Dsigyy]
                type = LambdaTerm
                variable = sigyy
                vx = u
                vy = v
                vz = w
        []

        [Msigyy]
                type = MuTerm
                variable = sigyy
                vx = 0
                vy = v
                vz = 0
                alpha = '0 2 0'
        []

        [SARyy]
                type = SAR
                variable = sigyy
                func = '1'
        []

        [sigyzt]
                type = TimeDerivative
                variable = sigyz
        []

        [Msigyz]
                type = MuTerm
                variable = sigyz
                vx = 0
                vy = w
                vz = v
                alpha = '1 1 1'
        []

        [sigzzt]
                type = TimeDerivative
                variable = sigzz
        []

        [Dsigzz]
                type = LambdaTerm
                variable = sigzz
                vx = u
                vy = v
                vz = w
        []

        [Msigzz]
                type = MuTerm
                variable = sigzz
                vx = 0
                vy = 0
                vz = w
                alpha = '0 0 2'
        []

        [SARzz]
                type = SAR
                variable = sigzz
                func = '1'
        []
[]

[Functions]
        [SarInterpolate]
                type = PiecewiseMultilinear
                data_file = 'test.txt'
        []
[]

[Materials]
        [LameConstantMu]
                type = ParsedMaterial
                block = 0
                property_name = mu
                expression = '1'
        []

        [LameConstantLambda]
                type = ParsedMaterial
                block = 0
                property_name = lambda
                expression = '1'
        []

        [Density]
                type = ParsedMaterial
                block = 0
                property_name = rho
                expression = '1'
        []

        [ThermalExpansion]
                type = ParsedMaterial
                block = 0
                property_name = alpha
                expression = '1'
        []
[]

[Executioner]
        type = Transient
        end_time = 1e-10
        scheme = 'bdf2'
        solver_type = PJFNK
        automatic_scaling = True                

        [TimeStepper]
                type = ConstantDT
                dt = 1e-12
        []
[]

[Outputs]
        exodus = false
        [other]
                type = VTK
        []
[]


