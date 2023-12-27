// 初始化空数组来保存最近的10条数据和时间戳
let cpuData = [];
let memData = [];
let timestamps = [];
const maxDataPoints = 25; // 最多保存10条数据

// 创建 Chart 实例
const ctx = document.getElementById('sysStatsChart').getContext('2d');
const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'CPU Usage',
                data: [],
                borderColor: 'red',
                fill: false
            },
            {
                label: 'Memory Usage',
                data: [],
                borderColor: 'blue',
                fill: false
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: {
                display: false // 隐藏横轴标签
            },
            y: {
                suggestedMin: 0,
                suggestedMax: 100 // 根据数据范围调整纵轴的显示范围
            }
        }
    }
});

// 定义定时器，每隔一秒获取数据并更新折线图
setInterval(function () {
    $.ajax({
        url: '/api/get_sys_stats',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            const cpuUsage = data.cpuusage.toFixed(2);
            const memUsage = data.memusage.toFixed(2);

            // 添加新数据到数组中，最多保存10条数据
            cpuData.push(cpuUsage);
            memData.push(memUsage);
            timestamps.push(new Date().toLocaleTimeString());

            if (cpuData.length > maxDataPoints) {
                cpuData.shift(); // 移除最旧的数据点
                memData.shift();
                timestamps.shift();
            }

            // 更新图表数据并重绘图表
            chart.data.labels = timestamps;
            chart.data.datasets[0].data = cpuData;
            chart.data.datasets[1].data = memData;
            chart.update();
        },
        error: function () {
            console.log('Failed to get system stats.');
        }
    });
}, 1000); // 间隔一秒调用一次接口并更新折线图