#include "SAR.h"
#include "Function.h"

registerMooseObject("ThermalApp", SAR);

InputParameters SAR::validParams() {
	InputParameters params = Kernel::validParams();
	params.addParam<FunctionName>("func", "1", "SAR function profile");
	return params;
}

SAR::SAR(const InputParameters &parameters): Kernel(parameters),
	_mu(getMaterialProperty<Real>("mu")),
	_lambda(getMaterialProperty<Real>("lambda")),
    _alpha(getMaterialProperty<Real>("alpha")),
	_function(getFunction("func"))
{}

Real SAR::computeQpResidual() {
	return _alpha[_qp] * ( 3 * _lambda[_qp] + 2 * _mu[_qp] ) * _function.value(_t, _q_point[_qp]) * _test[_i][_qp];
}
