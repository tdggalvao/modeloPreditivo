def getCharts():
  return [
    {
      'id': 'arima',
      'label': 'ARIMA',
      'passado': [
        { 'mes': '06/23', 'observado': 20 },
        { 'mes': '07/23', 'observado': 55 },
        { 'mes': '08/23', 'observado': 45 },
        { 'mes': '09/23', 'observado': 75 },
      ],
      'futuro': [
        { 'mes': '10/23', 'previsto': 50, 'superior': 55, 'inferior': 45 },
        { 'mes': '11/23', 'previsto': 75, 'superior': 80, 'inferior': 70 },
        { 'mes': '12/23', 'previsto': 90, 'superior': 100, 'inferior': 80 },
      ]
    }
  ]
