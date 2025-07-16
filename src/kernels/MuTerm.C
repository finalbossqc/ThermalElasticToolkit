#include "MuTerm.h"
#include "ModDiv.h"

registerMooseObject("ThermalApp", MuTerm);

InputParameters MuTerm::validParams() {
	return ModDiv::validParams();
}

MuTerm::MuTerm(const InputParameters &parameters): ModDiv(parameters),
	_grad_vx(coupledGradient("vx")),
	_grad_vy(coupledGradient("vy")),
	_grad_vz(coupledGradient("vz")),
	_mu(getMaterialProperty<Real>("mu")),
	_lambda(getMaterialProperty<Real>("lambda"))
{}

Real MuTerm::computeQpResidual() {
	return -_mu[_qp] * ( _grad_vx[_qp](0) + _grad_vy[_qp](1) + _grad_vz[_qp](2) ) * _test[_i][_qp];
}
