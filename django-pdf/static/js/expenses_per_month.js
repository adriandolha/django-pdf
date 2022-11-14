


const createExpensesChart = (chartId, chartTitle, chartData) => {
  const CHART_COLORS = {
    red: 'rgb(255, 99, 132)',
    orange: 'rgb(255, 159, 64)',
    yellow: 'rgb(255, 205, 86)',
    green: 'rgb(75, 192, 192)',
    blue: 'rgb(54, 162, 235)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(201, 203, 207)'
  };
  const CHART_COLORS_LIST = [
    'rgb(255, 99, 132)',
    'rgb(75, 192, 192)',
    'rgb(54, 162, 235)',
    'rgb(255, 159, 64)',
    'rgb(255, 205, 86)',
    'rgb(153, 102, 255)',
    'rgb(201, 203, 207)'
  ];
  console.log(chartData);
  const _items = chartData.items
  const _countries = _items.map(item => `${item[0]}`)
  let countries = [...new Set(_countries)];
  const _labels = _items.filter(item => item[0] === countries[0]).map(item => `${item[1]}-${item[2]}`)
  console.log(countries)
  console.log(_labels)

  const _datasets = countries.map((country, index) => {
    return {
      label: country,
      data: _items.filter(item => item[0] === country).map(item => `${item[3]}`),
      borderColor: CHART_COLORS_LIST[index],
      backgroundColor: CHART_COLORS_LIST[index],
      yAxisID: country,
    }
  })
  console.log(_datasets)
  
  const data = {
    labels: _labels,
    datasets: _datasets
  };
  const config = {
    type: 'line',
    data: data,
    options: {
      // responsive: true,
      // maintainAspectRatio: false,

      stacked: false,
      plugins: {
        title: {
          display: true,
          text: chartTitle
        }
      },
      scales: {
        y: {
          type: 'linear',
          display: true,
          position: 'left',
        },
        y1: {
          type: 'linear',
          display: true,
          position: 'right',

          // grid line settings
          grid: {
            drawOnChartArea: false, // only want the grid lines for one axis to show up
          },
        },
      }
    },
  };
  const chart = new Chart(
    document.getElementById(chartId),
    config
  );
}