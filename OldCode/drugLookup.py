from collections import defaultdict
import re

cocaine = ['Aunt Nora','Bernice','Binge','Blow','Bump','Charlie','Coke','Dust','Flake','Nose Candy','Paradise', 'Sneeze','Sniff','Toot','24-7','Apple jacks','Badrock',
		   'Cloud','Freebase Crack','Crumbs','Crunch and munch','Devil drug','Dice','Electric kool-aid','Fat bags','French fries','Glo','Gravel','Grit','Hail',
			  'Hard ball','Hard rock','Hotcakes','Ice cube','Jelly beans','Kryptonite','Nuggets', 'Prime time','Rockstar','Roxanne','Scrabble','Sleet','Snow coke','Sugar block', 'Topo','Tornado','Troop', 'kool-aid',
		  'kool aid', 'cocaine', 'fishscale', 'kokain', 'koks', 'cocain***', 'cocain', 'flakes', 'sociable', 'coca', 'kokaiini', 'hard candy', '3.5 Ball', 'Mk2 COLUMBIANA', 'cocaine(fishscale', 'peruvian']

cocaine = [x.lower() for x in cocaine]

# cocaine = set(cocaine) & set(drug_names)
cocaine = list(cocaine)


# barbituates = ['Barbs','Phennies','Red birds', 'Reds', 'Tooies', 'Yellow jackets', 'Yellows', 'barbituates']
# barbituates = [x.lower() for x in barbituates]
# barbituates = set(barbituates) & set(drug_names)
# barbituates = list(barbituates)


benzodiazepines = ['Rohypnol', 'Flunitrazepam','Circles', 'Date rape drug', 'Forget pill', 'Forget-me pill', 'La Rocha',
				   'Lunch money', 'Mexican Valium','Mind eraser','Pingus', 'R2', 'Reynolds', 'Rib', 'Roach', 'Roach 2',
				   'Roaches','Roachies', 'Roapies', 'Rochas Dos', 'Roofies', 'Rope', 'Rophies', 'Row-shay', 'Ruffies',
				   'Trip-and-fall', 'Wolfies', 'Benzos', 'Downers', 'Sleeping pills', 'Tranks', 'roofie', 
				   'benzodiazepine', 'benzodiazepines', 'valium', 'benzo', 'xanax', 'alprazolam', 'diazepam','diazpam', 'apo-diazepam', 'alprax-xanax', 'midazolam', 'lorazepam', 'etizolam', 'bensedin', 'clonazepam', 'klonopin', 'rivotril', 'ksalol', 'temazepam', 'bromazepam', 'zopiclone' ]
benzodiazepines = [x.lower() for x in benzodiazepines]
# benzodiazepines = list(set(benzodiazepines) & set(drug_names))

ketamine = ['Cat Valium', 'Jet', 'Special K', 'Super acid', 'Vitamin K', 'ketamine', 'ketamine-', 'ketamin', 'ketamiini', 'keta', 'KÃ©tamine', 'KETAMINE?ISOMERE']
ketamine = [x.lower() for x in ketamine]
# ketamine = list(set(ketamine) & set(drug_names))

lsd = ['lysergic acid diethylamide', 'Acid', 'Battery acid', 'Blotter', 'Bloomers', 'Blue heaven', 'California Sunshine', 'Cid', 'Cubes', 'Doses',
	   'Dots', 'Golden dragon', 'Heavenly blue', 'Hippie', 'Loony toons', 'Lucy in the sky with diamonds', 'Microdot',
	   'Pane', 'Purple Heart', 'Superman', 'Window pane', 'Yellow sunshine', 'Zen', 'lsd', 'game of thrones', 'lsd-25']
lsd = [x.lower() for x in lsd]
#lsd = list(set(lsd) & set(drug_names))

mescaline = ['Buttons', 'Cactus', 'Mesc', 'mescaline', 'peyote']
mescaline = [x.lower() for x in mescaline]
#mescaline = list(set(mescaline) & set(drug_names))

pcp = ['phencyclidine', 'Angel dust', 'Boat', 'Hog', 'Love boat', 'Peace pill','pcp']
pcp = [x.lower() for x in pcp]
#pcp = list(set(pcp) & set(drug_names))

