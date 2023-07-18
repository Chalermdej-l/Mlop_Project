import pandas as pd
import uuid 

def main():
    path = 'data/bank-additional-full.csv'
    df = pd.read_csv(path,sep=';')
    df['id']= df['age'].apply(lambda x: str(uuid.uuid1()))

    df.to_csv(path,index=False,sep=';')

if __name__ == "__main__":
    main()



