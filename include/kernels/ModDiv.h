#pragma once

#include "Kernel.h"

class ModDiv : public Kernel {
	public:
		ModDiv(const InputParameters &parameters);
		static InputParameters validParams();

	protected:
		virtual Real computeQpResidual() override;	
	
	private:
		VariableGradient _grad_velocity_comp;
};
