
$(document).ready(function () {
    $('#add_btn').click(function(){
        $('#new').addClass('hidden');
        $('#add_dependent_form').removeClass('hidden');
        $('#dependent_list').addClass('hidden')
        $('#cancel').removeClass('hidden');
    }) 

    $('#cancel_btn').click(function(){
        $('#new').removeClass('hidden');
        $('#add_dependent_form').addClass('hidden');
        $('#dependent_list').removeClass('hidden')
        $('#cancel').addClass('hidden');
    }) 
    
});

function showEdit(){
        $('#new').addClass('hidden');
        $('#add_dependent_form').removeClass('hidden');
        $('#dependent_list').addClass('hidden')
        $('#cancel').removeClass('hidden');
}
