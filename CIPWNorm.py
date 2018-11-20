'''
Title: CIPW Norm Calculation
Author: Nick Sylva
Date: 12/31/2017

Calculates the CIPW Norm based on provided weight percentage of oxides/elements
in a rock sample. The output is the weight percentage of normative minerals.

'''

#Element/Oxide Object:

class ElementOrOxide(object):
	'''
	Defines an Element or an Oxide.
	Properties: 
		name (string): represents name of the Element or Oxide. ex. SiO2 or
		Silcon Dioxide
		mol_weight (float, 2 decimal places): Molecular weight of an Element
		or Oxide. ex. 60.08 for SiO2
		weight_percent (float, 2 decimal places): nominal percentage of an
		Element or Oxide in a given Rock.
		mole_proportion (float, 4 decimal places): weight_percent divided by
		mol_weight
	'''

	def __init__(self,name,weight_percent):
		self.name = name
		self.mol_weight = StandardElementsAndOxides[name]
		self.weight_percent = weight_percent
		try:
			self.mole_proportion = round(self.weight_percent/self.mol_weight,4)
		except ZeroDivisionError:
			self.mole_proportion = 0

	def __str__(self):
		return 'Element/Oxide: {0}\nMolecular Weight: {1} mols'.format(self.name,str(self.mol_weight))

	@property 
	def name(self):
		return self._name
	@name.setter
	def name(self, value):
		self._name = value

	@property 
	def mol_weight(self):
		return self._mol_weight
	@mol_weight.setter
	def mol_weight(self, value):
		self._mol_weight = round(value,2)

	@property 
	def weight_percent(self):
		return self._weight_percent
	@weight_percent.setter
	def weight_percent(self, value):
		self._weight_percent = round(value*100,2)

	@property 
	def mole_proportion(self):
		return self._mole_proportion
	@mole_proportion.setter
	def mole_proportion(self, value):
		self._mole_proportion = value

#factory function to create a new Element or Oxide
def create_ElementOrOxide(name,weight_percent):
	new_ElementOrOxide = ElementOrOxide(name,weight_percent)
	return new_ElementOrOxide

class Mineral(object):
	'''
	Defines a Mineral.
	Properties: 
		name (string): represents name of the Mineral. ex. Quartz, Corundum
		abbr (string): abbreviation of the Mineral. ex. qz, crn
		mtw_conversion_factor (float, 2 decimal places): Mole-to-Weight
		conversion factor. Used for converting from mole proportions to weight
		proportions. ex. 60.06 for qz or 101.96 for crn
	'''

	def __init__(self,name,abbr,key_oxide,mtw_conversion_factor):
		self.name = name
		self.abbr = abbr
		self.key_oxide = key_oxide
		self.mtw_conversion_factor = mtw_conversion_factor
	
	def __str__(self):
		return '''Mineral: {0}\nAbbreviation: {1}\nKey Oxide: {2}\nMole-to-weight conversion factor: {3}
			   '''.format(self.name, self.abbr,self.key_oxide,str(self.mtw_conversion_factor))

	@property 
	def name(self):
		return self._name
	@name.setter
	def name(self, value):
		self._name = value
	
	@property 
	def abbr(self):
		return self._abbr
	@abbr.setter
	def abbr(self, value):
		self._abbr = value	
	
	@property 
	def key_oxide(self):
		return self._key_oxide
	@key_oxide.setter
	def key_oxide(self, value):
		self._key_oxide = value

	@property 
	def mtw_conversion_factor(self):
		return self._mtw_conversion_factor
	@mtw_conversion_factor.setter
	def mtw_conversion_factor(self, value):
		self._mtw_conversion_factor = value		

#factory function to create a new Mineral
def create_Mineral(name,lookup_dict):
	abbr = lookup_dict[name]['abbr']
	key_oxide = lookup_dict[name]['key_oxide']
	mtw_conversion_factor = lookup_dict[name]['mtw_conversion_factor']
	new_Mineral = Mineral(name,abbr,key_oxide,mtw_conversion_factor)
	return new_Mineral

