/* dummy main.js file */
anychart.onDocumentReady(function() {

    var data = JSON.parse('{{ data | safe }}');

    // create a tag (word) cloud chart
    var chart = anychart.tagCloud(data);
    // set a chart title
    chart.title('NewsCloud | {{ paper }}');
    // set an array of angles at which the words will be laid out
    chart.angles([0]);
    // enable a color range
    chart.colorRange(true);
    // set the color range length
    chart.colorRange().length('80%');
    // display the word cloud chart
    chart.container("container");
    chart.draw();

    chart.listen("pointClick", function(e) {
        var url = "https://en.wikipedia.org/wiki/" + e.point.get("x");
        window.open(url, "_blank");
    });

});
