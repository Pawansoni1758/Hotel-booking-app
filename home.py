import pandas as pd
from fpdf import FPDF

df = pd.read_csv("articles.csv", dtype={'id': str})


class Article:

    def __init__(self, article_id):
        self.id = article_id
        self.name = df.loc[df['id'] == self.id, 'id'].squeeze()
        self.price = df.loc[df['id'] == self.id, 'price'].squeeze()

    def available(self):
        in_stock = df.loc[df['id'] == self.id, 'in stock'].squeeze()
        return in_stock


class Receipt:

    def __init__(self, article):
        self.article = article

    def generate(self):
        pdf = FPDF(orientation="p", unit="mm", format="A4")
        pdf.add_page()
        pdf.set_font(family="Times", style="B", size=16)
        pdf.cell(w=50, h=8, txt=f"Recept nr.{self.article.id}", align="L")
        pdf.ln()
        pdf.set_font(family="Times", style="B", size=16)
        pdf.cell(w=50, h=8, txt=f"Article name:{self.article.name}", align="L")
        pdf.ln()
        pdf.set_font(family="Times", style="B", size=16)
        pdf.cell(w=50, h=8, txt=f"Price:{self.article.price}", align="L")
        pdf.ln()
        pdf.output("invoice.pdf")


print(df)
stock_id = input("Choose an article to buy: ")
article = Article(stock_id)
if article.available():
    receipt = Receipt(article)
    receipt.generate()
else:
    print("No such article in stock")
