// Sensor chart containers
const temperatureContainer = document.getElementById('temperature').getContext('2d');
const pressureContainer = document.getElementById('pressure').getContext('2d');
const humidityContainer = document.getElementById('humidity').getContext('2d');
// sensor charts
var temperatureChart;
var pressureChart;
var humidityChart;
// image containers
var rgbImage = document.getElementById('rgb-image');
var objDetImage = document.getElementById('objdet-image');
var hyperspectralImage = document.getElementById('hyperspectral-image');

var socket = io();
socket.on('connect', () => {
    console.log('Connected');
});

socket.on('init-chart', (data) => {
    console.log(data)
    temperatureChart = createTemperatureChart(temperatureContainer, data[1], data[0]);
    pressureChart = createPressureChart(pressureContainer, data[2], data[0])
    humidityChart = createHumidityChart(humidityContainer, data[3], data[0])
})

socket.on('update-chart', (sensorData) => {
    temperatureChart.data.labels.push(sensorData[0]);
    temperatureChart.data.datasets[0].data.push(sensorData[1]);
    
    pressureChart.data.labels.push(sensorData[0]);
    pressureChart.data.datasets[0].data.push(sensorData[2]);
    
    humidityChart.data.labels.push(sensorData[0]);
    humidityChart.data.datasets[0].data.push(sensorData[3]);
    
    temperatureChart.update();
    pressureChart.update();
    humidityChart.update();
    socket.emit('update-current', sensorData)
});

socket.on('update-current', (mostCurrent) => {
    console.log('update current')
    currentTime = document.getElementById('current-time');
    currentTemp = document.getElementById('current-temp');
    currentHumidity = document.getElementById('current-humidity');
    currentPressure = document.getElementById('current-pressure');

    currentTime.innerHTML = mostCurrent[0];
    currentTemp.innerHTML = mostCurrent[1];
    currentHumidity.innerHTML = mostCurrent[2];
    currentPressure.innerHTML = mostCurrent[3];
})

socket.on('update-recent-images', (images) => {
    rgbImage.src = images[0];
    objDetImage.src = images[1];
    hyperspectralImage.src = images[2];
})

function handlePictureButton() {
    console.log('Button Pressed')
    socket.emit('take-picture')
}

setInterval(() => {
    socket.emit('update');
    console.log('update sent');
}, 1000); 


function createTemperatureChart(chartContainer, xaxis, yaxis) {
    if(temperatureChart) {
        temperatureChart.destroy();
    }
    return new Chart( chartContainer, {
        type: 'line',
        data: {
            labels: yaxis, // Time series data
            datasets: [{
                label: 'temperature',
                data: xaxis // Temperature data
            }]
        },
        options: {
            responsive: false,
            maintainAspectRatio: true,
            elements: {
                point: {
                    pointStyle: false
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                title:{
                    display: true,
                    text: 'Temperature',
                }
            },
            scales: {
                x: {
                    ticks: {
                        display: false
                    }
                }
            }
        }
    });
}
function createPressureChart(chartContainer, xaxis, yaxis) {
    if(pressureChart) {
        pressureChart.destroy();
    }
    return new Chart( chartContainer, {
        type: 'line',
        data: {
            labels: yaxis, // Time series data
            datasets: [{
                label: 'Pressure',
                data: xaxis // Pressure data
            }]
        },
        options: {
            responsive: false,
            maintainAspectRatio: true,
            elements: {
                point: {
                    pointStyle: false
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                title:{
                    display: true,
                    text: 'Pressure'
                }
            },
            scales: {
                x: {
                    ticks: {
                        display: false
                    }
                }
            }
        }
    });
}
function createHumidityChart(chartContainer, xaxis, yaxis) {
    if(humidityChart) {
        humidityChart.destroy();
    }
    return new Chart( chartContainer, {
        type: 'line',
        data: {
            labels: yaxis, // Time series data
            datasets: [{
                label: 'Humidity',
                data: xaxis // Humidity data
            }]
        },
        options: {
            responsive: false,
            maintainAspectRatio: true,
            elements: {
                point: {
                    pointStyle: false
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                title:{
                    display: true,
                    text: 'Humidity'
                }
            },
            scales: {
                x: {
                    ticks: {
                        display: false
                    }
                }
            }
        }
    });
}