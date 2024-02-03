

import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn import model_selection






models = ['Arteon', 'Golf', 'Série 3', 'T-Roc', 'Zoe', 'Mazda 2', 'C-HR', 'Punto', 'A1', 'Mazda 3', 'C4', 'Puma', 'Arkana', '500', 'SpaceTourer', 'Tucson', 'Megane', 'Sandero', 'Focus', '5008', 'Karoq', 'Twingo', 'Leon', 'Golf Sportsvan', '508', 'Kadjar', 'Rio', 'Koleos', 'DS 7', 'Polo', 'Crossland X', 'Ibiza', 'Qashqai', 'C3', 'Grandland X', 'Clio', 'C5', '308', '1007', 'GS', 'Mazda 5', 'Passat', 'Vitara', 'A5', '207', 'Corsa', 'CX-5', 'MiTo', 'T-Cross', 'Mokka', 'Autre', 'Trafic Combi', 'DS 3', 'Grand Cherokee', '3008', 'Countryman', 'Matiz', 'Duster', 'C1', 'Talisman', 'TT', '2008', 'Q5', 'Autres', 'Kangoo', 'Captur', 'DS 4', 'C3 Aircross', 'Range Rover', 'C-MAX', 'MX-3', 'MX-5', 'Swift', 'C4 Picasso', 'XC60', 'Renegade', 'X1', '208', 'Grand C-MAX', 'Jumpy Fg', 'Jazz', 'Tiguan', 'CX-30', 'Rifter', 'Giulietta', 'Explorer', 'Touran', 'Micra', 'Scenic', 'Tipo', 'Giulia']
colors = ['Blanc','Gris','Noir','Vert','Bleu','Beige','Rouge','Marron','Argent','Jaune','Orange','Autre']
fuel = ['Diesel','Essence','Hybride','Electrique']
gearbox = ['Automatique','Manuelle']
brands = ['HONDA', 'LAND-ROVER', 'BMW', 'CHEVROLET', 'VOLKSWAGEN', 'CITROEN', 'MINI', 'HYUNDAI', 'MAZDA', 'DACIA', 'SEAT', 'FORD', 'LEXUS', 'AUDI', 'DS', 'ALFA ROMEO', 'FIAT', 'JEEP', 'PEUGEOT', 'SKODA', 'TOYOTA', 'NISSAN', 'OPEL', 'RENAULT', 'ABARTH', 'VOLVO', 'KIA', 'SUZUKI']

def normalise(array):
    mini = min(array)
    maxi = max(array)
    return((array-mini)/(maxi-mini))

def kNN(voitures1,note):
    X = np.zeros((len(note),7))
    Xpredi = np.zeros((len(voitures1),7))
    y = np.zeros(len(note))

    for i in range(len(note)):
        voiture,val = note[i]
        y[i] = val 
        X[i][0]=brands.index(voiture['brand'])
        X[i][1]=voiture['price']
        X[i][2]=models.index(voiture['model'])
        X[i][3]=voiture['km']
        X[i][4]=fuel.index(voiture['fuel'])
        X[i][5]=gearbox.index(voiture['gearbox'])
        X[i][6]=colors.index(voiture['color'])
        X[i] = normalise(X[i])
        
        
    
    param_grid = {'n_neighbors':[5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,25]}


# Créer un classifieur kNN avec recherche d'hyperparamètre par validation croisée
    clf = model_selection.GridSearchCV(
        KNeighborsRegressor(), # un classifieur kNN
        param_grid,     # hyperparamètres à tester
        cv=3,           # nombre de folds de validation croisée
     
)
# Optimiser ce classifieur sur le jeu d'entraînement
    clf.fit(X, y)
    nb_neighbors = clf.best_params_['n_neighbors']
    

    model = KNeighborsRegressor(nb_neighbors,weights='uniform')
    model.fit(X,y)

    for i in range(len(voitures1)):
         
        Xpredi[i][0]=brands.index(voitures1[i]['brand'])
        Xpredi[i][1]=voitures1[i]['price']
        Xpredi[i][2]=models.index(voitures1[i]['model'])
        Xpredi[i][3]=voitures1[i]['km']
        Xpredi[i][4]=fuel.index(voitures1[i]['fuel'])
        Xpredi[i][5]=gearbox.index(voitures1[i]['gearbox'])
        Xpredi[i][6]=colors.index(voitures1[i]['color'])
        Xpredi[i] = normalise(Xpredi[i])
        

    result = model.predict(Xpredi)
    
    

    return result