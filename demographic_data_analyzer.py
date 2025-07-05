import pandas as pd

def calculate_demographic_data():
    # Noms des colonnes (le fichier original n'a pas d'en-têtes)
    columns = [
        'age', 'workclass', 'fnlwgt', 'education', 'education-num',
        'marital-status', 'occupation', 'relationship', 'race', 'sex',
        'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'salary'
    ]
    
    # Lire le fichier CSV
    df = pd.read_csv('adulte.data.csv', header=None, names=columns)

    # 1. Nombre de personnes par race
    race_count = df['race'].value_counts()

    # 2. Âge moyen des hommes
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)

    # 3. Pourcentage de diplômés de Bachelor
    percentage_bachelors = round(
        (df['education'] == 'Bachelors').mean() * 100, 1
    )

    # 4. Pourcentage de diplômés supérieurs gagnant >50K
    higher_education = df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])
    higher_education_rich = round(
        (df[higher_education]['salary'] == '>50K').mean() * 100, 1
    ) if higher_education.sum() > 0 else 0.0

    # 5. Pourcentage de non-diplômés supérieurs gagnant >50K
    lower_education_rich = round(
        (df[~higher_education]['salary'] == '>50K').mean() * 100, 1
    ) if (~higher_education).sum() > 0 else 0.0

    # 6. Nombre minimal d'heures travaillées par semaine
    min_work_hours = df['hours-per-week'].min()

    # 7. Pourcentage de travailleurs à temps minimal gagnant >50K
    num_min_workers = (df['hours-per-week'] == min_work_hours).sum()
    rich_percentage = round(
        (df[df['hours-per-week'] == min_work_hours]['salary'] == '>50K').mean() * 100, 1
    ) if num_min_workers > 0 else 0.0

    # 8. Pays avec le plus haut pourcentage de riches (>50K)
    rich_by_country = df[df['salary'] == '>50K']['native-country'].value_counts()
    total_by_country = df['native-country'].value_counts()
    
    country_stats = (rich_by_country / total_by_country * 100).dropna()
    
    if not country_stats.empty:
        highest_earning_country = country_stats.idxmax()
        highest_earning_country_percentage = round(country_stats.max(), 1)
    else:
        highest_earning_country = "None"
        highest_earning_country_percentage = 0.0

    # 9. Profession la plus populaire en Inde parmi les riches
    india_rich = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]
    if not india_rich.empty:
        top_IN_occupation = india_rich['occupation'].value_counts().idxmax()
    else:
        top_IN_occupation = "None"

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage': highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }

# Pour tester

if __name__ == '__main__':
    data = calculate_demographic_data()

    print("\n📊 Résumé démographique (affichage tabulaire) :\n")

    print("+----------------------------------------------+----------------------------+")
    print("| Statistique                                  | Valeur                     |")
    print("+----------------------------------------------+----------------------------+")
    print(f"| Nombre moyen d'âge des hommes                | {str(data['average_age_men']).ljust(26)}|")
    print(f"| % de personnes avec un diplôme 'Bachelors'   | {str(data['percentage_bachelors']) + ' %':<26}|")
    print(f"| % diplômés supérieurs gagnant >50K           | {str(data['higher_education_rich']) + ' %':<26}|")
    print(f"| % non diplômés supérieurs gagnant >50K       | {str(data['lower_education_rich']) + ' %':<26}|")
    print(f"| Heures de travail minimales par semaine      | {str(data['min_work_hours']).ljust(26)}|")
    print(f"| % de riches parmi ceux qui bossent peu       | {str(data['rich_percentage']) + ' %':<26}|")
    print(f"| Pays avec le + de riches (>50K)              | {data['highest_earning_country']:<26}|")
    print(f"| % de riches dans ce pays                     | {str(data['highest_earning_country_percentage']) + ' %':<26}|")
    print(f"| Métier le + populaire en Inde (>50K)         | {data['top_IN_occupation']:<26}|")
    print("+----------------------------------------------+----------------------------+")

    # Affichage du nombre de personnes par race
    print("\n📊Répartition par race :\n")
    print("+----------------------------+------------+")
    print("| Race                      | Nombre     |")
    print("+----------------------------+------------+")
    for race, count in data['race_count'].items():
        print(f"| {race.ljust(26)} | {str(count).ljust(10)} |")
    print("+----------------------------+------------+")
