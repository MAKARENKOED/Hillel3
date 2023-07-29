import pandas

df = pandas.read_csv('output.csv')

df = df.drop('Возраст', axis=1)

df.to_excel('output.xlsx', index=False)
