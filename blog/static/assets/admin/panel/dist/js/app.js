$(document).ready(function(){
    $('form').on('submit',function(event){

        var name = $('#inputPassword1').val();
        var yas = $('#inputPassword12').val();

        req = $.ajax({
            type : "POST",
            url  : '/update2',
            data : { 
                name : name ,
                yas : yas }

        })

        .done(function(data){
            if (data.error){
                $("#alert").text(data.error).show();
            

            }
            else {
                $("#alert").text(data.name).show();


            }

        });
        
        event.preventDefault();



    });

});
