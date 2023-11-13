from flask import Flask, render_template, redirect, request
import ssl
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
ssl_context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

app = Flask(__name__)
@app.route("/")
def main():   
    return render_template("home.html")

@app.route("/contato")
def contato():
    return render_template ("contato.html")

@app.route("/valuation")
def valuation():
    return render_template ("valuation.html")

@app.route("/loan")
def loan():
    salario = float(request.args.get('salario', '0.0'))
    return render_template ("loanbank.html",salario=salario)

@app.route("/applyloan", methods=['POST'])
def applyloan():
    salario = float(request.form['salario'])
    valor_emprestimo = float(request.form['valor_emprestimo'])
    prazo= int(request.form['prazo'])
    if (salario < 1200):
        return render_template("notapprove.html")
    maxemprestimo = 24*(0.6*salario)
    if (valor_emprestimo>maxemprestimo):
        return render_template('threshold.html', maxemprestimo=format_currency(maxemprestimo))
    if (prazo>24):
        return 'Prazo muito alto'
    prazominimo =  int(valor_emprestimo/(0.6*salario))
    print(prazominimo)
    if (prazo<prazominimo):
        return render_template('shortterm.html',prazominimo=prazominimo)
    valor_parcela, custo_total = calcular_emprestimo(valor_emprestimo,prazo)
    if (valor_parcela<100):
        return render_template('installment.html')
    return render_template("agreement.html",
                           valor_emprestimo=format_currency(valor_emprestimo),
                           valor_parcela=format_currency(valor_parcela),
                           custo_total=format_currency(custo_total),
                           prazo=prazo)
    #return f' parcelas : {str(valor_parcela)}, custo total financeiro= {str(custo_total)}'
    #return render_template("contrato.html",valor_emprestimo=valor_emprestimo, prazo=prazo)

def calcular_emprestimo (valor, prazo):
    juros=0.13/12
    #montante= capital x (1+juros/100/12) elevado ao quadrado de prazo em meses
    valor_total = valor * (1 + juros) ** prazo
    valor_parcela = valor_total / prazo
    custo_total = valor_total - valor

    return valor_parcela, custo_total

def format_currency(value):
    return "R$ {:,.2f}".format(value).replace(",", "X").replace(".", ",").replace("X", ".")

@app.route("/income", methods=['POST'])
def income():    
    input_text = float(request.form['salario'])
    if (input_text < 1200):
        return render_template("notapprove.html")
    else:
        maxemprestimo = 24*(0.6*input_text)        
        valor_maximo_formatado = format_currency(maxemprestimo)
        return render_template("approved.html",valor_maximo_formatado=valor_maximo_formatado, salario=input_text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