psilocybin = ['Cubensis', 'Little smoke', 'Magic mushrooms', 'Purple passion', 'Shrooms', 'psilocybin', 'mushrooms']
psilocybin = [x.lower() for x in psilocybin]
#psilocybin = list(set(psilocybin) & set(drug_names))

ecstasy = ['Adam', 'Beans', 'Cadillac', 'California sunrise', 'Clarity', 'Essence', 'Elephants', 'Eve', 'Hug',
		   'Hug drug', 'Love drug', 'Love pill', 'Lover’s speed', 'Molly', 'Peace', 'Roll', 'Scooby snacks', 'Snowball',
		   'Uppers', 'XE', 'XTC', 'ecstasy', 'mdma', 'mdma-', 'yellow warner bros', 'glock', 'mda', 'superman', 'netto', 'q-dance', 'blue punisher', 'Teslas', '?unishers', 'blue 69', 'MDMA(84', '25gr*MDMA', 'PRICES?MDMA?UNCUT', 'SUPERMAN\\', 'TOMORROWLAND', 'Fortnites']
ecstasy = [x.lower() for x in ecstasy]
#ecstasy = list(set(ecstasy) & set(drug_names))

heroin = ['Brown sugar', 'Dope', 'Hell dust', 'Horse', 'Junk', 'Nose drops', 'Skag',
	  'Smack', 'White horse', 'heroin', 'heroine', 'heroin-', 'opium', 'heroin#4']


heroin = [x.lower() for x in heroin]
#heroin = list(set(heroin) & set(drug_names)) 

inhalants = ['Air blast', 'Ames', 'Amys', 'Aroma of men', 'Bolt', 'Boppers', 'Bullet', 'Bullet bolt', 'Buzz bomb',
			 'Discorama', 'Hardware', 'Heart-on', 'Hiagra-in-a-bottle', 'Highball', 'Hippie crack', 'Huff',
			 'Locker room', 'Medusa', 'Moon gas', 'Pearls', 'Poor man’s pot', 'Poppers','Quicksilver', 'Rush snappers',
			 'Satan’s secret', 'Shoot the breeze', 'Snappers', 'Snotballs', 'Texas shoe shine', 'Thrust',
			 'Toilet water', 'Toncho', 'Whippets', 'Whiteouts', 'inhalant', 'inhalants', 'GHB', 'GBL', 'laughing gas', 'whipped cream']

inhalants = [x.lower() for x in inhalants]
#inhalants = list(set(inhalants) & set(drug_names)) 

khat = ['bath salts', 'Arctic blasts', 'Aura', 'Avalance', 'Avalanche', 'Blizzard', 'Bloom',
	  'Blue silk', 'Bolivian bath', 'Cloud nine', 'Cotton cloud', 'Drone', 'Dynamite plus', 'Euphoria',
	  'Glow stick', 'Hurricane Charlie', 'Ivory snow', 'Ivory wave', ' Ivory wave ultra', 'Lunar wave','Mexxy',
	  'Mind change', 'Mino Charge', 'Monkey dust', 'Mystic', 'Natural energy powder', 'Ocean snow', 'Purple wave',
	  'Quicksilver', 'Recharge', 'Red dawn', 'Red dove', 'Rock on', 'Rocky Mountain High', 'Route 69', 'Sandman Party Powder',
	  'Scarface', 'Sextasy', 'Shock wave', 'Snow day', 'Snow leopard', 'Speed freak miracle', 'Stardust',
	  'Super coke', 'Tranquility', 'UP energizing', 'UP Supercharged', 'Vanilla Sky', 'Wicked X', 'XX', 'Zoom', 'cathinone' ,
	  'Abyssinian tea', 'African salad', 'Catha', 'Chat', 'Kat', 'Oat', 'khat', 'mephedrone', 'mephedorne', 'meow meow']

khat = [x.lower() for x in khat]
#khat = list(set(khat) & set(drug_names)) 



kratom = ['Biak-biak', 'Herbal speedball', 'Ketum', 'Kahuam', 'Ithang', 'Thom', 'kratom']

kratom = [x.lower() for x in kratom]
#kratom = list(set(kratom) & set(drug_names)) 



