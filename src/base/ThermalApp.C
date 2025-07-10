#include "ThermalApp.h"
#include "Moose.h"
#include "AppFactory.h"
#include "ModulesApp.h"
#include "MooseSyntax.h"

InputParameters
ThermalApp::validParams()
{
  InputParameters params = MooseApp::validParams();
  params.set<bool>("use_legacy_material_output") = false;
  params.set<bool>("use_legacy_initial_residual_evaluation_behavior") = false;
  return params;
}

ThermalApp::ThermalApp(const InputParameters & parameters) : MooseApp(parameters)
{
  ThermalApp::registerAll(_factory, _action_factory, _syntax);
}

ThermalApp::~ThermalApp() {}

void
ThermalApp::registerAll(Factory & f, ActionFactory & af, Syntax & syntax)
{
  ModulesApp::registerAllObjects<ThermalApp>(f, af, syntax);
  Registry::registerObjectsTo(f, {"ThermalApp"});
  Registry::registerActionsTo(af, {"ThermalApp"});

  /* register custom execute flags, action syntax, etc. here */
}

void
ThermalApp::registerApps()
{
  registerApp(ThermalApp);
}

/***************************************************************************************************
 *********************** Dynamic Library Entry Points - DO NOT MODIFY ******************************
 **************************************************************************************************/
extern "C" void
ThermalApp__registerAll(Factory & f, ActionFactory & af, Syntax & s)
{
  ThermalApp::registerAll(f, af, s);
}
extern "C" void
ThermalApp__registerApps()
{
  ThermalApp::registerApps();
}
