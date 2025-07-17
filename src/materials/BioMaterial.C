#include "BioMaterial.h"

registerMooseObject("ThermalApp", BioMaterial);

InputParameters BioMaterial::validParams() {
	InputParameters params = Material::validParams();
	params.addRequiredParam<Real>("density", "Material density");
	params.addRequiredParam<Real>("mu", "mu parameter in thermoelastic equation");
	params.addRequiredParam<Real>("lambda", "lambda parameter in thermoelastic equation");
	params.addRequiredParam<Real>("alpha", "thermal expansion coefficient");
	return params;
}

BioMaterial::BioMaterial(const InputParameters & parameters) : Material(parameters), 
	_density(declareProperty<Real>("density")),
	_mu(declareProperty<Real>("mu")),
	_lambda(declareProperty<Real>("lambda")),
	_alpha(declareProperty<Real>("alpha")),
	_Qs(declareProperty<Real>("Qs"))
{}

void BioMaterial::computeQpProperties() {
	_Qs[_qp] = _alpha[_qp] * ( 3 * _lambda[_qp] + 2 * _mu[_qp] );
}
