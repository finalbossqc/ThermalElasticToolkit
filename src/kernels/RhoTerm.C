#pragma once
#include "RhoTerm.h"
#include <algorithm>

registerMooseObject("ThermalApp", RhoTerm);

InputParameters RhoTerm::validParams() {
	InputParameters params = Kernel::validParams();
	params.addRequiredCoupledVar("sigix", "The component of the velocity in the x direction");
	params.addRequiredCoupledVar("sigiy", "The component of the velocity in the y direction");
	params.addRequiredCoupledVar("sigiz", "The component of the velocity in the z direction");
	return params;
}

RhoTerm::RhoTerm(const InputParameters &parameters): Kernel(parameters),
	_grad_sigix(coupledGradient("sigix")),
	_grad_sigiy(coupledGradient("sigiy")),
	_grad_sigiz(coupledGradient("sigiz")),
	_rho(getMaterialProperty<Real>("density"))
{}

Real RhoTerm::computeQpResidual() {
	Real rhodensity = std::max(_rho[_qp], 1e-6);
	return ( -1.0 / rhodensity ) * ( _grad_sigix[_qp](0) + _grad_sigiy[_qp](1) + _grad_sigiz[_qp](2) ) * _test[_i][_qp];
}