marijuana = ['Astro Yurf','Bhang', 'Blunt', 'Bud', 'Blaze', 'Dagga', 'Dope', 'Dry high', 'Ganja', 'Grass',
			 'Hemp', 'Herb', 'Home grown', 'Joint', 'Mary Jane', 'Pot', 'Reefer', 'Roach', 'Sinsemilla', 
			 'Skunk', 'Smoke', 'Texas tea', 'THC', 'Trees', 'Weed', 'White widow', 'marijuana', 'k2', 'kush', 'fruity pebbles', 'tutti frutti', 'haze', 'grand daddy purple', 'blue dream', 'white widow', 'citrus blast', 'gorrilla glue', 'durban poison', 'sativa', 'indica', 'hybrid', 'purple trainwreck', 'diesel', 'orange crush', 'cannabis', 'medical', 'gelato', 'wedding cake', 'star dawg', 'california', 'amber shatter', 'buds', 'lemon tree', 'dry-sift', 'kief', 'tangerine dream', 'cheesecake', 'green krack', 'green crack', 'maui', 'trainwreck', 'chemdawg', 'candyland', 'sunset sherbert', 'granddaddypurple', 'white buffalo', 'moby dick', 'kush//indoor', 'cookies//indoor', 'strain', 'strains', 'blueberry', 'strawberry', 'stardawg', 'blue 69', 'flying dutchman', 'jungle boys', 'black domina', 'super lemon', 'amnesia', 'thai', 'chokladkola', 'joint', 'sour cookie', 'evergreen', 'blue twist', 'pine', 'glaze', 'og', 'skywalker', 'flower', 'chemdog', 'cherry bomb', 'ortega', 'critical bilbo', 'mj', 'dank', 'alpujarrena', 'white russian', 'northern lights', 'lemon', 'jack herer', 'mr. nice', 'hydro', 'gorilla glue', 'zkittlez', 'cheese', 'indoor', 'outdoor', 'spice 5F-ADB blend', '1.75 Teen', 'gorilla glue!', 'AmnesiaUltimate', 'Cali orange', 'Blue Dream', 'purepowerplant', 'darkstar', 'odv3', 'heavy hitters', 'Kalashnikova' '455G//Grand Daddy Purple?GDP', 'blue goo', 'Sunset Sherbert', 'golden goat', 'zerozero', 'golden goat', '#Honey Moroccan Blonde', 'white widow', 'Afghan hero', 'brownies', 'Canna Butter', 'ARMAGEDDON', 'silverhaze', 'alaskan thunder fuck', 'jack herer', 'brownies-', 'ARMAGEDDON', 'cbd#thc#coco#oil#capsules']
marijuana = [x.lower() for x in marijuana]
#marijuana = list(set(marijuana) & set(drug_names))



hashish = ['Boom', 'Gangster', 'Hash', 'Hemp', 'hashish', 'hasch', 'hasch', 'hasish', 'king pens', 'kingpen', 'rick simpson oil', 'cartridge','cartridges', 'cart', 'carts', 'pollen', 'culero egg', 'golden morroccan', 'exotic carts', 'crumble', 'ginger dank', 'super polm', 'rosin', 'resin', 'ketama', 'morroccan', 'distillate', 'polm', 'shatter', 'wax', 'dab']

hashish = [x.lower() for x in hashish]
#hashish = list(set(hashish) & set(drug_names))



methamphetamine = ['Beanies', 'Crank', 'Chalk', 'Chicken feed', 'Cinnamon', 'Crink', 'Crypto',
				'Get go', 'Glass', 'Go fast', 'Ice', 'Meth', 'Methlies quick', 'Mexican crack',
				'Redneck cocaine', 'Speed', 'Tick tick', 'Tweak', 'Yellow powder', 'methamphetamine',
				'Batu', 'blade', 'cristy', 'crystal glass', 'hot ice', 
				'shabu','shards', 'stove top', 'Tina', 'ventana', 'methamphetamin', 'memphedrone', '1. Gram Of the Shard', '3.5 grams of shard', 'cartel crystal', 'Cartel Black']
methamphetamine = [x.lower() for x in methamphetamine]
#methamphetamine = list(set(methamphetamine) & set(drug_names))



