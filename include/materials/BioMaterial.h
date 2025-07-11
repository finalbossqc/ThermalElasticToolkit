#include "Material.h"

class BioMaterial : public Material {
	public:
		BioMaterial(const InputParameters &parameters);
		static InputParameters validParams();
	protected:
	
	private:
		MaterialProperty<Real> & _density;
		MaterialProperty<Real> & _mu;
		MaterialProperty<Real> & _lambda;
};
