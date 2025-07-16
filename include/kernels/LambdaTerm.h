#pragma once

#include "Kernel.h"
#include "ModDiv.h"

class LambdaTerm : public ModDiv {
	public:
		LambdaTerm(const InputParameters &parameters);
		static InputParameters validParams();

	protected:
		virtual Real computeQpResidual() override;	
	
	private:
		const VariableGradient & _grad_vx;
		const VariableGradient & _grad_vy;
		const VariableGradient & _grad_vz;
		const MaterialProperty<Real> & _mu;
		const MaterialProperty<Real> & _lambda;
};
