
function get_city()
{
    // ссылка на select region
    var regionObj = document.getElementById("region");
    // ссылка на select city
    var cityObj = document.getElementById("city");
    // индекс выбраного региона
    var index = regionObj.options.selectedIndex;
    $.ajax({
        url: "/_get_city/",
        type: "POST",
        data: {'id': index},
        success: function (resp) {
            // массив городов из выбраного региона
            var arr = resp.data
            // заполняем строку для select
            // option ('название объекта', 'значение')
            for (var n = 0; n < arr.length; n++) {
                cityObj[n] = new Option(arr[n], arr[n]);
            }
        }
    });
}