class Rock(object):
	'''
	Defines a Rock.
	Properties:
		label (string): Name or label for the rock.
		components_EO (dictionary): dictionary of Element/Oxide components
		of the Rock. Key is the Element/Oxide name and value is the weight 
		percentage expressed as a float rounded to 4 decimal places. ex:
			{
			'Silcon Dioxide':0.5006 #50.06%
			'Titanium Oxide':0.0187 #1.87%
			}
		components_Mineral (dictionary): dictionary of Mineral components
		of the Rock. Not calculated on __init__ but is the result of the
		Analysis process. The output of Analysis is the Rock object with this
		property populated.
	'''
	def __init__(self,label,components_EO = {},components_Mineral = {}):
		self.label = label
		self.components_EO = components_EO
		self.components_Mineral = components_Mineral
	
	@property 
	def label(self):
		return self._label
	@label.setter
	def label(self, value):
		self._label = value

	@property 
	def components_EO(self):
		return self._components_EO
	@components_EO.setter
	def components_EO(self, value):
		self._components_EO = {}
		#EO: Element/Oxide | WP: Weight Percentage
		try:
			for EO, WP in value.items():
				self._components_EO[EO] = create_ElementOrOxide(EO,WP)
		except Exception as E:
			print('It is likely that you did not provide the Element/Oxide \
				  components as a dictionary of E/O : Weight Percentage \
				  pairs.', E)

	@property 
	def components_Mineral(self):
		return self._components_Mineral
	@components_Mineral.setter
	def components_Mineral(self, value):
		self._components_Mineral = value

def create_Rock(label,components_EO,components_Mineral = {}):
	new_Rock = Rock(label,components_EO,components_Mineral)
	return new_Rock

#Standard Elements/Oxides
StandardElementsAndOxides = {
							 'Aluminum Trioxide' : 101.96,
							 'Barium Oxide' : 153.33,
							 'Beryllium Oxide' : 25.01,
							 'Carbon Dioxide' : 44.01,
							 'Calcium Oxide' : 56.08,
							 'Chlorine' : 35.45,
							 'Chromium-3 Oxide' : 151.99,
							 'Fluorine' : 19.00,
							 'Iron-2 Oxide' : 71.85,
							 'Iron-3 Oxide' : 159.69,
							 'Water' : 18.02,
							 'Potassium Oxide' : 94.20,
							 'Magnesium Oxide' : 40.30,
							 'Manganese Oxide' : 70.94,
							 'Sodium Oxide' : 61.98,
							 'Nickel Oxide' : 74.69,
							 'Phosphorus Pentoxide' : 141.94,
							 'Sulphur' : 32.06,
							 'Silicon Dioxide' : 60.08,
							 'Titanium Dioxide' : 79.88,
							 'Zinc Oxide' : 81.38,
							 'Zirconium Dioxide' : 123.22
							}

