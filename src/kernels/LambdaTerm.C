#include "LambdaTerm.h"
#include "ModDiv.h"

registerMooseObject("ThermalApp", LambdaTerm);

InputParameters LambdaTerm::validParams() {
	return ModDiv::validParams();
}

LambdaTerm::LambdaTerm(const InputParameters &parameters): ModDiv(parameters), 
	_grad_vx(coupledGradient("vx")),
	_grad_vy(coupledGradient("vy")),
	_grad_vz(coupledGradient("vz")),
	_mu(getMaterialProperty<Real>("mu")),
	_lambda(getMaterialProperty<Real>("lambda")) {
}

Real LambdaTerm::computeQpResidual() {
	return -_lambda[_qp] * ( _grad_vx[_qp](0) + _grad_vy[_qp](1) + _grad_vz[_qp](2) ) * _test[_i][_qp];
}