# over_counter = ['CCC', 'DXM', 'Poor man’s PCP', 'Robo', 'Robotripping', 'Skittles', 'Triple C']
# over_counter = [x.lower() for x in over_counter]
# #over_counter = list(set(over_counter) & set(drug_names))


codeine = ['Captain Cody', 'Cody', 'Doors and fours', 'Lean','Loads', 'Pancakes and syrup', 'Purple drank', 
		   'Schoolboy', 'Sizzurp', 'codeine', 'dihydrocodeine']

codeine = [x.lower() for x in codeine]
#codeine = list(set(codeine) & set(drug_names))


fentanyl = ['Apache', 'China girl', 'Dance fever', 'Goodfella', 'Murder 8', 
			'Tango and Cash', 'TNT', 'Hydrocodone', 'Dihydrocodeinone','Vike', 'Watson 387', 'vicodine', 'carfentanil', 'Cyclopropyl']

fentanyl = [x.lower() for x in fentanyl]
#fentanyl = list(set(fentanyl) & set(drug_names))


hydromorphone = ['Dillies', 'Footballs', 'Smack', 'hydromorphone', 'dilaudid']
hydromorphone = [x.lower() for x in hydromorphone]
#hydromorphone = list(set(hydromorphone) & set(drug_names))



meperidine = ['Demmies', 'meperidine']
meperidine = [x.lower() for x in meperidine]
#meperidine= list(set(meperidine) & set(drug_names))


methadone = ['Amidone', 'Fizzies', 'methadone']

methadone = [x.lower() for x in methadone]
#methadone = list(set(methadone) & set(drug_names))


morphine = ['Miss Emma', 'White stuff', 'morphine', 'oramorph']

morphine = [x.lower() for x in morphine]
#morphine = list(set(morphine) & set(drug_names))


oxycodone = ['O.C.', 'OxyContin', 'Oxy 80', 'Oxycat', 'Oxycet', 'Oxycotton', 'Oxy', 'Hillbilly heroin', 'Percs', 'Perks', 'oxy', 'oxycodone', 'oxys', 'percocet', 'oxycodine', 'ox', 'oxycodon', 'roxies', 'Roxicodone']
oxycodone = [x.lower() for x in oxycodone]
#oxycodone = list(set(oxycodone) & set(drug_names))


oxymorphone = ['Biscuits', 'Blue heaven', 'Heavenly blues', 'Mrs. O', 'O bombs', 'Octagons', 'Stop signs', 'oxymorphone']

oxymorphone = [x.lower() for x in oxymorphone]
#oxymorphone = list(set(oxymorphone) & set(drug_names))


amphetamine = ['Bennies', 'Black beauties', 'Crosses','LA Turnaround', 'Truck drivers', 'Uppers', 'adderall', 
			  'benzedrine', 'amphetamine', 'dextroamphetamine', 'adderral', 'amfetamin', 'speedpaste', 'vyvanse', '3-fluorophenmetrazine', 'clobenzorex', 'dexamphetamine', '4-fluoramphetamine', '4-fmp', 'amfetamiini', 'D-methylated', 'adderall(amphetamine', 'SPEED?PASTE', 'Ampthetamine']

amphetamine = [x.lower() for x in amphetamine]
#amphetamine = list(set(amphetamine) & set(drug_names))



methylphenidate = ['concerta', 'ritalin','Diet coke','JIF', 'Kiddie cocaine', 'Kiddie coke', 'MPH', 'Poor man’s cocaine',
				   'R-ball', 'Skippy', 'Skittles', 'Smarties', 'The Smart Drug', 'Vitamin R', 'methylphenidate']

methylphenidate = [x.lower() for x in methylphenidate]
#methylphenidate = list(set(methylphenidate) & set(drug_names))


