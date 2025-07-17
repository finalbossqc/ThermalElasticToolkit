#pragma once

#include "Kernel.h"

class RhoTerm : public Kernel {
	public:
		RhoTerm(const InputParameters &parameters);
		static InputParameters validParams();

	protected:
		virtual Real computeQpResidual() override;	
	
	private:
		const VariableGradient & _grad_sigix;
		const VariableGradient & _grad_sigiy;
		const VariableGradient & _grad_sigiz;
		const MaterialProperty<Real> & _invrho;
};