'''
#Normative Minerals
Dictionary describing each Normative Mineral, including: Name, Abbreviation,
and Mole-to-weight conversion factor.
'''
NormativeMinerals = {
					 'Quartz' : {'key_oxide': 'Silicon Dioxide',
					 			 'abbr' : 'qz', 
					 			 'mtw_conversion_factor' : 60.08
					 			 },
					 'Corundum' : {'key_oxide': 'Aluminum Trioxide',
					 			 'abbr' : 'crn',
					 			 'mtw_conversion_factor' : 101.96
					 			 },	
					 'Zircon' : {'key_oxide': 'Zirconium Dioxide',
					 			 'abbr' : 'zrc',
					 			 'mtw_conversion_factor' : 183.30
					 			 },
					 'Orthoclase' : {'key_oxide': 'Potassium Oxide',
					 			 'abbr' : 'or',
					 			 'mtw_conversion_factor' : 556.64
					 			 },
					 'Albite' : {'key_oxide': 'Sodium Oxide',
					 			 'abbr' : 'ab',
					 			 'mtw_conversion_factor' : 524.43
					 			 },
					 'Anorthite' : {'key_oxide': 'Calcium Oxide',
					 			 'abbr' : 'an',
					 			 'mtw_conversion_factor' : 278.20
					 			 },
					 'Leucite' : {'key_oxide': 'Potassium Dioxide',
					 			 'abbr' : 'lc',
					 			 'mtw_conversion_factor' : 436.48
					 			 },
					 'Nepheline' : {'key_oxide': 'Sodium Oxide',
					 			 'abbr' : 'ne',
					 			 'mtw_conversion_factor' : 284.10
					 			 },
					 'Acmite' : {'key_oxide': 'Sodium Oxide',
					 			 'abbr' : 'ac',
					 			 'mtw_conversion_factor' : 461.99
					 			 },
					 'Diopside-Wollastonite' : {'key_oxide': 'Calcium Oxide',
					 			 'abbr' : 'di-wo',
					 			 'mtw_conversion_factor' : 116.16
					 			 },
					 'Diopside-Enstatite' : {'key_oxide': 'Magnesium Oxide',
					 			 'abbr' : 'di-en',
					 			 'mtw_conversion_factor' : 100.38
					 			 },
					 'Diopside-Ferrosilite' : {'key_oxide': 'Iron-2 Oxide',
					 			 'abbr' : 'di-fs',
					 			 'mtw_conversion_factor' : 131.93
					 			 },
					 'Wollastonite' : {'key_oxide': 'Calcium Oxide',
					 			 'abbr' : 'wo',
					 			 'mtw_conversion_factor' : 116.16
					 			 },
					 'Hypersthene-Enstatite' : {'key_oxide': 'Magnesium Oxide',
					 			 'abbr' : 'hy-en',
					 			 'mtw_conversion_factor' : 100.38
					 			 },
					 'Hypersthene-Ferrosilite' : {'key_oxide': 'Iron-2 Oxide',
					 			 'abbr' : 'hy-fs',
					 			 'mtw_conversion_factor' : 131.93
					 			 },
					 'Olivine-Forsterite' : {'key_oxide': 'Magnesium Oxide',
					 			 'abbr' : 'ol-fo',
					 			 'mtw_conversion_factor' : 70.34
					 			 },
					 'Olivine-Fayalite' : {'key_oxide': 'Iron-2 Oxide',
					 			 'abbr' : 'ol-fa',
					 			 'mtw_conversion_factor' : 101.89
					 			 },
					 'Ca-orthosilicate' : {'key_oxide': 'Calcium Oxide',
					 			 'abbr' : 'cs',
					 			 'mtw_conversion_factor' : 86.12
					 			 },
					 'Magnetite' : {'key_oxide': 'Iron-2 Oxide',
					 			 'abbr' : 'mt',
					 			 'mtw_conversion_factor' : 231.54
					 			 },
					 'Chromite' : {'key_oxide': 'Chromium-3 Oxide',
					 			 'abbr' : 'chr',
					 			 'mtw_conversion_factor' : 223.84
					 			 },
					 'Hematite' : {'key_oxide': 'Iron-3 Oxide',
					 			 'abbr' : 'hem',
					 			 'mtw_conversion_factor' : 159.69
					 			 },
					 'Ilmenite' : {'key_oxide': 'Titanium Dioxide',
					 			 'abbr' : 'ilm',
					 			 'mtw_conversion_factor' : 151.73
					 			 },
					 'Titanite' : {'key_oxide': 'Titanium Dioxide',
					 			 'abbr' : 'spn',
					 			 'mtw_conversion_factor' : 196.04
					 			 },
					 'Perovskite' : {'key_oxide': 'Titanium Dioxide',
					 			 'abbr' : 'pf',
					 			 'mtw_conversion_factor' : 135.96
					 			 },
					 'Rutile' : {'key_oxide': 'Titanium Dioxide',
					 			 'abbr' : 'rt',
					 			 'mtw_conversion_factor' : 79.88
					 			 },
					 'Apatite' : {'key_oxide': 'Phosphorus Pentoxide',
					 			 'abbr' : 'ap',
					 			 'mtw_conversion_factor' : 336.21
					 			 },
					 'Fluorite' : {'key_oxide': 'Fluorine',
					 			 'abbr' : 'fr',
					 			 'mtw_conversion_factor' : 39.04
					 			 },
					 'Pyrite' : {'key_oxide': 'Sulphur',
					 			 'abbr' : 'pyr',
					 			 'mtw_conversion_factor' : 59.98
					 			 },
					 'Calcite' : {'key_oxide': 'Carbon Dioxide',
					 			 'abbr' : 'cc',
					 			 'mtw_conversion_factor' : 100.09
					 			 }
					}

test_rock_components = {
						'Silicon Dioxide'      : 0.5006,
						'Titanium Dioxide'     : 0.0187,
						'Aluminum Trioxide'    : 0.1594,
						'Iron-3 Oxide'         : 0.0390,
						'Iron-2 Oxide'         : 0.0750,
						'Manganese Oxide'      : 0.0020,
						'Magnesium Oxide'      : 0.0698,
						'Calcium Oxide'        : 0.0970,
						'Sodium Oxide'         : 0.0294,
						'Potassium Oxide'      : 0.0108,
						'Phosphorus Pentoxide' : 0.0034
					   }


