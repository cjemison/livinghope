$(document).ready(function(){  
    //is it better to have dynamic urls and js in the templates
    //or hard coded urls and js in a separate file?
    $('.contact-leader-link').click(function(){
        var leader_id = $(this).data('leader-id');
        var subject = $(this).data('subject')
        // var url = "{% url 'get_contact_leader_form' %}";
        // could do this in a data attr
        var url = '/get_contact_leader_form/'
        var current_url = window.location.href; 

        function update_contact_form(response){
          $('#contact-leader-modal-body').empty();
          $('<p>' +response+'</p>').appendTo('#contact-leader-modal-body');
          $('#contact-leader-submit-button').click(function(){

                // need to use ajax for callback to reload current page
                $("#contact-leader-submit-button").attr('disabled', 'disabled');
                $("#contact-leader-submit-spinner").show();
                $.ajax({
                    // url: "{% url 'process_contact_leader_form' %}",
                    url: '/process_contact_leader_form/',
                    type:'get',
                    data: $('#contact-leader-form').serialize(),
                    //this is recursively done since all the listeners
                    //must be set after the html is put into the DOM
                    success: function(data){
                        //this means that the form was invalid
                        if (data){
                            update_contact_form(data);

                        } else { //form submission was successful
                            location.reload();
                        }
                    }

                })
            })
        }

        $.get(url, {'leader-id': leader_id, 'system-subject':subject}, function(response){
            update_contact_form(response);
        })
    });
});