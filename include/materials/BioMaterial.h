#include "Material.h"

class BioMaterial : public Material {
	public:
		BioMaterial(const InputParameters &parameters);
		static InputParameters validParams();
	protected:
		virtual void computeQpProperties() override;
	
	private:
		MaterialProperty<Real> & _density;
		MaterialProperty<Real> & _mu;
		MaterialProperty<Real> & _lambda;
		MaterialProperty<Real> & _alpha;
		MaterialProperty<Real> & _Qs;
};
