from django.shortcuts import render, redirect
from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

from .models import Product
from .charts import getCharts
from .forms import UploadFileForm

from json import dumps
import csv

from datetime import datetime
from .models import *
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima import auto_arima

#from neuralprophet import NeuralProphet


def index(request):
  charts = getCharts()

  context = {
    'segment'  : 'index',
    'charts': charts,
    'chartsJSON': dumps(charts),
  }
  return render(request, "pages/index.html", context)

def processar_arquivo_csv(request):
  if request.method == 'POST':
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
      arquivo = request.FILES['file'].read().decode('utf-8').splitlines()
      reader = csv.DictReader(arquivo)
            
      # Processar o arquivo CSV e adicionar os dados ao banco de dados
      for row in reader:
        # Format the date as per the "YYYY-MM-DD" format
        formatted_order_date = datetime.datetime.strptime(row['Order Date'], "%m/%d/%Y").strftime("%Y-%m-%d")
        formatted_ship_date = datetime.datetime.strptime(row['Ship Date'], "%m/%d/%Y").strftime("%Y-%m-%d")

        # Ajuste os campos conforme o seu modelo
        Product.objects.create(
          Row_ID        = row['Row ID'],
          Order_ID      = row['Order ID'],
          Order_Date    = formatted_order_date,
          Ship_Date     = formatted_ship_date,
          Ship_Mode     = row['Ship Mode'],
          Customer_ID   = row['Customer ID'],
          Customer_Name = row['Customer Name'],
          Segment       = row['Segment'],
          Country       = row['Country'],
          City          = row['City'],
          State         = row['State'],
          Postal_Code   = row['Postal Code'],
          Region        = row['Region'],
          Product_ID    = row['Product ID'],
          Category      = row['Category'],
          Sub_Category  = row['Sub-Category'],
          Product_Name  = row['Product Name'],
          Sales         = row['Sales'],
          Quantity      = row['Quantity'],
          Discount      = row['Discount'],
          Profit        = row['Profit'],
        )
            
      return redirect('index')  # Redirecione para uma página de sucesso após o processamento

  else:
    form = UploadFileForm()

  return render(request, 'pages/dynamic-tables.html', {'form': form, 'segment': 'tables'})

def result(request, product, months):
  # monta dicionario com informações Sales e Order date do produto especificado
  product_dic = getProducts(product) 
  # faz a previsão de preços do produto especificado na quantidade de meses especificada
  resultado = calculate_SARIMAX(product_dic, months)

  passado = []
  for var1, var2 in zip(resultado['observadox'], resultado['observadoy']):
    passado.append({
      "mes": var1,
      "previsto": var2,
      "observado": var2,
    })    
  futuro = []
  for var1, var2 in zip(resultado['previstox'], resultado['previstoy']):
    futuro.append({
      "mes": var1,
      "previsto": var2,
    })    

  charts = [{
    'id': 'sarimax',
    'label': 'SARIMAX',
    'passado': passado,
    'futuro': futuro,
  }]
  
  # variaveis para passar ao grafico
  context = {
    'segment': 'index',
    'charts': charts,
    'chartsJSON': dumps(charts),
  }
  
  return render(request, "pages/index.html", context)


def calculate_ARIMA(data, months):
  df = pd.DataFrame.from_dict(data)

  df['Sales'] = df['Sales'].str.replace(',', '.', regex=True)
  df['Discount'] = df['Discount'].str.replace(',', '.', regex=True)
  df['Profit'] = df['Profit'].str.replace(',', '.', regex=True)

  df = df[['Order Date', 'Sales']]
  df['Order Date'] = pd.to_datetime(df['Order Date'])
  # Converta a coluna 'Sales' para o tipo numérico
  df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
  df = df.set_index('Order Date')
  df_monthly = df.resample('M').sum()
  # Verifique se há valores ausentes
  if df_monthly['Sales'].isnull().any():
    print("Existem valores ausentes na coluna 'Sales'. Trate-os antes de prosseguir.")
  
  else:
    # Ajuste do modelo ARIMA
    model_arima = auto_arima(df_monthly['Sales'], trace=True, error_action='ignore', suppress_warnings=True, seasonal=False)
    arima_order = model_arima.order

    # Ajuste o modelo ARIMA com os parâmetros encontrados
    model = ARIMA(df_monthly['Sales'], order=arima_order)
    fit_arima = model.fit()

    # Faça previsões para os próximos N meses
    forecast_arima = fit_arima.get_forecast(steps=months)
    forecast_arima_ci = forecast_arima.conf_int()

    return {'before': df_monthly['Sales'], 'predicted':forecast_arima.predicted_mean, 'error':(forecast_arima_ci.iloc[:, 0], forecast_arima_ci.iloc[:, 1])}


