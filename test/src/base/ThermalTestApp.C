//* This file is part of the MOOSE framework
//* https://mooseframework.inl.gov
//*
//* All rights reserved, see COPYRIGHT for full restrictions
//* https://github.com/idaholab/moose/blob/master/COPYRIGHT
//*
//* Licensed under LGPL 2.1, please see LICENSE for details
//* https://www.gnu.org/licenses/lgpl-2.1.html
#include "ThermalTestApp.h"
#include "ThermalApp.h"
#include "Moose.h"
#include "AppFactory.h"
#include "MooseSyntax.h"

InputParameters
ThermalTestApp::validParams()
{
  InputParameters params = ThermalApp::validParams();
  params.set<bool>("use_legacy_material_output") = false;
  params.set<bool>("use_legacy_initial_residual_evaluation_behavior") = false;
  return params;
}

ThermalTestApp::ThermalTestApp(const InputParameters & parameters) : MooseApp(parameters)
{
  ThermalTestApp::registerAll(
      _factory, _action_factory, _syntax, getParam<bool>("allow_test_objects"));
}

ThermalTestApp::~ThermalTestApp() {}

void
ThermalTestApp::registerAll(Factory & f, ActionFactory & af, Syntax & s, bool use_test_objs)
{
  ThermalApp::registerAll(f, af, s);
  if (use_test_objs)
  {
    Registry::registerObjectsTo(f, {"ThermalTestApp"});
    Registry::registerActionsTo(af, {"ThermalTestApp"});
  }
}

void
ThermalTestApp::registerApps()
{
  registerApp(ThermalApp);
  registerApp(ThermalTestApp);
}

/***************************************************************************************************
 *********************** Dynamic Library Entry Points - DO NOT MODIFY ******************************
 **************************************************************************************************/
// External entry point for dynamic application loading
extern "C" void
ThermalTestApp__registerAll(Factory & f, ActionFactory & af, Syntax & s)
{
  ThermalTestApp::registerAll(f, af, s);
}
extern "C" void
ThermalTestApp__registerApps()
{
  ThermalTestApp::registerApps();
}
