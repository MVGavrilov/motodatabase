
$(document).ready(function(){

$.get("/api/manufacturers", function(result){

    var manufacturers = result.data;

    for (const element of result) {
      $('#select_manufacturer').append($('<option>', {
            value: element.id,
            text: element.name
        }));
    }}

    );

$('#select_manufacturer').on('change', function() {
  var manufacturer_id = this.value;

$.get( "/api/models/" + manufacturer_id, function( result ) {
    $("#id_model").empty();

    for (const element of result) {
      $('#id_model').append($('<option>', {
            value: element.id,
            text: element.name
        }));
    }
});

});


});