def calculate_SARIMAX(data, months):
  df = pd.DataFrame.from_dict(data)

  df['Order date'] = list(map(str, df['Order date']))

  df['Sales'] = pd.Series(df['Sales'])
  df['Order date'] = pd.Series(df['Order date'])

  df['Sales'] = df['Sales'].str.replace(',', '.', regex=True)

  #df['Sales'] = list(map(lambda x : x.replace(',', '.'), df['Sales']))

  df = df[['Order date', 'Sales']]
  df['Order date'] = pd.to_datetime(df['Order date'])
  # Converta a coluna 'Sales' para o tipo numérico
  df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
  df = df.set_index('Order date')
  df_monthly = df.resample('M').sum()
  # Verifique se há valores ausentes
  if df_monthly['Sales'].isnull().any():
    print("Existem valores ausentes na coluna 'Sales'. Trate-os antes de prosseguir.")

  else:
    # Ajuste do modelo SARIMAX
    model_sarimax = auto_arima(df_monthly['Sales'], trace=True, error_action='ignore', suppress_warnings=True, seasonal=True, m=12)
    sarimax_order = model_sarimax.order
    sarimax_seasonal_order = model_sarimax.seasonal_order

    # Ajuste o modelo SARIMAX com os parâmetros encontrados
    model = SARIMAX(df_monthly['Sales'], order=sarimax_order, seasonal_order=sarimax_seasonal_order)
    fit_sarimax = model.fit()

    # Faça previsões para os próximos N meses
    forecast_sarimax = fit_sarimax.get_forecast(steps=months)
    forecast_sarimax_ci = forecast_sarimax.conf_int()

    return {'observadox': map(str, (df_monthly['Sales'].keys())), 'observadoy': (df_monthly['Sales']), 'previstox': list(map(str, (forecast_sarimax.predicted_mean.keys()))), 'previstoy': list(forecast_sarimax.predicted_mean), 'error':(forecast_sarimax_ci.iloc[:, 0], forecast_sarimax_ci.iloc[:, 1])}

def getProducts(product_name):
  # Dicionario com as informações que seram retornadas 
  products_dic = {'Sales': [], 'Order date': []}

  if product_name == 'ALL':
    # se a palavra pesquisada for ALL todos os produtos são usados
    products_list = Product.objects.all()
  else:
    # obtem Produtos no baco de dados com o mesmo nome 
    products_list = Product.objects.filter(Product_Name=product_name)
    
  # itera por cada produto adicionando no dicionario sua informação de Sales e Order date
  for product in products_list:
    products_dic['Sales'].append(product.Sales)
    products_dic['Order date'].append(product.Order_Date)
  
  # retorna o dicionario para ser passado a função que fara a previsão
  return products_dic 

def calculate_Prophet(data, months):
  #converte o dicionario para um data frame
  df = pd.DataFrame.from_dict(data)
  # Substitua as vírgulas por pontos na coluna 'Sales'
  df['Sales'] = df['Sales'].str.replace(',', '.', regex=True)
  # Converta 'Order date' para formato de data
  df['Order date'] = pd.to_datetime(df['Order date'])
  # Selecione as colunas relevantes (por exemplo, 'Order date' e 'Sales')
  df = df[['Order date', 'Sales']]
  # Converta a coluna 'Sales' para o tipo numérico
  df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
  # Defina 'Order date' como índice
  df = df.set_index('Order date')
  # Agrupe as vendas por mês e some os valores
  df_monthly = df.resample('M').sum()

  # Criar um DataFrame com as colunas 'ds' (data) e 'y' (vendas)
  df_prophet = pd.DataFrame({'ds': df_monthly.index, 'y': df_monthly['Sales']})
  # Criar e treinar o modelo Neural Prophet
  model = NeuralProphet(yearly_seasonality=True, weekly_seasonality=True)
  model.fit(df_prophet)
  # Criar um DataFrame com datas futuras para fazer previsões
  future = model.make_future_dataframe(df_prophet, periods=months)
  # Fazer previsões para os próximos 12 meses
  forecast = model.predict(future)

  return {'observadox':df_prophet['ds'], 'observadoy':df_prophet['y'], 'previstox':forecast['ds'], 'previstoy':forecast['yhat1'],}
