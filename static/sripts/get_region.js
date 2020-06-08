
function get_region()
{
    // ссылка на select region
    var regionObj = document.getElementById("region");
    // массив для вывода
    $.ajax({
        url: "/_get_region/",
        type: "POST",
        success: function(resp) {
            // массив регионов
            var arr = resp.data
            for (var n = 0; n < arr.length; n++){
                // заполняем строку для select
                // option ('название объекта', 'значение')
                regionObj[n+1] = new Option(arr[n], arr[n]);
            }
        }
    });
}