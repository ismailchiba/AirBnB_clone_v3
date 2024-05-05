$(document).ready(function () {
    const amens = {};
    $('input:checkbox').click(function () {
      $(this).each(function () {
        if (this.checked) {
          amens[$(this).data('id')] = $(this).data('name');
        } else {
          delete amens[$(this).data('id')];
        }
      });
      if (Object.values(amens).length > 0) {
        $('.amenities h4').text(Object.values(amens).join(', '));
      } else {
        $('.amenities h4').html('&nbsp');
      }
    });
  });

  $.get('http://0.0.0.0:5001/api/v1/status/', function (data, status) {
    if (data.status === 'OK') {
        $('div#api_status').addClass('available');
    } else {
        $('div#api_status').removeClass('available');
    }
  })