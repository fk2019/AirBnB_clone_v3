document.addEventListener('DOMContentLoaded', () => {
  url = 'http://127.0.0.1:5001/api/v1/status/'
    $.get(url, function(data) {
	if (data.status === 'OK') {
	    $('#api_status').addClass('available');
	} else {
	    $('#api_status').removeClass('available');
    }
    });
  const amenities = {};
  $('input[type=checkbox]').on('change', function() {
    if ($(this).is(':checked')) {
      amenities[$(this).data('id')] = $(this).data('name');
    } else {
      delete amenities[$(this).data('id')];
    }
    if (Object.keys(amenities).length > 0) {
      $('.amenities h4:eq(0)').text(Object.values(amenities).join(', '));
    }
  })
});