bath_salts = ['bath salts', 'Arctic blasts', 'Aura', 'Avalance', 'Avalanche', 'Bliss', 'Blizzard', 'Bloom',
			  'Blue silk', 'Bolivian bath', 'Cloud nine', 'Cotton cloud', 'Drone', 'Dynamite', 'Dynamite plus', 'Euphoria',
			  'Glow stick', 'Hurricane Charlie', 'Ivory snow', 'Ivory wave', ' Ivory wave ultra', 'Lunar wave','Mexxy',
			  'Mind change', 'Mino Charge', 'Monkey dust', 'Mystic', 'Natural energy powder', 'Ocean snow', 'Purple wave',
			  'Quicksilver', 'Recharge', 'Red dawn', 'Red dove', 'Rock on', 'Rocky Mountain High', 'Route 69', 'Sandman Party Powder',
			  'Scarface', 'Sextasy', 'Shock wave', 'Snow day', 'Snow leopard', 'Speed freak miracle', 'Stardust',
			  'Super coke', 'Tranquility', 'UP energizing', 'UP Supercharged', 'Vanilla Sky', 'Wicked X', 'XX', 'Zoom']

bath_salts = [x.lower() for x in bath_salts]
#bath_salts = list(set(bath_salts) & set(drug_names))

# alcohol = ['alcohol', 'booze', 'sauce', 'hooch', 'juice']

clonidine = ['clonidine']

antidepressants = ['zoloft', 'prozac'] 

naltrexone = ['vivitrol', 'naltrexone']

buprenorphine = ['buprenorphine', 'naloxone', 'suboxone', 'subutex']

dmt = ['dmt', 'dmt','nn-dmt', 'dimethyltryptamine', 'changa']

two_cb = ['2c-b', 'cornetto', '2-cb', '2cb', '2C', 'hcl', 'hydrochloride salt',  'tusi']

others = ['viagra', 'sildenafil', 'modafinil', 'tadaga', 'kamagra', 'vicodin', 'tramadol', 'lidocaine', 'hydrochloride salt', 'testosterone', 'trenbolone', 'clomid', 'dbol', 'duromine', 'amoxicillin', 'azithromycin', 'lyrica','cialis', 'levitra', 'zolpidem', 'boldenone', 'divinorum', 'mxe', 'tamoxifen', 'moclobemide', 'amlodipine', 'ramipril', 'dapoxetine', 'gabapentin', 'benzocaine', 'vidalista', 'dexamfetamine', 'hydroxyzine', 'ondansetron', 'phenobarbital', 'dnp', 'anastrozole', 'armodafinil', 'propofol', '?Viagra+Cialis', 'soma', 'TAPENTADOL', 'Syntholan Sustanon', 'nbome', 'Cytotec', 'Clindamycin', 'Ampicillin', 'NBOH', 'Levofloxacin', 'Clenbuterol', 'Ephedrine Hydrochloride', 'Testesterone', 'viagra+cialis+levitra']

not_drugs = ['credit', 'debit','license','licence', 'card','cards','carding', 'cc','ccs', 'ccv','cvv','cvvs', 'hack','hacked','hacking', 'ssn', 'counterfeit', 'account','accounts', 'passport','passports',
'porn', 'porno', 'profile','profiles', 'template','templates', 'paypal', 'login','logins', 'bank', 'moneygram',
'instagram','instagrams','followers', 'tipjar', 'tip jar', 'tip box', 'phone','mobile','fraud','amazon','cash', 'cashout', 'checks', 'background', 'computer','atm','hbo','virus','windows','visa', 'xbox' ,'fullz','dumps', 'android', 'scotiabank', 'cookbook', 'girlfriend', 'onion', 'surprise', 'combined delivery', 'balance', 'balances', 'make money', 'making money', 'ssndob', 'tip', 'tips', 'tipping', 'pin', 'bins', 'full information', 'full info', 'pay pal', 'pay stub', 'software', 'security', 'proxies', 'vhq', 'vpn', 'cpn', 'fake id', 'COUNTERFEITS', 'socks', 'socks5', 'how to', 'stealer', 'generator', 'non vbv', 'cardable', 'carded', 'scans', 'hacker', 'randsomware', 'tutorial', 'kit', 'shares', 'subs', 'bankdrop', 'website', 'make $', 'business', 'fulls', 'fullz', 'stripe', 'hulu', 'guide', 'Thanks for your generosity,']


