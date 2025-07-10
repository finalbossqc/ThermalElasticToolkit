#include "ModDiv.h"

registerMooseObject("ThermalApp", ModDiv);

InputParameters ModDiv::validParams() {
	InputParameters params = Kernel::validParams();
	params.addRequiredCoupledVar("velocity_comp", "The component of the velocity");
	return params;
}

ModDiv::ModDiv(const InputParameters &parameters): Kernel(parameters) {
	_grad_velocity_comp = coupledGradient("velocity_comp");
}

Real ModDiv::computeQpResidual() {
	return _grad_velocity_comp[_qp](0) * _test[_qp][0] + _grad_velocity_comp[_qp](1) * _test[_qp][0] + _grad_velocity_comp[_qp](2) * _test[_qp][0];
}
