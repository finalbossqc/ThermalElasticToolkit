#include "MuTerm.h"
#include "ModDiv.h"

registerMooseObject("ThermalApp", MuTerm);

InputParameters MuTerm::validParams() {
	InputParameters params = ModDiv::validParams();
	params.addRequiredParam<RealVectorValue>("alpha", "weak contribution extra coefficient");
	return params;
}

MuTerm::MuTerm(const InputParameters &parameters): ModDiv(parameters),
	_grad_vx(coupledGradient("vx")),
	_grad_vy(coupledGradient("vy")),
	_grad_vz(coupledGradient("vz")),
	_mu(getMaterialProperty<Real>("mu")),
	_lambda(getMaterialProperty<Real>("lambda")),
	_alpha(getParam<RealVectorValue>("alpha")) {
}

Real MuTerm::computeQpResidual() {
	return -_mu[_qp] * ( _alpha(0) * _grad_vx[_qp](0) + _alpha(1) * _grad_vy[_qp](1) + _alpha(2) * _grad_vz[_qp](2) ) * _test[_i][_qp];
}
