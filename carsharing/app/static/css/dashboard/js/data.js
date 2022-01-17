
        $(document).ready(function () {
            showGraph1();
        });


        function showGraph1()
        {
            {
                $.post("weeklydata.php",
                function (data)
                {
                    //console.log(data);
                     var day = [];
                    var sales = [];

                    for (var i in data) {
                        day.push(data[i].day);
                        sales.push(data[i].sales);
                    }

                    var chartdata1 = {
                        labels: day,
                        datasets: [
                            {
                                label: 'sales',
                                backgroundColor: '#49e2ff',
                                borderColor: '#46d5f1',
                                hoverBackgroundColor: '#CCCCCC',
                                hoverBorderColor: '#666666',
                                strokeColor: "#22A7F0",
                                animationEnabled: true,
                                data: sales
                            }
                        ]
                    };

                    var graphTarget = $("#graphCanvas1");

                    var barGraph = new Chart(graphTarget, {
                        type: 'line',
                        data: chartdata1
                    });
                });
            }
        }
      
      
        $(document).ready(function () {
            showGraph();
        });


        function showGraph()
        {
            {
                $.post("monthlydata.php",
                function (data)
                {
                    //console.log(data);
                     var month = [];
                    var sales = [];

                    for (var i in data) {
                        month.push(data[i].month);
                        sales.push(data[i].sales);
                    }

                    var chartdata = {
                        labels: month,
                        datasets: [
                            {
                                label: 'sales',
                                backgroundColor: '#49e2ff',
                                borderColor: '#46d5f1',
                                hoverBackgroundColor: '#CCCCCC',
                                hoverBorderColor: '#666666',
                                strokeColor: "#22A7F0",
    
                                data: sales
                            }
                        ]
                    };

                    var graphTarget = $("#graphCanvas");

                    var barGraph = new Chart(graphTarget, {
                        type: 'bar',
                        data: chartdata
                    });
                });
            }
        }
       
                        