def analysis_CIPWNorm(rock):
	'''
	Input: Rock Object with known weight percentages of key oxides

	Output: Rock Object with CIPW Norm Calculated mineral components.
	'''
	provisional_mineral_balances = []
	#load initial oxide balances
	oxide_balances = {oxide:obj.mole_proportion for (oxide, obj) in rock.components_EO.items()}
	
	def calc_oxide_balance(control_oxide,proportional_oxide,proportion):
		'''		
		Input:
		 - control_oxide: Oxide to control the transaction
		 - proportional_oxide: Oxide reduced in proportion with the proportional_oxide
		 - proportion: the ratio to use to reduce the proportional_oxide. The
		   control_oxide is always reduced by its own amount
		'''
		try:
			control_oxide_balance = oxide_balances[control_oxide]
		except KeyError:
			print('{0} not present in rock.'.format(control_oxide))
			control_oxide_balance = 0
		try:
			proportional_oxide_balance = oxide_balances[proportional_oxide]
		except KeyError:
			print('{0} not present in rock.'.format(proportional_oxide))
			proportional_oxide_balance = 0
		# control = 2 > prop = 3 /ratio:2
		# 2>1.5
		# control reduced to 0.5 left, prop reduced to 0
		# 1.5 of mineral is created
		# Output:
		#   - set new control balance
		#   - set new prop balance
		#   - return mineral creation amount
		if control_oxide_balance != 0 and proportional_oxide_balance != 0:
			if proportional_oxide != 'Silicon Dioxide' and control_oxide_balance > proportional_oxide_balance/proportion:
				new_mineral_amount = proportional_oxide_balance/proportion
				control_oxide_balance -= new_mineral_amount
				proportional_oxide_balance = 0
				oxide_balances[control_oxide] = control_oxide_balance
				oxide_balances[proportional_oxide] = proportional_oxide_balance
				return new_mineral_amount
			else:
				new_mineral_amount = control_oxide_balance
				proportional_oxide_balance -= control_oxide_balance*proportion
				control_oxide_balance = 0
				oxide_balances[control_oxide] = control_oxide_balance
				oxide_balances[proportional_oxide] = proportional_oxide_balance
				return new_mineral_amount
		else:
			print('Oxide Calculation failed for {0} ({1}) and {2} ({3}). No new mineral created.'.format(control_oxide,control_oxide_balance,proportional_oxide,proportional_oxide_balance))


	#STEP 1: Calcite = 1:1 CO2:CaO if no CO2 -> skip
	Calcite = calc_oxide_balance('Carbon Dioxide','Calcium Oxide',1)
	provisional_mineral_balances['Calcite'] = Calcite

	#STEP 2: Apatite = 1:3.33 P2O5:CaO if no P2O5 ->skip
	Apatite = calc_oxide_balance('Phosphorus Pentoxide','Calcium Oxide',3.33)
	provisional_mineral_balances['Apatite'] = Apatite

	#STEP 3: Pyrite = 1:0.5 FeO:S if no S -> skip
	Pyrite = calc_oxide_balance('Sulphur','Iron-2 Oxide',0.5)
	provisional_mineral_balances['Pyrite'] = Pyrite

	#STEP 4: Ilmenite = TiO2:FeO
	Ilmenite = calc_oxide_balance('Titanium Dioxide','Iron-2 Oxide',1)
	provisional_mineral_balances['Ilmenite'] = Ilmenite
	#If there is any TiO2 left turn it into provisional sphene
	if oxide_balances['Titanium Dioxide'] != 0:
		Sphene = oxide_balances['Titanium Dioxide']
		oxide_balances['Calcium Oxide'] -= Sphene
		oxide_balances['Silicon Dioxide'] -= Sphene
		provisional_mineral_balances['Sphene'] = Sphene
		oxide_balances['Titanium Dioxide'] = 0
	
	#STEP 5: Zircon = ZrO2:SiO2
	Zircon = calc_oxide_balance('Zirconium Dioxide','Silicon Dioxide',1)
	provisional_mineral_balances['Zircon'] = Zircon

	#STEP 6: Fluorite = 1:0.5 CaO:F
	Fluorite = calc_oxide_balance('Fluorine','Calcium Oxide',0.5)
	provisional_mineral_balances['Fluorite'] = Fluorite

	#STEP 7: Chromite = Cr2O3:FeO
	Chromite = calc_oxide_balance('Chromium-3 Oxide', 'Iron-2 Oxide', 1)
	provisional_mineral_balances['Chromite'] = Chromite

	#STEP 8: Orthoclase' (provisional) = 




	#STEP 10: Anorthite
	

	#case where there is CaO left over and Sphene has been created provisionally
	try:
		Ca = oxide_balances['Calcium Oxide']
		if Ca > 0:
	#Check remaining Al2O3; make additional Anorthite by up to the amount of sphene previously created provisionally
	

	#BELOW IS WRONG - YOU DONT TAKE AWAY SPHENE

			Ti = provisional_mineral_balances['Sphene']
			if  0 < Ti <= Ca:
				#take away sphene and use excess TiO2 for Rutile
				provisional_mineral_balances['Sphene'] = 0
				provisional_mineral_balances['Rutile'] = Ti
				#free up Ca and Si
				Ca += Ti
				Si = Ti
				oxide_balances['Calcium Oxide'] = Ca
				oxide_balances['Silicon Dioxide'] = Si
			elif Ti > Ca:
				#subtract Sphene by the excess amount og 

	except KeyError as KE:
		print('No Excess TiO2 from STEP 4.', KE)


def main():
	test_rock = Rock('test',test_rock_components)
	analysis_CIPWNorm(test_rock)
	#min_list = []
	#for mineral in NormativeMinerals.keys():
	#	min_list.append(create_Mineral(mineral,NormativeMinerals))
	#for min in min_list:
	#	print(min)
	#print('\n')
	#for mineral, obj in NormativeMinerals.items():
	#	print(obj)

if __name__ == '__main__':
	main()