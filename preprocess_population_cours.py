import pandas as pd
import matplotlib.pyplot as plt

"""
Ce script lit les donnees de statistiques canada 
de population des recensements 2021 et 2016
ainsi que la superficie des territoire recenses, 
dans le but de faire une analyse statistique sur les municipalites
"""

# importation des donnees brutes : index_col pour utiliser l'index fourni dans le fichier dans la premiere colonne
df = pd.read_csv('Census_2016_2021.csv', index_col=0)

print('Extrait des données traitées de recensements :\n')
print(df.head())
print('\n')

print('Résumé statistique des recensements :\n')
print(df.describe())
print('\n')

# Création d'une DataFrame qui regroupe uniquement les municipalités, c’est-à-dire dont le type est ’MÉ’.
df_municipalites = df[df['Type'] == 'MÉ'].reset_index(drop=True)

print('DataFrame regroupant uniquement les municipalités :\n')
print(df_municipalites.head())
print('\n')

# Affichez le nombre de municipalités
nombre_de_municipalites = df_municipalites['Nom'].count()
print("Le nombre de municipalités est de :", nombre_de_municipalites)
print('\n')

# Calculer et afficher la population moyenne dans les municipalités en 2016 et en 2021.
population_moyenne_2016 = df_municipalites['Pop16'].mean()
population_moyenne_2021 = df_municipalites['Pop21'].mean()

print("La population moyenne dans les municipalités en 2016 est de :", population_moyenne_2016)
print('\n')
print("La population moyenne dans les municipalités en 2021 est de :", population_moyenne_2021)
print('\n')

"""Tracé d'un nuage de points du pourcentage d’accroissement de la population de 2016 à
2021 en fonction de la population des municipalités en 2021"""
# Calculer le pourcentage d'accroissement de la population de 2016 à 2021
df_municipalites.loc[:, 'PctAcc'] = ((df_municipalites['Pop21'] - df_municipalites['Pop16'])
                                     / df_municipalites['Pop16']) * 100

# On classe avec ce champ > sort_values (classement par pourcentage d’accroissement)
df_municipalites_Acc = df_municipalites.sort_values('PctAcc', ascending=False)

print('DataFrame regroupant les municipalités par ordre décroissant de pourcentage d\'accroissement :\n')
print(df_municipalites_Acc)
print('\n')

# Tracer le nuage de points du pourcentage d’accroissement
plt.figure(1)
plt.scatter(df_municipalites_Acc['Pop21'], df_municipalites_Acc['PctAcc'], color='blue')
plt.title('Pourcentage d\'accroissement de la population entre 2016 et 2021')
plt.xlabel('Population en 2021')
plt.ylabel('Pourcentage d\'accroissement [%]')
plt.grid(True)
plt.show()

"""Classez les municipalités sen 5 catégories selon leur population en 2021 :"""
# Définir les limites des catégories d'âge
limites_categorie_ME = [0, 2_000, 10_000, 25_000, 100_000, float('inf')]

# Définir les étiquettes des catégories
etiquettes_categorie_ME = ['1', '2', '3', '4', '5']

# Créer une nouvelle colonne 'Catégorie' basée sur les catégories de population
df_municipalites.loc[:, 'Catégorie'] = pd.cut(df_municipalites['Pop21'], bins=limites_categorie_ME,
                                              labels=etiquettes_categorie_ME, right=False)

# On classe par ordre décroissant avec sort_values (classement par catégorie)
df_municipalites = df_municipalites.sort_values('Catégorie', ascending=False)

print("DataFrame regroupant les municipalités par ordre décroissant de catégories de population en 2021 :\n")
print(df_municipalites[['Nom', 'Pop21', 'Catégorie']])
print('\n')

"""Tracé d'un diagramme en barres horizontales du nombre de municipalités (ME) dans chaque catégories"""
# Compter le nombre de municipalités dans chaque catégorie
nbr_de_ME_par_categorie = df_municipalites['Catégorie'].value_counts()

# Tracer le diagramme en barres horizontales
plt.figure(2)
nbr_de_ME_par_categorie.plot(kind='barh', color='blue')
plt.title('Nombre de municipalités par catégorie selon la population en 2021')
plt.xlabel('Nombre de municipalités')
plt.ylabel('Catégorie')
plt.grid(axis='x')
plt.show()
