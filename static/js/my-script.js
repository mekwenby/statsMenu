function validateForm(romas) {
    var roma = document.getElementById("roma").value;

    if (roma === romas) {

        location.reload();
        return false;
    }

    // 在这里执行其他验证或处理逻辑

    alert("错误。" + romas);
    return true;
}

window.onload = function () {
    document.getElementById("roma").focus();
};

function updateTime() {
    var now = new Date();
    var hours = now.getHours();
    var minutes = now.getMinutes();
    var seconds = now.getSeconds();
    document.getElementById('time').innerHTML = hours + ':' + minutes + ':' + seconds;
    var today = new Date();
    var date = today.getDate();
    var month = today.getMonth() + 1;
    var year = today.getFullYear();
    var dayOfWeek = today.getDay(); // 0代表星期日，1代表星期一，以此类推
    var daysOfWeek = ["日", "一", "二", "三", "四", "五", "六"];
    document.getElementById('date').innerHTML = year + '年' + month + '月' + date + '日' + '&nbsp;&nbsp;' + '星期' + daysOfWeek[dayOfWeek];
}

setInterval(updateTime, 1000);


function mywordForm() {
    // 获取表单字段
    var text = document.forms[0].elements["text"].value;
    var translation = document.forms[0].elements["translation"].value;
    var classify = document.forms[0].elements["classify"].value;

    // 验证字段是否为空
    if (text === '' || kana === '' || translation === '' || classify === '') {
        alert("请填写完整的表单");
        return false; // 阻止表单提交
    }

    return true; // 允许表单提交
}