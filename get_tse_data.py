"""Script to get the elections data from the TSE website."""
import pandas as pd
import datetime
import altair as alt
import time


class TSEData:
    def __init__(self, state, city):
        self.state = state
        self.city = city
        self.url = "https://resultados.tse.jus.br/oficial/ele2022/544/dados-simplificados/br/br-c0001-e000544-r.json"
        self.df_total = pd.read_csv("election_data.csv")
        self.get_data()
        self.meta = []

    def get_data(self):
        """Get the data from the TSE website."""
        sorce = self.url
        self.data = pd.read_json(sorce)
        nome = []
        votos = []
        hora = []
        apurado = []
        for candidato in range(len(self.data)):

            nome.append(self.data["cand"][candidato]["nm"])
            votos.append(float(self.data["cand"][candidato]["pvap"].replace(",", ".")))
            apurado.append(float(self.data["pst"][0].replace(",", ".")))
            hora.append(self.data["hg"][0])

        self.df_temp = pd.DataFrame(
            {"nome": nome, "votos": votos, "hora": hora, "apurado": apurado}
        )
        self.df_temp["proporcao"] = self.df_temp["votos"] * self.df_temp["apurado"]
        self.df_total = pd.concat([self.df_total, self.df_temp], ignore_index=True)
        self.df_total.to_csv("election_data.csv", index=False)


while True:
    time.sleep(30)
    teste = TSEData("SP", "São Paulo")
    teste.df_total["hora"] = pd.to_datetime(teste.df_total["hora"])

    teste_chart = teste.df_total[teste.df_total["hora"] >= "18:25"]
    teste_chart.query("nome == 'JAIR BOLSONARO' or nome == 'LULA'", inplace=True)

    df_chart = (
        (
            alt.Chart(teste_chart)
            .mark_area(opacity=0.7)
            .encode(
                alt.X("hora:T"),
                alt.Y("proporcao:Q", stack=None, axis=None),
                alt.Color("nome:N"),
            )
        )
        .configure_range(category=["green", "red"])
        .properties(width=800, height=400)
    )

    df_chart.save("teste.html")
