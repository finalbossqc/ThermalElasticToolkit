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

        [Qxx]
                type = MatBodyForce
                variable = sigxx
                material_property = Qs 
                postprocessor = -1
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

        [Qyy]
                type = MatBodyForce
                variable = sigyy
                material_property = Qs
                postprocessor = -1
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

        [Qzz]
                type = MatBodyForce
                variable = sigzz
                material_property = Qs
                postprocessor = -1
                function = 'x^2'
        []
[]

[Materials]
        [main]
                type = BioMaterial
                block = 0
                density = 1
                mu = 1
                lambda = 1
                alpha = 1
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