# Rank addiction potential based on DEA Drug Schedules
# high_potential = set(['cocaine', 'benzodiazepines', 'heroin', 'lsd', 'mescaline', 
# 				'pcp', 'marijuana', 'ecstasy', 'khat', 'kratom', 'methamphetamine',
# 				'codeine', 'fentanyl', 'hydromorphone', 'meperidine', 'methadone', 
# 				'morphine', 'oxycodone', 'oxymorphone', 'amphetamine', 'methylphenidate'])
# medium_potential = set(['ketamine', 'inhalants', 'alcohol', 'buprenorphine'])
# low_potential = set(['psilocybin', 'hashish', 'over_counter', 'clonidine', 'naltrexone', 'antidepressants'])


def get_recovery_drugs(include_street_names=False):
	recovery_drugs = set(['buprenorphine', 'benzodiazepines', 'naltrexone', 'antidepressants', 'clonidine', 'methadone'])
	if not include_street_names:
		return recovery_drugs

	drugs_dict = get_drugs_dict()
	all_names = set()
	for name in recovery_drugs:
		all_names |= (set([name]) | set(drugs_dict[name]))

	return all_names

def get_danger_drugs(include_street_names=False):
	drugs_dict = get_drugs_dict()
	if include_street_names:
		all_recovery_drugs = get_recovery_drugs(include_street_names=True)
		all_drugs = get_all_names(drugs_dict.keys())
		return set(all_drugs) - set(all_recovery_drugs)
	else:
		recovery_drugs = get_recovery_drugs()
		return set(drugs_dict.keys()) - set(recovery_drugs)

def get_addiction_potential_lists():
	return low_potential, medium_potential, high_potential

def get_all_names(official_names):
	drugs_dict = get_drugs_dict()
	all_names = set()
	for name in official_names:
		all_names |= set(drugs_dict[name])
	return all_names

def get_drugs_dict():
	# creating lookup table: 
	drugs_dict = {'cocaine': cocaine,
				'benzodiazepines': benzodiazepines,
				 'heroin': heroin,
				'ketamine': ketamine, 
				'lsd': lsd, 
				'mescaline': mescaline,
				'pcp': pcp, 
				'marijuana': marijuana,
				'psilocybin': psilocybin,
				'ecstasy': ecstasy, 
				'inhalants': inhalants, 
				'khat': khat, 
				'kratom': kratom, 
				'hashish': hashish, 
				'methamphetamine': methamphetamine,
				'codeine': codeine,
				'fentanyl': fentanyl,
				'hydromorphone': hydromorphone,
				'meperidine': meperidine, 
				'methadone':methadone, 
				'morphine': morphine,
				'oxycodone': oxycodone, 
				'oxymorphone': oxymorphone, 
				'amphetamine': amphetamine, 
				'methylphenidate': methylphenidate,
				'naltrexone': naltrexone, 
				'buprenorphine': buprenorphine,
				'clonidine': clonidine,
				'antidepressants': antidepressants,
				'dmt': dmt,
				'two_cb': two_cb,
                'others': others,
                'not_drugs': not_drugs  
                 }
	return drugs_dict


def get_drugs_list():
	all_drugs = set()
	DRUGS_DICT = get_drugs_dict()
	for official_name in DRUGS_DICT:
		all_drugs |= (set([official_name]) | set(DRUGS_DICT[official_name]))

	return all_drugs


def get_support_groups():
	return ['12-step',
		  '12 step',
		  'Alcoholics Anonymous',
		  'AA',
		  'Heroin Anonymous',
		  'HA',
		  'Cocaine Anonymous',
		  'CA',
		  'Crystal Meth Anonymous',
		  'CMA',
		  'Narcotics Anonymous',
		  'NA',
		  'Secular Organizations for Sobriety',
		  'SOS',
		  'Rational Recovery',
		  'RR',
		  'Self Management and Recovery Training',
		  'SMART']

def get_drug_counts(texts):
	DRUGS_DICT = get_drugs_dict()
	counts = defaultdict(int)
	for text in texts: 
		for official_name in DRUGS_DICT.keys():
			count = 0
			# Compile a reg. exp.
			# drug_re = re.compile(r'{}'.format([]), flags=re.IGNORECASE)
			street_names = DRUGS_DICT[official_name]
			drug_re = re.compile(r'\b(?:%s)\b' % '|'.join([official_name]+street_names), flags=re.I)    
			counts[official_name] += len(list(drug_re.finditer(text)))
	return counts
